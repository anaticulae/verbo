# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import texmex.sentences


def mark_quotes(word: iamraw.PageContentTexts) -> iamraw.PageContentTexts:
    for page in word:
        for textsection in page.content:
            textsection.content = find_quote(textsection.content)
    return word


def find_quote(text: list) -> list:
    result = []
    for line in text:
        if contains_quote(line):
            line = f'{texmex.sentences.QUOT}{line}'
        result.append(line)
    return text


def contains_quote(text: str) -> bool:
    splitted = german.word_tokenize(text, validate_sentences=False)
    for item in splitted:
        if isinstance(item, str):
            continue
        if 'QUOTATION' in item.name:
            return True
    return False
