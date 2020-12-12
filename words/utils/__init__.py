# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import german
import konrad
import utila


def sentences(texts, numbers: bool = False):
    number, current = 0, None
    for chunk in texts:
        for section in chunk.content:
            for page, sentence in zip(section.pages, section.content):
                if not numbers:
                    yield page, sentence
                else:
                    if current != page:
                        number = 0
                        current = page
                    else:
                        number += 1
                    yield page, number, sentence


def sentence_lookup(text) -> dict:
    lookup = collections.defaultdict(list)
    for page, sentence in sentences(text):
        lookup[page].append(sentence)
    return dict(lookup)


def sentence_plain(sentence, marks) -> list:
    result = []
    splitted = german.split_words(sentence, validate_sentences=False)
    for start, end in marks:
        selected = [splitted[item] for item in utila.ranged_tuple(start, end)]
        selected = selection_plain(selected)
        result.append(selected)
    return result


def selection_plain(items: list) -> str:
    items = [konrad.mark2str(item) for item in items]
    raw = ' '.join(items)
    raw = raw.replace('( ', '(')
    raw = raw.replace('[ ', '[')
    raw = raw.replace(' )', ')')
    raw = raw.replace(' ]', ']')
    raw = raw.replace(' ,', ',')
    raw = raw.replace(' ; ', '; ')
    raw = raw.replace(' - ', '-')
    raw = raw.replace(' : ', ': ')
    return raw


def references_plain(references, text) -> list:
    result = []
    lookup = sentence_lookup(text)
    for ref in references:
        page, sentenceid, marked = ref.page, ref.sentence, ref.marked
        selected = sentence_plain(  # pylint:disable=E1101
            lookup[page][sentenceid],
            marks=marked,
        )
        result.append(selected)
    return result
