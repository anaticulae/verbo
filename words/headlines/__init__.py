# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import abc
import collections
import re
import typing

import iamraw
import iamraw.sections
import sections.feature.section
import texmex
import utila

import words.headlines.cluster
import words.loader.basic

WHITELIST = {
    'Anhang',
    'Eidesstattliche Erklärung',
    'Erklärung',
    'Literaturverzeichnis',
}

ChapterRange = collections.namedtuple('ChapterRange', 'start end')
ChapterRanges = typing.List[ChapterRange]


class HeadlineExtractorStrategy(abc.ABC):  # pylint:disable=too-many-instance-attributes
    """Strategy approach to determine the `Headlines` of a given set of
    pages.

    Invoke `result` to determine result of current stategy.

    Progress:

    .. code-block :: none

        for chapter in chapters:
            extract_chapter
                for page in chapter:
                    extract_page
                        for line in page:
                            extract_headlines
                                if should_skip:
                                    continue
                                add Headline
    """

    def __init__(
            self,
            basic: words.loader.basic.BasicRequiredResources,
            sectionlist: typing.List[iamraw.Sections],
            chapters: ChapterRanges = None,
    ):
        """Extract Headlines out of document.

        Args:
            basic: extracted pages with font and size information.
            sectionlist: list that devides pages into introduction, main-
                         content, appendix
            chapters: list with tuple of (start, end) of defined chapter
        """
        self.__result = {}

        self.sectionlist = sectionlist
        self.pagetextnavigators = basic.textnavigators
        self.fontstore = basic.fontstore
        self.sizeandborder = basic.sizeandborder
        self.headerfooters = basic.headerfooters
        self.chapters, self.content = prepare_chapter_and_content(
            sectionlist,
            chapters,
        )
        # bounding box of text content
        self.border = contentborder(
            self.sizeandborder,
            self.headerfooters,
        )
        self.setup()
        self.ready = False

    def result(self, pages=None):
        if self.ready:
            return self.__result
        self.ready = True
        # run extraction
        for chapter in self.chapters:
            # HACK: REMOVE LAST PAGE TO PASS SHOULD_SKIP THERE IS A
            # PROBLEM WITH THE LAST AREA, CAUSE THE INDEX OF AN AREA IS
            # EXPANDED + 1 OVER THE AREA. AT THE LAST AREA THIS EXPANDS
            # OUTSIDE OF THE DOCUMENT. HACKING PAGE SKIP CHECK SEEMS NOT
            # SO PROBLEMATIC HERE, BUT MUST BE FIXED.
            chapter_pages = list(self.content[chapter])
            chapter_pages = tuple(chapter_pages[:-1])  # pylint:disable=R0204
            if utila.should_skip(chapter_pages, pages):
                continue
            self.extract_chapter(chapter)

        # filter result
        self.__result = self.filter(self.__result)
        extracted = [item for item in self.__result.values()]

        flatten = utila.flatten(extracted)
        grouped = []
        if flatten:
            if isinstance(flatten[0].level, dict):
                # HACK NOLEVEL?
                flatten[0].level = None
            grouped.append([flatten[0]])
        for item in flatten[1:]:
            if isinstance(item.level, dict):
                # HACK NOLEVEL?
                item.level = None
            if item.level is None or item.level == 1:
                grouped.append([item])
            else:
                grouped[-1].append(item)
        return grouped

    def filter(self, items):  # pylint:disable=R0201
        """Convert level etc."""
        # TODO: IMprove this
        convert_level(items)
        return items

    def setup(self):
        """Run before starting extraction."""
        self.textsize = texmex.document_textsize(
            navigators=self.pagetextnavigators)

        # TODO: DECIDE WHAT TODO WITH TEXTDISTANCE
        textdistance = texmex.document_textdistance(
            navigators=self.pagetextnavigators,
            borders=self.sizeandborder,
            digits=0,
        )
        try:
            self.textdistance = textdistance[0]
        except TypeError:
            self.textdistance = textdistance

    def extract_chapter(self, chapter: int):
        assert 0 <= chapter < self.chaptercount, chapter
        result = []
        start, end = self.content[chapter]
        for page in range(int(start), int(end + 1)):
            border = utila.select_page(self.border, page=page)
            textnavigator = utila.select_page(
                self.pagetextnavigators,
                page=page,
            )
            if not border or not textnavigator:
                # empty page
                continue
            pagecontent = texmex.PageTextContentNavigator(
                textnavigator,
                border,
            )
            pageheadlines = self.extract_page(pagecontent)
            result.extend(pageheadlines)
        self.__result[chapter] = result

    def extract_page(
            self,
            pagecontent,
    ):
        result = []
        xoff, xend = pagecontent.offset
        xoff = xoff if xoff is not None else 0
        bounds = texmex.textbounds(
            pagecontent,
            utila.select_page(self.border, page=pagecontent.page),
        )
        without_content = [item.bounds for item in bounds]
        # PageContentNavigator, the header and footer is ignored
        textdistances = texmex.fontdistance_textbounds(without_content)

        textfeeds = [item.bounds.leftdist for item in bounds]

        for containerid, item in enumerate(pagecontent, start=xoff):
            splitted = item.text.splitlines()
            if len(splitted) > 1:
                # TODO: REMOVE?
                continue
            headline = self.extract_headline(
                textinfo=item,
                textdistances=textdistances,
                textfeeds=textfeeds,
                page=pagecontent.page,
                containerid=containerid,
                content_range=(xoff, xend),
            )
            if not headline:
                continue
            result.append(headline)
        return result

    def extract_headline(
            self,
            textinfo,
            textdistances,
            textfeeds,
            page,
            containerid,
            content_range,
    ):  # pylint:disable=R0914
        text = textinfo.text
        contentstart, contentend = content_range
        distanceid = containerid - contentstart
        # TODO: BEFORE, AFTER, TOP OF THE PAGE? DISTANCE IS ZERO ON PAGE
        # START.
        fontdistance = textdistances[distanceid + 1]
        textfeed = textfeeds[distanceid]
        textsize = texmex.TextStyle.textsizes(textinfo.style)

        distance_tosmall = fontdistance < self.smallest_headlinedistance()
        headline_tosmall = textsize < self.smallest_textsize()
        lastitem = (distanceid + 1) == contentend
        skip = self.should_skip(
            distance_tosmall=distance_tosmall,
            headline_tosmall=headline_tosmall,
            textfeed=textfeed,
            lastitem=lastitem,
        )
        if len(text) <= 6:  # TODO: MIN HEADLINE LENGTH
            return None

        if headline_blacklisted(text):
            utila.debug(f'{self.__class__.__name__}: {skip} {text}')
            return None

        utila.debug(f'{self.__class__.__name__}: {skip} {text}')
        if skip:
            return None

        dist_top = textdistances[distanceid]
        dist_bottom = None if lastitem else textdistances[distanceid + 1]

        style = dict(
            textsize=textsize,
            before=dist_top,
            after=dist_bottom,
            feed=textfeed,
        )
        headline = iamraw.Headline(
            container=containerid,
            level=style,
            page=page,
            title=text.strip(),
        )
        return headline

    @abc.abstractmethod
    def should_skip(
            self,
            distance_tosmall,
            headline_tosmall,
            textfeed,
            lastitem,
    ):
        pass

    @property
    def chaptercount(self):
        return len(self.chapters)

    @abc.abstractmethod
    def smallest_headlinedistance(self):
        pass

    @abc.abstractmethod
    def smallest_textsize(self):
        pass


