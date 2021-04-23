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

import words.utils

PATTERN = (
    '(Abb. 100 und 101)',
    '(s. Abb. 3)',
    '(siehe Abb. 100 und 101)',
    '(siehe Abb. 100)',
    '(siehe Abbildung 100)',
    '(siehe Abbildung 2.12)',
    'Abb. 100 und 1001',
    'Abb. 100 und Abb. 101',
    'Abbildung 2.1',
    'Abbildungen 100 und 1001',
    's. Abb. 3',
    'siehe Abbildung 2.12',
)


def parse_text(
        text,
        pattern=PATTERN,
        compare_content: bool = True,
) -> iamraw.DocRefs:
    result = []
    for page, number, sentence in words.utils.sentences(text, numbers=True):
        parsed = german.searches(
            pattern,
            sentence,
            compare_content=compare_content,
        )
        if not parsed:
            continue
        parsed = remove_overlapping(parsed)
        result.append(iamraw.DocRef(page, number, parsed))
    return result


def remove_overlapping(items: list) -> list:
    """\
    >>> remove_overlapping([(0, 5), (4, 9)])
    [(0, 5), (4, 9)]
    >>> remove_overlapping([(2, 5), (3, 4)])
    [(2, 5)]
    """
    items = sorted(items, key=lambda x: x[0])
    result = []
    done = set()
    for item in items:
        start, stop = item
        if all((item in done for item in range(start, stop))):
            continue
        for index in range(start, stop):
            done.add(index)
        result.append(item)
    return result
