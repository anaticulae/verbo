# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import functools
import itertools

import iamraw
import texmex
import utila

import words.boxed
import words.feature
import words.headlines
import words.text
import words.text.paragraph
import words.text.sentence


def extract_texts(
        loaded: words.feature.TextRequiredResources,
        require_headlinelevel: bool = True,
) -> words.text.PageContentPageTextDetectedList:
    """Iterate thrue document via headline and process the content
    between the headlines. Split Chapter into paragraphs and paragraphs
    into sentences and words.

    Args:
        loaded: resources provided by text module
        require_headlinelevel(bool): shrink chapter data to leveled headlines
    Returns:
        list of text pages with textutal content definition
    """
    result = split(loaded)

    if result:
        chapters = words.text.sentence.extract_textsections(
            result,
            merge_headlines=False,
            require_headlinelevel=require_headlinelevel,
        )
    else:
        # in some cases it is not possible to load any content, cause a
        # document is to short or the headlines are not parsed correctly.
        utila.error('could not merge empty pages')
        chapters = []

    grouped = groupby_page(chapters)

    result = []
    for page, item in grouped.items():
        item = sorted(item, key=container_start)
        result.append(
            words.text.PageContentPageTextDetected(
                page=page,
                content=item,
            ))
    return result


def groupby_page(chapters) -> dict:
    chapters = utila.flatten([split_textsection(item) for item in chapters])

    def getpage(item) -> int:
        if item.headline:
            return item.headline.page
        return item.pages[0]

    grouped = collections.defaultdict(list)
    for item in chapters:
        page = getpage(item)
        grouped[page].append(item)
    return dict(grouped)


def split_textsection(item: words.text.TextSection) -> words.text.TextSections:
    if not item.pages:
        return [item]
    result = [
        words.text.TextSection(
            headline=item.headline,
            content=[item.content[0]],
            pages=[item.pages[0]],
        )
    ]
    for content, page in zip(item.content[1:], item.pages[1:]):
        if page != result[-1].pages[0]:  # pylint:disable=E1136
            result.append(
                words.text.TextSection(
                    headline=iamraw.Headline(
                        title=None,
                        level=None,  # TODO: REMOVE AFTER FIXING LOADER/DUMPER
                        page=page,
                        container=-1,
                    ),
                    content=[content],
                    pages=[page],
                ))
        else:
            result[-1].pages.append(page)  # pylint:disable=E1136,E1101
            result[-1].content.append(content)  # pylint:disable=E1136,E1101
    return result


def container_start(item) -> int:
    """Determine start of headline container. Some headlines are spread
    over more than one line."""
    if item.headline is None:
        return -1
    if isinstance(item.headline.container, int):
        return item.headline.container
    return item.headline.container[0]


def split(loaded: words.feature.TextRequiredResources) -> words.text.PageTextWithHeadlines: # yapf:disable
    headlines = loaded.headlines
    pages = [int(item.page) for item in loaded.textnavigators]
    if not headlines:
        start, end = min(pages), max(pages)
        headlines = [[
            iamraw.Headline(title=None, level=None, page=page),
        ] for page in range(start, end + 1)]
    result = []
    # ensure to preserve correct page order when having pages without headline
    headlines = insert_empty_pages(headlines, max(pages))
    # start analyzing
    for headline in headlines:
        analyzed = analyze_page(
            headline,
            loaded.fontstore,
            loaded.textnavigators,
            loaded.border,
            loaded.boxes,
            loaded.lists,
        )
        if analyzed is None:
            # empty page
            continue
        result.append(analyzed)
    return result


def analyze_page(
        headlines,
        fontstore: iamraw.FontStore,
        textnavigators: texmex.PageTextNavigators,
        border: iamraw.Border,
        boxes: words.boxed.BoxedChecker,
        lists: 'ListLookUp',
) -> words.text.PageTextWithHeadlines:
    assert headlines, 'empty `headlines`'
    # Seek pagetextnavigator to correct positon
    prepared = prepare_analyze_page(
        headlines,
        textnavigators,
        fontstore,
        border,
    )
    if prepared is None:
        # Skip analyzing empty pages
        return None

    call = functools.partial(
        words.text.paragraph.collect_paragraph,
        page=prepared.number,
        pcn=prepared.pagetextcontentnavigator,
        boxes=boxes,
        lists=lists,
    )
    zipped = itertools.zip_longest(
        prepared.headlines,
        prepared.headlines[1:],
        fillvalue=None,
    )
    # collect paragraphs
    sections = [
        words.text.TextSection(
            headline=first,
            content=call(
                first=first,
                second=second,
            ),
        ) for (first, second) in zipped
    ]

    # clear result, remove empty content
    result = []
    for item in sections:
        if item.headline.container == -1 and not item.content:
            continue
        result.append(item)
    return words.text.PageTextWithHeadlines(
        page=prepared.number,
        content=result,
    )


def prepare_analyze_page(
        headlines,
        textnavigators,
        fontstore,
        borders,
) -> words.text.PageAnalyzeResources:
    """Add dummy headline if required.

    Some pages does not contain a headline or the headline starts after
    the first text content. Therefore adding a dummy headline is
    required to collect this content under the dummy headline.
    """
    page = headlines[0].page
    contentborder = utila.select_page(borders, page=page)
    if contentborder is None:
        return None

    pcn = utila.select_page(textnavigators, page=page)
    if pcn.offset == (None, None):
        # empty page
        return None

    fontstore = iamraw.FontContentStore(fontstore, pcn, page)
    # pcn.offset[0] - 1: the "virtual" headline is one container element before
    # the first content.
    if headlines[0].container is None:
        # start with None-Container
        headlines[0].container = pcn.offset[0] - 1  # absolute coordinate
    elif headlines[0].end > pcn.offset[0]:
        # the page does not start with a headline, without inserting an empty
        # line the starting content of the page is ignored
        # -> add starting container
        headline = iamraw.Headline(
            title=None,
            level=None,
            raw_level=None,
            page=page,
            container=pcn.offset[0] - 1,  # absoulte coordinate
        )
        headlines = [headline] + headlines
    else:
        # normal headline
        pass

    return words.text.PageAnalyzeResources(
        number=page,
        headlines=headlines,
        pagetextcontentnavigator=pcn,
        fontcontentstore=fontstore,
    )


def insert_empty_pages(
        headlines: iamraw.Headlines,
        maxpage: int,
) -> iamraw.Headlines:
    """Add pages with content but without any headlines.

    What happens when we forget to fill the headlines? All pages without
    any headlines are ignored in content analyzis.

    Args:
        headlines: loaded headlines, without virtual headlines
        maxpage: last loaded content page
    Returns:
        filled headline list
    """
    assert headlines, 'require at least one headline'
    flat = utila.flatten(headlines)
    # fill headlines
    heads = []
    for first, second in itertools.zip_longest(flat, flat[1:], fillvalue=None):
        heads.append(first)
        secondpage = second.page if second is not None else maxpage + 1
        # add virtual headlines to analyse content which does not ends
        # with headline.
        for index in range(first.page + 1, secondpage):
            heads.append(iamraw.Headline(title=None, level=None, page=index))
    headlines = [
        list(group) for _, group in itertools.groupby(heads, lambda x: x.page)
    ]
    return headlines
