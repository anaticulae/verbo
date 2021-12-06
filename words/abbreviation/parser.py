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
        if not parsed[1]:
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
                utila.info(f'incomplete sentence: {sentence}')
                continue
            for word in wordx:
                if word in lookup or isabbreviation(word):
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


def isabbreviation(item: str):
    if not isinstance(item, str):
        return False
    if len(item) <= 1:
        return False
    if item.isupper():
        if any((char in item for char in ['.', '-'])):
            # A-B
            # B.
            return False
        return True

    return False


def abbreviation(items):
    # remove special signs
    items = [item for item in items if isinstance(item, str)]
    # make unique
    items = list(set(items))
    items = [item for item in items if 2 <= len(item) <= 5]
    items = [item for item in items if not utila.isnumber(item)]
    items = [item for item in items if count_upper(item) / len(item) >= 0.3]
    return items


def count_upper(items):
    return len([item for item in items if item.isupper()])