BLACK_CHAPTER = re.compile(r'(Kapitel|Chapter)[ ]{0,5}\d{1,2}', re.IGNORECASE)


def headline_blacklisted(item: str) -> bool:
    """\
    >>> headline_blacklisted('KAPITEL  1 ')
    True
    >>> headline_blacklisted('Chapter 5 ')
    True
    """
    item = item.strip()
    if BLACK_CHAPTER.match(item):
        return True
    return False


def prepare_chapter_and_content(sections_, chapter):
    assert isinstance(sections_, iamraw.Sections)
    assert sections_, 'no sections provided'
    if chapter is None:
        # process all chapter
        # TODO: clearify code
        content = determine_contentrange(sections_)
        chapter = list(range(len(content)))
    else:
        content = sections.feature.section.chapters(sections_)
        chapter = [chapter] if isinstance(chapter, int) else chapter
    return chapter, content


def contentborder(sizeandborders, headerfooters):
    assert all([isinstance(it, iamraw.PageSizeBorder) for it in sizeandborders])
    result = {}
    pages = [item.page for item in sizeandborders]
    for page in pages:
        selected = utila.select_page(sizeandborders, page)
        pageheight = selected.size.height
        pageborder = selected.border
        # Not every page provides footer and/or header information,
        # therefore we have to check if footerheader exists before
        # acessing the value.
        footerheader = utila.select_page(headerfooters, page)

        top = 0
        if footerheader and footerheader.header:
            top = pageheight * footerheader.header.end

        bottom = pageheight
        if footerheader and footerheader.footer:
            bottom = pageheight * footerheader.footer.begin

        top, bottom = utila.roundme(top), utila.roundme(bottom)

        result[page] = iamraw.Border(
            left=pageborder.left,
            right=pageborder.right,
            top=top,
            bottom=bottom,
        )
    return result


