# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila

import words.lists.multiplepages


def test_merge_pages():
    # TODO: WHAT SHOULD WE CHECK?
    source = power.link(power.MASTER072_PDF)
    pages = utila.ranged_tuple(35, 40)
    ptcns = serializeraw.create_pagetextcontentnavigators_frompath(
        path=source,
        pages=pages,
    )
    merged = words.lists.multiplepages.merge(ptcns)
    assert merged
    assert merged[-1].bounding[3] >= 3000
