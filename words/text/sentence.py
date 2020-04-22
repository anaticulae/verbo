# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import konrad
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
                    lines.extend(split_sentences(' '.join(current)))
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
            lines.extend(split_sentences(' '.join(current)))
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
                    for sentence in split_sentences(' '.join(current)):
                        result.append((section.headline, sentence))
                if not skip_undefined:
                    result.append((section.headline, f'{seq.container}u'))
                continue
            text = texmex.remove_highnotes(seq.content)
            text = text.replace(utila.NEWLINE, ' ').strip()
            current.append(text)
        if current:
            for sentence in split_sentences(' '.join(current)):
                result.append((section.headline, sentence))
    return result


def merge_sentences( # pylint:disable=R1260,too-many-branches
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
        last_sentence_closed = is_sentence_closed(last_content.split())
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
    result = []
    current = None
    collected = []
    done = AlreadyDone()
    for headline, sentence in merge_sentences(pages):
        if done.done((headline, sentence)):
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


class AlreadyDone:

    def __init__(self):
        self.saved = set()

    def done(self, item):
        hashed = str(item)
        if hashed in self.saved:
            return True
        self.saved.add(hashed)
        return False


def split_token(text: str):
    # replace text division -
    text = text.replace('-\n', '')
    # support multi line text
    text = text.replace('\n', ' ')
    tokens = text.split(' ')
    result = [token for token in tokens if token]
    return result


def split_sentences(text: str) -> utila.Strings:  # pylint:disable=R1260,R0912
    """Split a regular `text` into sentence chunks.

    Args:
        text(str): text to split without any newlines
    Returns:
        list of splitted sentences
    """
    # TODO: REPLACE WITH EXTERNAL SMART ALTERNATIVE, facebook, google or
    # something else.
    # TODO: MAKE ROBUST AGAINST WHITE SPACE
    result = []
    current = []
    for token in split_token(text):
        current.append(token)
        token = token.lower()  # make approach more robust
        lastchar = token[-1]
        if lastchar == '.':
            if len(token) == 2:
                # W. G.
                continue
            if token in konrad.ABBREVIATION_LOWER:
                continue
            if token[:-1].isnumeric():
                # 1.; 13.
                continue
            if token.startswith('(') and not token.endswith(').'):
                # (z.B.), Phelps (2006).
                continue
        if lastchar in konrad.SIGN:
            if token.startswith('('):
                # (2004b: 3) SKIP
                # (2006).    NOSKIP
                if token[-2] != ')':
                    continue
            if open_quotation_mark(current):
                continue
            result.append(' '.join(current))
            current = []
        if lastchar in '’”“':  # TODO: LOOK DEEPER
            if token[-2] in konrad.SIGN:
                # to observe.” Dennoch
                result.append(' '.join(current))
                current = []
    if current:
        result.append(' '.join(current))
    return result


def open_quotation_mark(tokens):
    count = 0
    # TODO: CHECK DIFFERENT DOUBLE QUOTATION MARK SIGNS
    for token in tokens:
        count += token.count('„')
        count -= token.count('”')
        count -= token.count('“')
    return count > 0


QUOTATION_CLOSE_SIGNS = '"”“'


def is_sentence_closed(token: list) -> bool:
    """Check that the last character of the last token of a sentences contains
    a sentence close sign."""
    assert token, 'empty sentence'
    assert isinstance(token, (list, tuple)), type(token)
    last = token[-1].strip()
    last_char = last[-1]
    if last_char in konrad.SIGN:
        # ... hello?
        return True
    if len(last) < 2:
        return False
    before_last_char = last[-2]
    if last_char in QUOTATION_CLOSE_SIGNS:
        # ... hello."
        if before_last_char in konrad.SIGN:
            return True
    return False


def is_sentence(sentence: str, min_length: int = 4):
    if len(sentence) < min_length:  # TODO: HOLY VALUE
        # sentence is too short
        return False
    length = len(sentence)
    dotcount = sentence.count('.')
    percent_sentence = sentence.count('.') / length if length else 0.0

    if dotcount >= 3 and percent_sentence > 0.04:  # TODO: HOLY VALUE
        # sentence contains too much dots, maybe a toc line
        return False
    splitted = split_sentences(sentence)
    if len(splitted) > 1:
        return False
    token = split_token(splitted[0])
    if is_sentence_closed(token):
        return True
    return False
