# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Multiple Page List Extractor
============================

This strategy is required to parse lists which are very long and
expanded over multiple pages. If the content of some list steps is so
huge, that only one content line is on the page, it is very
hard/impossible to detect this as a valid lists, cause most of the
strategies expect more than one list item on a page. Furthermore it is
hard to distinguish between lists and headlines.
"""

import math

import utila

CHUNK_SIZE = 10


def merge(items):
    if not items:
        return []
    result = []

    header = items[0][0].bounding[1]  # y0
    y0 = header
    for page in items:
        for item in page:
            # avoid side effects to other content
            item = item.copy()
            item.bounding.y0 = utila.roundme(item.bounding.y0 + y0 - header)
            item.bounding.y1 = utila.roundme(item.bounding.y1 + y0 - header)
            result.append(item)
        footer = page.content.bottom
        y0 += footer - header
    return result


def chunks(items, size: int = 1):
    """\
    >>> chunks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), size=3)
    [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10,)]
    """
    result = []
    for index in range(math.ceil(len(items) / size)):
        result.append(items[index * size:(index + 1) * size])
    return result
