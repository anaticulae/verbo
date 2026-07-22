# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import hoverpower
import utilotest

import words.feature


@configos.cache_small
def textrequired(pages=None):
    utilotest.fixture_requires(hoverpower.MASTER072_PDF)
    return words.feature.load_resources_frompath(
        hoverpower.link(hoverpower.MASTER072_PDF),
        pages=pages,
    )
