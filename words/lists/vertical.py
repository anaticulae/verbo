# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex

import words.lists.regex


def analyze_page(ptcn):
    grouped = texmex.group_linedistances_complex(ptcn)

    collected = []
    for group in grouped:
        content = ''.join([ptcn[item].text for item in group])
        parsed = words.lists.regex.parse_single(content)
        if parsed:
            collected.append((parsed, group))
        else:
            collected.append(None)

    lists = groupby_none(collected)

    result = []
    for listgroup in lists:
        current = iamraw.PageList()
        for row, indexs in listgroup:
            for item in row:
                assert len(item) == 2, str(item)
                current.append(*item)
            current.area.extend(indexs)  # pylint:disable=E1101
        if len(current) <= 1:
            # SKIP PARSED HEADLINE
            # TODO: THINK ABOUT SMARTER CONCEPT TO COVER SINGLE ITEM LIST
            # TODO: IS SINGLE ITEM LIST NECESSARY?
            continue
        result.append(current)
    return result


def groupby_none(items):
    """\
    >>> groupby_none([1, 2, None, 1, None, 3, 4, 5, None])
    [(1, 2), (1,), (3, 4, 5)]
    """
    # TODO: REPLACE WITH UTILA CODE
    result = []
    collected = []
    for item in items:
        if item:
            collected.append(item)
        else:
            if collected:
                result.append(tuple(collected))
                collected = []
    if collected:
        result.append(tuple(collected))
    return result
