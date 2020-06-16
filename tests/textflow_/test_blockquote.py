# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import tests.resources
import textflow.features.blockquote


def test_blockquote_master72():
    source = tests.resources.MASTER72
    pages = (15,)

    ptcn = serializeraw.create_pagetextcontentnavigators_frompath(
        source,
        pages=pages,
    )
    extracted = textflow.features.blockquote.analyze_page(ptcn[0])
    assert len(extracted) == 2
