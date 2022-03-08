# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import functools
import typing

import german
import iamraw
import texmex
import utila

import words.feature
import words.text
import words.undefined

HeadlinedSentence = collections.namedtuple(
    'HeadlinedSentence',
    'headline, page, sentence',
)
HeadlinedSentences = typing.List[HeadlinedSentence]


def find_sentences(page: words.text.PageTextWithHeadlines) -> words.text.TextSections: # yapf:disable
    result = []
    for section in page.content:
        lines = []
        current = []
        for seq in section.content:
            if not isinstance(seq, iamraw.Paragraph):
                if current:
                    current: str = utila.NEWLINE.join(current)
                    lines.extend(german.sentence_tokenize(current))
                    current = []
                lines.append(undefined_tostr(seq))
                continue
            # skip here to ensure that Undefined Container is added which
            # does not have any content, see commit XXX:commit,haha.
            if seq.content is None:
                continue
            text = texmex.remove_highnotes(
                seq.content,
                magic=True,
            )
            current.append(text)
        if current:
            lines.extend(german.sentence_tokenize(utila.NEWLINE.join(current)))
            current = []
        result.append(
            words.text.TextSection(
                headline=section.headline,
                content=lines,
            ))
    return result


def undefined_tostr(item: iamraw.Undefined) -> str:
    """\
    >>> undefined_tostr(iamraw.Undefined(content=10, container='cap'))
    'cap10'
    """
    if not item.content:
        return f'{item.container}u'
    return f'{item.container}{item.content}'


def visit_sections(page: words.text.PageTextWithHeadlines):
    for section in page.content:
        for seq in section.content:
            if not isinstance(seq, iamraw.Paragraph):
                continue
            # skip here to ensure that Undefined Container is added which
            # does not have any content, see commit.
            # TODO: DO WE NEED THIS HERE?
            if seq.content is None:
                continue
            yield section.headline, seq.content


def visit_sentences(
    page: words.text.PageTextWithHeadlines,
    *,
    skip_undefined: bool = False,
    merge_divis: bool = True,
    normalize_spaces: bool = True,
) -> typing.List[typing.Tuple[iamraw.Headline, str]]:
    """Yield tuple of Headline and extracted sentence.

    Go trough sections and extract sentences, formulas etc. and group
    them by headline.
    """
    sentence_tokenizer = functools.partial(
        german.sentence_tokenize,
        normalize_spaces=normalize_spaces,
        merge_divis=merge_divis,
    )
    result = []
    for section in page.content:
        current = []
        if not section.content:
            # if section does not contains any data, return headline with
            # empty content.
            result.append((section.headline, ''))
            continue
        # extract content between headlines
        current, appends = extract_section_content(
            section,
            current,
            skip_undefined=skip_undefined,
            sentence_tokenizer=sentence_tokenizer,
        )
        result.extend(appends)
        if current:
            current: str = utila.NEWLINE.join(current)
            for sentence in sentence_tokenizer(text=current):
                result.append((section.headline, sentence))
    return result


def extract_section_content(
    section,
    current,
    *,
    skip_undefined,
    sentence_tokenizer,
) -> tuple:
    result = []
    for seq in section.content:
        if isinstance(seq, iamraw.Paragraph):
            text = texmex.remove_highnotes(
                seq.content,
                magic=True,
            )
            current.append(text)
            continue
        # NoParagraph
        if current:
            current: str = utila.NEWLINE.join(current)
            for sentence in sentence_tokenizer(text=current):
                result.append((section.headline, sentence))
            current = []
        if not skip_undefined:
            if isinstance(seq, iamraw.DFormula):
                result.append((
                    section.headline,
                    f'#$@FORMULA@$#:{seq.content}',
                ))
            else:
                result.append((section.headline, f'{seq.container}u'))
    return current, result


def merge_sentences(
    pages: words.text.PageTextWithHeadlines,
    skip_undefined: bool = False,
    merge_divis: bool = True,
    normalize_spaces: bool = True,
) -> HeadlinedSentences:
    merger = SentenceMerge(
        skip_undefined=skip_undefined,
        merge_divis=merge_divis,
        normalize_spaces=normalize_spaces,
    )
    result = merger.process_pages(pages)
    return result


