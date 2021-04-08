# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import words.headlines.machine
import words.headlines.strategies.cluster


@pytest.fixture
def master155pages50():
    source = power.link(power.MASTER155_PDF)
    pages = utila.ranged_tuple(0, 50)
    ptcns = serializeraw.create_pagetextcontentnavigators_frompath(
        source,
        pages=pages,
    )
    return ptcns, pages


MASTER155_SECTIONLIST = iamraw.Sections(content=[
    iamraw.sections.Introduction(0, 7, 1.0),
    iamraw.MainPart(
        start=7,
        end=13,
        trust=1.0,
        content=[
            iamraw.sections.Chapter(7, 13, 1.0),
            iamraw.sections.Chapter(14, 20, 1.0),
            iamraw.sections.Chapter(21, 28, 1.0),
            iamraw.sections.Chapter(29, 47, 1.0),
        ],
    ),
])


@utilatest.longrun
def test_headlines_cluster_master155(master155pages50):
    ptcns, pages = master155pages50
    # TODO: START END DOES NOT MATCH WITH CONTENT. IS THIS A PROBLEM?
    # SHOULD WE REMOVE THIS REDUNDANCY?
    result = words.headlines.machine.headlines(
        ptcns=ptcns,
        sectionlist=MASTER155_SECTIONLIST,
        chapters=[0, 1, 2, 3],
        strategies=[words.headlines.strategies.cluster],
        pages=pages,
    )
    result = result[0]  # single strategy was used
    assert len(result) == 5  # five different chapter
