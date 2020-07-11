# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import german
import iamraw
import texmex
import utila

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
                    lines.extend(german.split_sentences(' '.join(current)))
                    current = []
                lines.append('%du' % seq.container)
                continue
            # skip here to ensure that Undefined Container is added which
            # does not have any content, see commit.
            if seq.content is None:
                continue
            text = texmex.remove_highnotes(seq.content)
            text = text.replace(utila.NEWLINE, ' ').strip()
            current.append(text)
        if current:
            lines.extend(german.split_sentences(' '.join(current)))
            current = []
        result.append(
            words.text.TextSection(
                headline=section.headline,
                content=lines,
            ))
    return result


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
        skip_undefined: bool = False,
) -> typing.Tuple[iamraw.Headline, str]:
    """Yield tuple of Headline and extracted sentence."""
    result = []
    for section in page.content:
        current = []
        if not section.content:
            result.append((section.headline, ''))
            continue
        for seq in section.content:
            if not isinstance(seq, iamraw.Paragraph):
                if current:
                    for sentence in german.split_sentences(' '.join(current)):
                        result.append((section.headline, sentence))
                    current = []
                if not skip_undefined:
                    result.append((section.headline, f'{seq.container}u'))
                continue
            text = texmex.remove_highnotes(seq.content)
            text = text.replace(utila.NEWLINE, ' ').strip()
            current.append(text)
        if current:
            for sentence in german.split_sentences(' '.join(current)):
                result.append((section.headline, sentence))
    return result


def merge_sentences(  # pylint:disable=R0912,R1260
        pages: words.text.PageTextWithHeadlines,
        skip_undefined: bool = False,
) -> HeadlinedSentences:
    result = []
    lastheadline = None
    lastsentence = None
    lastpage = None
    for page in pages:
        if lastpage is not None:
            if lastpage + 1 != page.page:
                # TODO: Figurepage between sentences?
                # Do not merge sentence if empty page is between?
                lastsentence = None
                # TODO: THIS SENTENCE IS LOST, WE MUST MERGE IT?
        current = visit_sentences(page, skip_undefined=skip_undefined)
        for headline, sentence in current:
            if headline.text and headline != lastheadline and lastsentence:
                # headline does not contains a complete sentence and
                # follows by a headline with text and not with text is
                # None, which indicates that this is a new page.
                # HINT: lastpage can be None if no page was processed
                pagenr = lastpage if lastpage is not None else page.page
                result.append(
                    HeadlinedSentence(
                        headline=lastheadline,
                        page=pagenr,
                        sentence=lastsentence,
                    ))
                lastsentence = None
            if headline.text:
                lastheadline = headline
            else:
                headline = lastheadline
            pagenr = page.page
            if lastsentence:
                # merge with sentence of page before
                sentence = lastsentence + ' ' + sentence
                sentence = sentence.strip()
                lastsentence = None
                pagenr = lastpage
                headline = lastheadline
            if not sentence:
                result.append(
                    HeadlinedSentence(
                        headline=headline,
                        page=page.page,
                        sentence=None,
                    ))
            else:
                isundefined = words.undefined.intindex(sentence) is not None
                issentence = german.is_sentence_closed(sentence.split())
                if issentence or isundefined:
                    assert not lastsentence
                    result.append(
                        HeadlinedSentence(
                            headline=headline,
                            page=pagenr,
                            sentence=sentence,
                        ))
                else:
                    lastsentence = sentence
                    # merging on the same page is also possible
                    lastpage = page.page
        lastpage = page.page
    # headline
    if lastsentence:
        # non added headline on the end of the document
        result.append(
            HeadlinedSentence(
                headline=lastheadline,
                page=lastpage,
                sentence=lastsentence,
            ))
    return result


def visit_chapters(
        pages,
        merge_headlines: bool = True,
        require_headlinelevel: bool = True,
) -> words.text.TextSections:
    assert pages and len(pages) >= 1, 'require at least one page'
    result = []
    current = None
    collected, contentpages = [], []
    for headline, page, sentence in merge_sentences(pages):
        if current is None:
            # start
            current = headline
        merges = headline.text is not None if merge_headlines else True
        if headline != current and merges:  # and headline.text is not None:
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
