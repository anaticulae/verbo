# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import german
import iamraw
import texmex
import utila

import words.text


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


def merge_sentences(  # pylint:disable=R1260,too-many-branches
        pages: words.text.PageTextWithHeadlines,
        skip_undefined: bool = False,
):
    # TODO: REDUCE COMPLEXITY
    result = []
    if len(pages) == 1:
        pages = list(pages)  # avoid side effects
        pages.append(None)
    assert len(pages) >= 2, 'require at least two `pages`'
    for current, after in zip(pages[0:-1], pages[1:]):
        # it is possible to have a None successor or there is a whitepage
        # and no content after.
        valid_successor = after and (current.page + 1) == (after.page)

        current = visit_sentences(current, skip_undefined=skip_undefined)

        if valid_successor:
            for headline, sentence in current[0:-1]:
                result.append((headline, sentence))
        else:
            for headline, sentence in current:
                result.append((headline, sentence))
            continue

        last_headline, last_content = current[-1]  # page ending
        after = visit_sentences(after, skip_undefined=skip_undefined)
        first_headline, first_content = after[0]  # page start
        if not last_content.strip():
            # Headline at the end of a page
            result.append((last_headline, ''))
            continue
        last_sentence_closed = german.is_sentence_closed(last_content.split())
        if not last_sentence_closed:
            # merge sentence
            assert last_content
            if first_content:
                # TODO: CHECK FOR A VALID PAGE START
                result.append((last_headline,
                               last_content + ' ' + first_content))
            else:
                # Content not closed but next page starts with Headline
                result.append((last_headline, last_content))
                continue

        if last_sentence_closed:
            # new page with headline start
            result.append((last_headline, last_content))

        if last_sentence_closed:
            if last_headline != first_headline:
                last_headline = first_headline
            if first_headline.text is not None:
                # after page does not starts with virtual headline
                result.append((last_headline, first_content))

        # use headline of the page before to first headline of after page
        afterstart = 1  # normal headline
        if last_headline.text is None:
            # virtual headline
            afterstart = 0
        for headline, sentence in after[afterstart:]:
            if headline != last_headline:
                if headline.text is not None:
                    # do not replace headlines from page before with
                    # virtual none-headlines after page break.
                    last_headline = headline
            result.append((last_headline, sentence))
    return result


def visit_chapters(pages, merge_headlines=True):
    assert pages and len(pages) >= 1, 'require at least one page'
    result = []
    current = None
    collected = []
    done = utila.Single()
    for headline, sentence in merge_sentences(pages):
        if done.contains((headline, sentence)):
            continue
        if current is None:
            # start
            current = headline
        merges = headline.text is not None if merge_headlines else True
        if headline != current and merges:  # and headline.text is not None:
            result.append(words.text.TextSection(current, collected))
            collected = []
            current = headline
        if sentence:
            # do not store empty sentences?
            collected.append(sentence)
    if collected:
        result.append(words.text.TextSection(current, collected))
    return result
