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
import textflow.alignment.info
import textflow.alignment.style
import textflow.features.alignment


def test_info_adapter():
    source = tests.resources.MASTER72
    pages = (10, 11, 12, 13)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    current = textflow.features.alignment.extract_alignment_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    adapter = textflow.alignment.info.AlignmentInfo(navigators, current)

    layout = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=pages,
    )
    first_page = layout[0]

    item = first_page[5]
    selected = adapter.alignment(first_page.page, item)
    assert selected, selected
    assert selected == [textflow.alignment.style.TextAlignment.BLOCK], selected
