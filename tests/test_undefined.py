# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import serializeraw

# pylint:disable=W0611
import tests.fixtures.restruct
import tests.resources
import words.headlines
import words.undefined

# collected by reading the pdf file
RESTRUCTURED_NON_TEXTUAL_PAGE = 10


# pylint:disable=W0621
def test_extract_undefined():
    """Text replacing the undefined items with content"""
    # TODO: Move to hey
    textexample = tests.fixtures.restruct.restructured_textexample()
    text = serializeraw.load_document(
        iamraw.path.text(tests.resources.RESTRUCT))
    textposition = serializeraw.load_textpositions(
        iamraw.path.textposition(tests.resources.RESTRUCT))

    border = serializeraw.load_pageborders(
        iamraw.path.sizeandborder(tests.resources.RESTRUCT))
    headerfooters = serializeraw.load_headerfooter(
        iamraw.path.headerfooters(tests.resources.RESTRUCT))

    contentborder = words.headlines.contentborder(border, headerfooters)
    extracted = words.undefined.extract_undefined(
        textexample,
        text,
        textposition,
        contentborder,
    )
    assert extracted
    non_empty_pages = [item for item in extracted if item]

    assert len(non_empty_pages) == RESTRUCTURED_NON_TEXTUAL_PAGE
