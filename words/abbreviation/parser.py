# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import utila

import words.feature.sentences


def parses(
    content: iamraw.PageContentTexts,
    lookup: iamraw.AbbreviationListLookup = None,
) -> iamraw.ExtractedTextAbbreviations:
    if lookup is None:
        lookup = iamraw.AbbreviationListLookup()
    result = []
    for textsection in content:
        parsed = parse_page(textsection.content, lookup)
        if not parsed.content:
            continue
        result.append(parsed)
    return result


def parse_page(  # pylint:disable=R0914
    textsections: iamraw.PageContentText,
    lookup: iamraw.AbbreviationListLookup,
) -> iamraw.ExtractedTextAbbreviation:
    collected = []
    pagenumber = -1
    page_sentence, page_word = 0, 0
    for textsection in textsections:
        for sentence, pagenumber in zip(textsection.content, textsection.pages):
            if words.feature.sentences.nosentence(sentence):
                continue
            wordx = german.word_tokenize(sentence, validate_sentences=False)
            if wordx is None:
                # TODO: REMOVE LATER?
                utila.info(f'incomplete sentence: {sentence}')
                continue
            for word in wordx:
                if isabbreviation(word, lookup):
                    position = iamraw.AbbreviationPosition(
                        page=pagenumber,
                        sentence=page_sentence,
                        word=page_word,
                    )
                    parsed = iamraw.Abbreviation(
                        short=word,
                        position=position,
                    )
                    collected.append(parsed)
                page_word += 1
            page_sentence += 1
    result = iamraw.ExtractedTextAbbreviation(
        page=pagenumber,
        content=collected,
    )
    return result


def isabbreviation(word: str, lookup) -> bool:
    if word in lookup:
        return True
    if isabbr(word):
        return True
    return False


def isabbr(item: str):  # pylint:disable=R0911
    """\
    F( T( MB PM SD M= MDHF \u2212MD HF M) MD Z=
    >>> isabbr('F(')
    False
    >>> isabbr('M=')
    False
    """
    if not isinstance(item, str):
        return False
    if len(item) <= 1:
        return False
    if unbalanced(item):
        return False
    if item.lower() in NOABBR:
        return False
    if item.isupper():
        if chars_invalid(item):
            return False
        return True
    return False


NOABBR = utila.splititems("""\
I II III IV V
""")
INVALIDS = '.-='


def chars_invalid(item):
    # A-B
    # B.
    if any(char for char in item if char in INVALIDS):
        return True
    return False


def unbalanced(item):
    if item.count('(') != item.count(')'):
        return True
    if item.count('[') != item.count(']'):
        return True
    if item.count('{') != item.count('}'):
        return True
    return False
