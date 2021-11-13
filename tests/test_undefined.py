# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

# pylint:disable=W0611
import tests.fixtures.restruct
import words.headlines
import words.undefined

# collected by reading the pdf file
RESTRUCTURED_NON_TEXTUAL_PAGE = 10


@pytest.mark.xfail
@utilatest.longrun
def test_extract_undefined():
    """Text replacing the undefined items with content"""
    # TODO: Move to hey
    textexample = tests.fixtures.restruct.docu27textexample()

    source = power.link(power.DOCU027_PDF)
    ptcns = serializeraw.ptcn_frompath(source)

    extracted = words.undefined.extract_undefined(textexample, ptcns)
    assert extracted
    non_empty_pages = [item for item in extracted if item]

    assert len(non_empty_pages) == RESTRUCTURED_NON_TEXTUAL_PAGE
