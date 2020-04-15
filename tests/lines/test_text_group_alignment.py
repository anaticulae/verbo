# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw

import tests.resources
import words.lines.style


def test_page_linealignments_expected_master72_page4():
    source = tests.resources.MASTER72
    pages = (4,)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=pages,
    )

    page4 = navigators[0]
    current = words.lines.style.page_linealignments_expected(page4)
    expected = [
        words.lines.style.TextAlignment.BLOCK,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.BLOCK,
        words.lines.style.TextAlignment.RIGHT,
    ]
    assert current == expected, expected


def test_page_linealignments_expected_master72_page6():
    source = tests.resources.MASTER72
    pages = (6,)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=pages,
    )
    page6 = navigators[0]
    current = words.lines.style.page_linealignments_expected(page6)
    expected = [
        [
            words.lines.style.TextAlignment.LEFT,
            words.lines.style.TextAlignment.CENTER,
            words.lines.style.TextAlignment.BLOCK,
        ],
        words.lines.style.TextAlignment.BLOCK,
        [
            words.lines.style.TextAlignment.CENTER,
            words.lines.style.TextAlignment.BLOCK,
        ],
        words.lines.style.TextAlignment.BLOCK,
        words.lines.style.TextAlignment.BLOCK,
        words.lines.style.TextAlignment.RIGHT,
    ]
    assert current == expected, expected


@pytest.mark.xfail(reason='grouping does not work properly')
def test_page_linealignments_expected_homework40_page3():
    source = tests.resources.HOMEWORK40
    pages = (3,)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=pages,
    )
    page3 = navigators[0]
    current = words.lines.style.page_linealignments_expected(page3)

    expected = [
        words.lines.style.TextAlignment.CENTER,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.RIGHT,
    ]
    assert current == expected, expected


@pytest.mark.xfail(reason='grouping does not work properly')
def test_page_linealignments_expected_homework40_page4():
    source = tests.resources.HOMEWORK40
    pages = (4,)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=pages,
    )
    page4 = navigators[0]
    current = words.lines.style.page_linealignments_expected(page4)

    expected = [
        words.lines.style.TextAlignment.CENTER,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.LEFT,
        words.lines.style.TextAlignment.RIGHT,
    ]
    assert current == expected, expected
