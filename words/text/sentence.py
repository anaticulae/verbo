# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

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
):
    for section in page.content:
        current = []
        for seq in section.content:
            if not isinstance(seq, iamraw.Paragraph):
                if current:
                    for sentence in split_sentences(' '.join(current)):
                        yield section.headline, sentence
                if not skip_undefined:
                    yield section.headline, f'{seq.container}u'
                continue
            text = texmex.remove_highnotes(seq.content)
            text = text.replace(utila.NEWLINE, ' ').strip()
            current.append(text)
        if current:
            for sentence in split_sentences(' '.join(current)):
                yield section.headline, sentence


def merge_sentences(
        pages: words.text.PageTextWithHeadlines,
        skip_undefined: bool = False,
):
    assert len(pages) >= 2, 'require at least two `pages`'
    for current, after in zip(pages[0:-1], pages[1:]):
        current = list(visit_sentences(current, skip_undefined=skip_undefined))
        after = list(visit_sentences(after, skip_undefined=skip_undefined))
        for headline, sentence in current[0:-1]:
            yield headline, sentence
        # TODO: DIRTY
        last = current[-1]
        first = after[0]
        current_headline = last[0]
        if not is_sentence_closed(current[-1]):
            # merge sentence
            assert last
            assert first
            yield current_headline, last[1] + ' ' + first[1]
        else:
            # new page with headline start
            yield last
            if current_headline != first[0]:
                current_headline = first[0]
            if first[0].text is not None:
                # after page does not starts with virtual headline
                yield current_headline, first[1]
        # use headline of the page before to first headline of after page
        afterstart = 1  # normal headline
        if current_headline.text is None:
            # virtual headline
            afterstart = 0
        for headline, sentence in after[afterstart:]:
            if headline != current_headline:
                if headline.text is not None:
                    # do not replace headlines from page before with
                    # virtual none-headlines after page break.
                    current_headline = headline
            yield current_headline, sentence


def visit_chapters(pages):
    current = None
    collected = []
    done = AlreadyDone()
    for headline, sentence in merge_sentences(pages):
        if done.done((headline, sentence)):
            continue
        if current is None:
            # start
            current = headline
        if headline != current and headline.text is not None:
            yield current, collected
            collected = []
            current = headline
        collected.append(sentence)
    if collected:
        yield current, collected


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
            if token in WHITELIST:
                continue
            if token[:-1].isnumeric():
                # 1.; 13.
                continue
            if token.startswith('(') and not token.endswith(').'):
                # (z.B.), Phelps (2006).
                continue
        if lastchar in SIGN:
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
            if token[-2] in SIGN:
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
    if last_char in SIGN:
        # ... hello?
        return True
    if len(last) < 2:
        return False
    before_last_char = last[-2]
    if last_char in QUOTATION_CLOSE_SIGNS:
        # ... hello."
        if before_last_char in SIGN:
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


SIGN = {
    '!',
    '.',
    ':',
    '?',
}

# TODO: MOVE TO DUDEN PACKAGE
WHITELIST = {
    'Abb.',
    'Aufl.',
    'Bd.',
    'Co.',
    'Diss.',
    'Dok.',
    'Forts.',
    'Hrsg.',
    'Jg.',
    'S.',
    'Sp.',
    'Verf.',
    'Verl.',
    'Vol.',
    'a.a.O.',
    'al.',
    'bzw.',
    'ca.',
    'etc.',
    'evtl.',
    'f.',
    'ff.'
    'ggf.',
    'lat.',
    'mind.',
    'o.J.',
    'o.V.',
    'o.Ä',
    'u.a.',
    'usw.',
    'vgl.',
    'z.B.',
}
WHITELIST = {item.lower() for item in WHITELIST}

# a.a.O. = am angeführten Ort
# Jg. = Jahrgang
# Aufl. = Auflage
# o.J. = ohne Jahresangabe
# Bd. = Band
# o.V. = ohne Verfasserangabe
# Diss. = Dissertation
# S. = Seite
# Dok. = Dokument
# s. = siehe
# f. = (die) folgende
# Sp. = Spalte
# Verf. = Verfasser
# Forts. = Fortsetzung
# Verl. = Verlag
# H. = Heft
# Vol. = Volume (Band)
# Hrsg. = Herausgeber