class SentenceMerge:

    def __init__(
        self,
        skip_undefined: bool = False,
        merge_divis: bool = True,
        normalize_spaces: bool = True,
    ):
        self.skip_undefined = skip_undefined
        self.merge_divis = merge_divis
        self.normalize_spaces = normalize_spaces

        self.result = []
        self.lastheadline = None
        self.lastsentence = None
        self.lastpage = None

    def process_pages(self, pages):
        for page in pages:
            self.process_page(page)
        # headline
        if self.lastsentence:
            # non added headline on the end of the document
            self.result.append(
                HeadlinedSentence(
                    headline=self.lastheadline,
                    page=self.lastpage,
                    sentence=self.lastsentence,
                ))
        return self.result

    def process_page(self, page):
        self.whitepage_before(page)
        current = visit_sentences(
            page,
            skip_undefined=self.skip_undefined,
            merge_divis=self.merge_divis,
            normalize_spaces=self.normalize_spaces,
        )
        for headline, sentence in current:
            self.incomplete_sentence_headline_changed(headline, page)
            self.incomplete_sentence_before_symbol_line(sentence)
            if headline.title:
                self.lastheadline = headline
            else:
                headline = self.lastheadline
            pagenr = page.page
            if self.lastsentence:
                # merge with sentence of page before
                sentence = f'{self.lastsentence} {sentence}'.strip()
                self.lastsentence = None
                pagenr = self.lastpage
                headline = self.lastheadline
            if not sentence:
                self.result.append(
                    HeadlinedSentence(
                        headline=headline,
                        page=page.page,
                        sentence=None,
                    ))
            else:
                isundefined = words.undefined.intindex(sentence) is not None
                isformula = texmex.is_formula(sentence)
                issentence = german.is_sentence_closed(sentence.split())
                if issentence or isundefined or isformula:
                    assert not self.lastsentence
                    self.result.append(
                        HeadlinedSentence(
                            headline=headline,
                            page=pagenr,
                            sentence=sentence,
                        ))
                else:
                    self.lastsentence = sentence
                    # merging on the same page is also possible
                    self.lastpage = page.page
        self.lastpage = page.page

    def whitepage_before(self, page):
        """Does white page is before current page and there is some
        incomplete sentence left."""
        if self.lastpage is None:
            return False
        if self.lastpage + 1 != page.page:
            # TODO: Figurepage between sentences?
            # Do not merge sentence if empty page is between?
            self.lastsentence = None
            # TODO: THIS SENTENCE IS LOST, WE MUST MERGE IT?
            return True
        return False

    def incomplete_sentence_headline_changed(self, headline, page) -> bool:
        if not headline.title:
            return False
        if headline == self.lastsentence:
            return False
        if not self.lastsentence:
            return False
        # headline does not contains a complete sentence and follows by a
        # headline with text and not with text is None, which indicates
        # that this is a new page.
        # HINT: lastpage can be None if no page was processed
        pagenr = self.lastpage if self.lastpage is not None else page.page
        self.result.append(
            HeadlinedSentence(
                headline=self.lastheadline,
                page=pagenr,
                sentence=self.lastsentence,
            ))
        self.lastsentence = None
        return True

    def incomplete_sentence_before_symbol_line(self, sentence) -> bool:
        if not self.lastsentence:
            return False
        isundefined = words.undefined.intindex(sentence) is not None
        isformula = texmex.is_formula(sentence)
        if not any((isundefined, isformula)):
            return False
        self.result.append(
            HeadlinedSentence(
                headline=self.lastheadline,
                page=self.lastpage,
                sentence=self.lastsentence,
            ))
        self.lastsentence = None
        return True


def extract_textsections(
    pagedata: words.feature.TextRequiredResources,
    *,
    merge_headlines: bool = True,
    require_headlinelevel: bool = True,
) -> words.text.TextSections:
    """Extract `TextSections out of chapters based on extracted headline
    definition.

    Args:
        pagedata: data to visit to extract TextSections
        merge_headlines(bool): if True: the content of a page without any
                  headline is merged to the headline of the page before.
                  if False: the content of a page starting without a
                  headline is treated as a new TextSection.
        require_headlinelevel(bool): if True, do not return headlines where
                  the headline level is None. For example "1.
                  Einleitung" has an level, "Anhang" not.
    Returns:
        List of extracted TextSection
    """
    assert pagedata and len(pagedata) >= 1, 'require at least one page'
    result = []
    current = None
    collected, contentpages = [], []
    for headline, page, sentence in merge_sentences(pagedata):
        if current is None:
            # start
            current = headline
        merges = headline.title is not None if merge_headlines else True
        if headline != current and merges:  # and headline.title is not None:
            result.append(
                words.text.TextSection(
                    current,
                    collected,
                    pages=contentpages,
                ))
            collected, contentpages = [], []
        if sentence:
            # do not store empty sentences?
            collected.append(sentence)
            contentpages.append(page)
        current = headline
    if collected:
        result.append(
            words.text.TextSection(
                current,
                collected,
                pages=contentpages,
            ))
    if require_headlinelevel:
        result = [
            item for item in result
            if item.headline and item.headline.level is not None
        ]
    return result
