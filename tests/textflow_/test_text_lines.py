# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import textflow.alignment.style

TextAlignment = textflow.alignment.style.TextAlignment


def test_extract_linestyleinfo_master72():
    content_navigators = serializeraw.create_pagetextcontentnavigators_frompath(
        power.link(power.MASTER072_PDF), pages=(3,), prefix='oneline')
    left = 114.0
    right = 527.5
    linestyles = textflow.alignment.style.page_textalignment(
        content_navigators[0],
        left=left,
        right=right,
    )
    assert linestyles == TextAlignment.BLOCK, str(linestyles)


@pytest.mark.parametrize('source, expected', [
    pytest.param(
        power.link(power.MASTER072_PDF),
        TextAlignment.BLOCK,
        id='master72',
        marks=pytest.mark.xfail(reason='require improvement'),
    ),
    pytest.param(
        power.link(power.BACHELOR037_PDF),
        TextAlignment.BLOCK,
        id='bachelor37',
        marks=pytest.mark.xfail(reason='require improvement'),
    ),
    pytest.param(
        power.link(power.DOCU07_PDF),
        TextAlignment.BLOCK,
        id='pyporting',
        marks=pytest.mark.xfail(reason='require improvement'),
    ),
    pytest.param(
        power.link(power.HOMEWORK040_PDF),
        TextAlignment.LEFT,
        id='homework40',
    ),
])
@utilatest.skip_longrun
def test_document_alignment(source, expected):
    content_navigators = serializeraw.create_pagetextnavigators_frompath(
        source,
        prefix='oneline',
    )
    alignment = textflow.alignment.style.document_alignment(content_navigators)
    assert alignment == expected, alignment


@pytest.mark.xfail(reason='improve block parser')
def test_page_linealignment():
    navigators = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.HOMEWORK040_PDF),
        prefix='oneline',
    )
    left, right = textflow.alignment.style.document_textfeed(navigators)
    page4 = navigators[4]
    linealignments = textflow.alignment.style.page_linealignments(
        page4,
        left,
        right,
    )
    assert linealignments[0] == TextAlignment.CENTER
    assert linealignments[1] == TextAlignment.LEFT
    assert linealignments[-1] == TextAlignment.RIGHT


@pytest.mark.xfail(reason='broken alignment algo')
def test_page_linealignment_master72_page4():
    navigators = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.MASTER072_PDF),
        prefix='oneline',
    )
    left, right = textflow.alignment.style.document_textfeed(navigators)
    page4 = navigators[4]
    linealignments = textflow.alignment.style.page_linealignments(
        page4,
        left,
        right,
    )
    assert linealignments[0] == TextAlignment.BLOCK
    assert linealignments[2] == TextAlignment.LEFT
    assert linealignments[3] == TextAlignment.LEFT
    assert linealignments[4] == TextAlignment.BLOCK
    assert linealignments[-1] == TextAlignment.RIGHT


@pytest.mark.xfail(reason='improve block parser')
def test_page_linealignment_master72_page15():
    navigators = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.MASTER072_PDF),
        prefix='oneline',
    )
    left, right = textflow.alignment.style.document_textfeed(navigators)
    page15 = navigators[15]
    linealignments = textflow.alignment.style.page_linealignments(
        page15,
        left,
        right,
    )
    assert linealignments[0] == TextAlignment.BLOCK_CENTER
    assert linealignments[1] == TextAlignment.BLOCK_CENTER
    assert linealignments[2] == TextAlignment.BLOCK_CENTER

    assert linealignments[7] == TextAlignment.BLOCK_CENTER
    assert linealignments[8] == TextAlignment.BLOCK_CENTER
    assert linealignments[9] == TextAlignment.BLOCK_CENTER
