# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilatest

import tests.fixtures.master72.seventytwo as fseventytwo
import words.feature.footerlink


@utilatest.longrun
def test_footerlink_extract_highnotes():
    required = fseventytwo.textrequired(pages=(3,))
    extracted = words.feature.footerlink.extract_highnotes(required)

    extracted = extracted[0].content
    values = [item.value for item in extracted]
    assert values == list(range(1, 7)), values
