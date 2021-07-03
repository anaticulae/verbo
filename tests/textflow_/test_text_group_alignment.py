# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import textflow.alignment.style


@utilatest.longrun
@utilatest.requires(power.MASTER072_PDF)
def test_page_linealignments_expected_master72_page4():
    source = power.link(power.MASTER072_PDF)
    pages = (4,)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=pages,
    )

    page4 = navigators[0]
    current = textflow.alignment.style.page_linealignments_expected(page4)
    expected = [
        textflow.alignment.style.TextAlignment.BLOCK,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.BLOCK,
        textflow.alignment.style.TextAlignment.RIGHT,
    ]
    assert current == expected, expected


@pytest.mark.xfail(reason='enable later')
@utilatest.longrun
@utilatest.requires(power.MASTER072_PDF)
def test_page_linealignments_expected_master72_page6():
    source = power.link(power.MASTER072_PDF)
    pages = (6,)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=pages,
    )
    page6 = navigators[0]
    current = textflow.alignment.style.page_linealignments_expected(page6)
    expected = [
        [
            textflow.alignment.style.TextAlignment.LEFT,
            textflow.alignment.style.TextAlignment.CENTER,
            textflow.alignment.style.TextAlignment.BLOCK,
        ],
        textflow.alignment.style.TextAlignment.BLOCK,
        [
            textflow.alignment.style.TextAlignment.CENTER,
            textflow.alignment.style.TextAlignment.BLOCK,
        ],
        textflow.alignment.style.TextAlignment.BLOCK,
        textflow.alignment.style.TextAlignment.BLOCK,
        textflow.alignment.style.TextAlignment.RIGHT,
    ]
    assert current == expected, expected


@utilatest.requires(power.HOME040_PDF)
def test_page_linealignments_expected_homework40_page3():
    source = power.link(power.HOME040_PDF)
    navigators = serializeraw.create_pagetextnavigators_frompath(source,)
    border = textflow.alignment.style.document_textfeed(navigators)

    current = textflow.alignment.style.page_linealignments_expected(
        utila.select_page(navigators, 3),
        border=border,
    )

    expected = [
        textflow.alignment.style.TextAlignment.CENTER,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.BLOCK,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.BLOCK,
    ]
    assert current[0:9] == expected, expected


@utilatest.requires(power.HOME040_PDF)
def test_page_linealignments_expected_homework40_page4():
    source = power.link(power.HOME040_PDF)
    navigators = serializeraw.create_pagetextnavigators_frompath(source)
    border = textflow.alignment.style.document_textfeed(navigators)

    current = textflow.alignment.style.page_linealignments_expected(
        utila.select_page(navigators, page=4),
        border=border,
    )

    expected = [
        textflow.alignment.style.TextAlignment.CENTER,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.LEFT,
        textflow.alignment.style.TextAlignment.LEFT,
    ]
    assert current[0:6] == expected, expected
