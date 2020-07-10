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
import words.path


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


def test_extract_lists():
    source = power.link(power.MASTER072_PDF)
    pages = utila.ranged_tuple(35, 50)
    lists = extract_multiple_lists(source, pages)
    # TODO: REPLACE AFTER CHANGING DATA STRUCTURE
    page39 = utila.select_page(lists, 39)
    assert len(page39.content) == 1
    assert len(page39.content[0]) == 4


def test_extract_multiple_lists_master72():
    source = power.link(power.MASTER072_PDF)
    pages = None
    lists = extract_multiple_lists(source, pages)
    # TODO: REPLACE AFTER CHANGING DATA STRUCTURE
    # lists = utila.flatten(lists)

    # lists on 4 starting pages
    assert len(lists) == 4

    listinstances = utila.flatten([item.content for item in lists])
    # number of lists
    assert len(listinstances) == 4


def extract_multiple_lists(source, pages):
    ptcns = serializeraw.create_pagetextcontentnavigators_frompath(
        path=source,
        pages=pages,
    )
    headlines = serializeraw.load_headlines(
        words.path.headlines(source),
        pages=pages,
    )
    lists = words.lists.multiplepages.extract_lists(ptcns, headlines)
    return lists
