# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def unique(first, second):
    mixed = []
    for item in first:
        mixed.append(item)
    for item in second:
        mixed.append(item)
    mixed = utila.make_unique(mixed)
    expected = len(first) + len(second)
    return len(mixed) == expected


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
