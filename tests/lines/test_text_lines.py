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
import utila

import tests.resources
import words.lines.style


def test_extract_linestyleinfo_master72():
    content_navigators = serializeraw.create_pagetextcontentnavigators_frompath(
        tests.resources.MASTER72, pages=(3,), prefix='oneline')
    left = 114.0
    right = 527.5
    linestyles = words.lines.style.page_textalignment(
        content_navigators[0],
        left=left,
        right=right,
    )
    assert linestyles == words.lines.style.TextAlignment.BLOCK, str(linestyles)


@pytest.mark.parametrize('source, expected', [
    pytest.param(
        tests.resources.MASTER72,
        words.lines.style.TextAlignment.BLOCK,
        id='master72',
    ),
    pytest.param(
        tests.resources.BACHELOR37,
        words.lines.style.TextAlignment.BLOCK,
        id='bachelor37',
    ),
    pytest.param(
        tests.resources.HOWTO_PYPORTING,
        words.lines.style.TextAlignment.BLOCK,
        id='pyporting',
        marks=pytest.mark.xfail(reason='require imporvement'),
    ),
    pytest.param(
        tests.resources.HOMEWORK40,
        words.lines.style.TextAlignment.LEFT,
        id='homework40',
    ),
])
@utila.skip_longrun
def test_document_alignment(source, expected):
    content_navigators = serializeraw.create_pagetextnavigators_frompath(
        source, prefix='oneline')
    alignment = words.lines.style.document_alignment(content_navigators)
    assert alignment == expected, alignment


@pytest.mark.xfail(reason='improve block parser')
def test_page_linealignment():
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.HOMEWORK40,
        prefix='oneline',
    )
    left, right = words.lines.style.document_textfeed(navigators)
    page4 = navigators[4]
    linealignments = words.lines.style.page_linealignments(page4, left, right)
    assert linealignments[0] == words.lines.style.TextAlignment.CENTER
    assert linealignments[1] == words.lines.style.TextAlignment.LEFT
    assert linealignments[-1] == words.lines.style.TextAlignment.RIGHT


def test_page_linealignment_master72_page4():
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.MASTER72,
        prefix='oneline',
    )
    left, right = words.lines.style.document_textfeed(navigators)
    page4 = navigators[4]
    linealignments = words.lines.style.page_linealignments(page4, left, right)
    assert linealignments[0] == words.lines.style.TextAlignment.BLOCK
    assert linealignments[2] == words.lines.style.TextAlignment.LEFT
    assert linealignments[3] == words.lines.style.TextAlignment.LEFT
    assert linealignments[4] == words.lines.style.TextAlignment.BLOCK
    assert linealignments[-1] == words.lines.style.TextAlignment.RIGHT


@pytest.mark.xfail(reason='improve block parser')
def test_page_linealignment_master72_page15():
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.MASTER72,
        prefix='oneline',
    )
    left, right = words.lines.style.document_textfeed(navigators)
    page15 = navigators[15]
    linealignments = words.lines.style.page_linealignments(page15, left, right)
    assert linealignments[0] == words.lines.style.TextAlignment.BLOCK_CENTER
    assert linealignments[1] == words.lines.style.TextAlignment.BLOCK_CENTER
    assert linealignments[2] == words.lines.style.TextAlignment.BLOCK_CENTER

    assert linealignments[7] == words.lines.style.TextAlignment.BLOCK_CENTER
    assert linealignments[8] == words.lines.style.TextAlignment.BLOCK_CENTER
    assert linealignments[9] == words.lines.style.TextAlignment.BLOCK_CENTER
