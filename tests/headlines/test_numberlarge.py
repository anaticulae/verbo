# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utila
import utilatest

import words.headlines.strategies.numberlarge


@utilatest.nightly
def test_diss172_headlines():
    path = power.link(power.DISS172_PDF)
    pages = None
    section = serializeraw.load_sections(
        iamraw.path.sections_(path),
        pages=pages,
    )
    content = serializeraw.ptcn_frompath(path, pages=pages)
    result = words.headlines.machine.headlines(
        ptcns=content,
        sectionlist=section,
        strategies=[words.headlines.strategies.numberlarge],
        pages=pages,
    )
    headlines = utila.flatten(result)
    assert len(headlines) in (8, 9)  # NOT VALIDATED


@utilatest.longrun
def test_diss172_headlines_content_headline():
    """Ensure that false detected first level headline `CONTENTS` is
    removed by first level duplicated mechanism."""
    path = power.link(power.DISS172_PDF)
    pages = utila.rtuple(20, 70)
    section = serializeraw.load_sections(
        iamraw.path.sections_(path),
        pages=pages,
    )
    content = serializeraw.ptcn_frompath(path, pages=pages)
    result = words.headlines.machine.headlines(
        ptcns=content,
        sectionlist=section,
        strategies=[words.headlines.strategies.standard],
        pages=pages,
    )
    headlines = utila.flatten(utila.flatten(result))
    firstlevels = [
        item for item in headlines
        if words.headlines.strategies.isfirstlevel(item)
    ]
    assert not firstlevels
