# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def global_score(items) -> int:
    content = utila.flatten([item.content for item in items])
    areas = sum([score_area(item.area) for item in content])
    return areas


def score_area(area):
    """\
    >>> score_area([(17, 18, 19, ), (0, 1, 2, 3), (0, 1, 2, 3)])
    11
    >>> score_area([0, 1, 2, 3])
    4
    """
    try:
        flat = utila.flatten(area)
    except TypeError:
        flat = area
    return len(flat)


def pagerange(items) -> int:
    """\
    >>> pagerange([1, 2, 3, 0, 1, 2, 3, 4, 0, 1])
    3
    """
    grouped = utila.groupby_ascending(items)
    return len(grouped)


def valid_area(items) -> bool:
    """\
    >>> valid_area([])
    False
    """
    if not items:
        return False
    if isinstance(items[0], int):
        items = [items]
    if len(items) == 1:
        return True
    for item in items:
        unqiue = utila.make_unique(
            utila.roundme(
                utila.diffs(item),
                digits=0,
                convert=False,
            ))
        if max(unqiue) > 2:
            return False
    return True


def valid_list_content(items) -> bool:
    for _, content in items:
        if content.count('..') > 5 or content.count('. .') > 5:
            # exclude table content `1 .Einleitung ............ 5`
            return False
    return True
