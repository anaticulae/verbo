# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import words.headlines.strategies.singlepage


def test_singlepage_bachelor067():
    source = power.link(power.BACHELOR067_PDF)
    ptcns = serializeraw.create_pagetextcontentnavigators_frompath(source)
    parsed = words.headlines.strategies.singlepage.pagewise(ptcns)
    assert len(parsed) == 1