FIRST_LEVEL = 0.8  # TODO: HOLY VALUE
SECOND_LEVEL = 0.5


def convert_level(result: iamraw.PagesHeadlineList) -> int:
    """Convert chapter level based on text distances to logical level
    (1,2,3,4,...).

    Hint: This function updates the level
    TODO: copy items
    """
    utila.call('convert_level')
    if (not result or not any(result.values()) or
            not any([item for item in result.values()])):
        # check that result pages are empty
        utila.info('empty PageHeadlineList')
        return {}
    assert isinstance(result, dict), type(result)

    nolevel = []
    for item in result.values():
        nolevel.extend(item)
    level = [item for item in nolevel if isinstance(item.level, int)]

    if not level:
        result = words.headlines.cluster.cluster_headline_level(result)
    return result


def determine_contentrange(items) -> ChapterRanges:
    """Iterate thrue `sections` and search for `Chapter` to determine
    section start and end.

    In some cases no `Chapter` is present. This can happen if you
    analyse only a few pages or a single one. In this case the start and
    end is defined by normal items.

    Returns:
        list of `ChapterRange` (start, end)
    """
    # analyze all chapter of the document
    contents = [
        item for item in items if isinstance(
            item,
            (
                iamraw.MainPart,
                iamraw.MultipleSection,
                iamraw.sections.Appendix,
                iamraw.sections.Unknown,
            ),
        )
    ]
    chapters = flat_chapters(contents)

    if not chapters and contents:
        # no chapter is present - create `virtual chapter`
        chapters = [[item for item in content.content] for content in contents]
        chapters = utila.flatten(chapters)
    if not chapters:
        # TODO: INVESTIGATE HERE
        return []
    result = items_before_firstchapter(chapters, contents)
    for current, after in zip(chapters[:-1], chapters[1:]):
        floatrange = isinstance(current.end, float) or isinstance(after.start, float) # yapf:disable
        if current.end == after.start and floatrange:
            # multi page: content on same page
            result.append((current.start, current.end))
        else:
            result.append((current.start, after.start - 1))
    result.append((chapters[-1].start, contents[-1].end))
    # ensure ascending page numbers
    assert all([start <= end for start, end in result]), str(result)
    return result


def flat_chapters(contents):
    result = []
    for item in contents:
        if isinstance(item, iamraw.MainPart):
            result.extend(item.content)
        elif isinstance(item, iamraw.sections.Appendix):
            result.append(item)
    result = utila.select_type(
        result,
        (iamraw.sections.Chapter, iamraw.sections.Appendix),
    )
    return result


def items_before_firstchapter(chapters, contents):
    """Determine items before the first **loaded** chapter starts.

    This is required, when loading a part in the middle of a document.
    To extract headlines, it is required to have `Chapter` separators to
    determine the range of the different chapter. Parts of chapter are
    not loaded if start of chapter is not selected.
    """
    assert chapters
    # check if content exists before the first chapter starts
    firstchapter_start = chapters[0].start
    before = [[
        item for item in content.content if item.start < firstchapter_start
    ] for content in contents]
    # remove empty pages
    before = [item for item in before if item]
    before = utila.flatten(before)
    if not before:
        return []
    return [(before[0].start, before[-1].end)]


def numbered_level(raw: str) -> int:
    """Convert number to raw level.

    >>> numbered_level('5 Geology')
    1
    >>> numbered_level('2. Zentrum')
    1
    >>> numbered_level('2.1.3. Abschluss')
    3
    >>> numbered_level('2.1 Anhang')
    2
    >>> numbered_level('2..1... Fehlerfrei') # ignore typos
    2
    >>> numbered_level('2020 This is not a headline level')
    False
    """
    # TODO: REPLACE WITH GROUPME CODE
    # TODO: MOVE TESTS?
    raw = raw.strip()
    if not raw:
        return None
    raw = raw.split()[0]
    if not '.' in raw:
        if raw.isnumeric():
            raw_level = int(raw)
            if raw_level > 30:  # TODO: HOLY VALUE
                return False
            return 1
        return None
    # 2.1.3
    splitted = [item for item in raw.split('.') if item]
    return len(splitted)
