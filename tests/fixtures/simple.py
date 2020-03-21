# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hey.fonts.store
import iamraw
import pytest
import sections.feature.chapter
import sections.feature.index
import sections.feature.section
import sections.feature.title
import sections.feature.toc
import sections.feature.whitepage
import serializeraw
import texmex
import utila

import tests
import tests.fixtures
import tests.resources

SIMPLE_PAGESIZE = iamraw.path.sizeandborder(tests.resources.HOWTO_PYPORTING)
SIMPLE_HORIZONTAL = iamraw.path.horizontals(tests.resources.HOWTO_PYPORTING)
SIMPLE_TEXT_POSITION = iamraw.path.textposition(tests.resources.HOWTO_PYPORTING)
SIMPLE_TEXT = iamraw.path.text(tests.resources.HOWTO_PYPORTING)
SIMPLE_ONELINE_TEXT = iamraw.path.text(
    tests.resources.HOWTO_PYPORTING,
    prefix='oneline',
)
SIMPLE_ONELINE_FONT_HEADER = iamraw.path.fontheader(
    tests.resources.HOWTO_PYPORTING,
    prefix='oneline',
)
SIMPLE_ONELINE_FONT_CONTENT = iamraw.path.fontcontent(
    tests.resources.HOWTO_PYPORTING,
    prefix='oneline',
)
SIMPLE_FONT_HEADER = iamraw.path.fontheader(tests.resources.HOWTO_PYPORTING)
SIMPLE_FONT_CONTENT = iamraw.path.fontcontent(tests.resources.HOWTO_PYPORTING)
SIMPLE_FOOTER = iamraw.path.headerfooters(tests.resources.HOWTO_PYPORTING)
SIMPLE_TOC = iamraw.path.toc(tests.resources.HOWTO_PYPORTING)
SIMPLE_FOOTERS = iamraw.path.headerfooters(tests.resources.HOWTO_PYPORTING)


@pytest.fixture
def simple():
    pagesize = serializeraw.load_pageborders(SIMPLE_PAGESIZE)
    horizontals = serializeraw.load_horizontals(SIMPLE_HORIZONTAL) # yapf:disable
    position = serializeraw.load_textpositions(SIMPLE_TEXT_POSITION) # yapf:disable
    document = serializeraw.load_document(SIMPLE_TEXT)

    assert pagesize
    assert horizontals
    assert position

    navigator = texmex.create_pagetextnavigators(
        text=document,
        text_positions=position,
    )
    return navigator, horizontals


@pytest.fixture
def simple_document() -> iamraw.Document:
    loaded = serializeraw.load_document(SIMPLE_ONELINE_TEXT)
    return loaded


def simple_document_fixture() -> iamraw.Document:
    loaded = serializeraw.load_document(SIMPLE_TEXT)
    return loaded


def simple_fontstore_fixture() -> hey.fonts.store.FontStore:
    lookup = hey.fonts.store.create_fontstore(
        SIMPLE_FONT_HEADER,
        SIMPLE_FONT_CONTENT,
    )
    return lookup


@pytest.fixture
def simple_fontstore() -> hey.fonts.store.FontStore:
    lookup = hey.fonts.store.create_fontstore(
        SIMPLE_FONT_HEADER,
        SIMPLE_FONT_CONTENT,
    )
    return lookup


@pytest.fixture
def simple_navigator(simple):  #pylint:disable=W0621
    navigator, _ = simple
    return navigator


@pytest.fixture
def simple_pagetextnavigators() -> texmex.PageTextNavigators:  # yapf:disable
    navigator = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.HOWTO_PYPORTING)
    return navigator


@pytest.fixture
def simple_pagesize():
    size = serializeraw.load_pageborders(SIMPLE_PAGESIZE)
    size = [item.size for item in size]
    return size


@pytest.fixture
def simple_contentborder():
    border = serializeraw.load_pageborders(SIMPLE_PAGESIZE)
    border = [item.border for item in border]
    return border


@pytest.fixture
def simple_page_0(simple_document: iamraw.Document) -> iamraw.Page:  # pylint: disable=W0621
    page: iamraw.Page = simple_document[0]
    return page


@pytest.fixture
def simple_page_2(simple_document: iamraw.Document) -> iamraw.Page:  # pylint: disable=W0621
    page: iamraw.Page = simple_document[2]
    return page


@pytest.fixture
def simple_page_2_text_only(simple_page_2: iamraw.Page):  # pylint: disable=W0621
    lines = []
    for child in simple_page_2:
        if not isinstance(child, iamraw.TextContainer):
            continue
        lines.extend(child.text.splitlines())
    return lines


# TODO: Reduce amout of fixtures
@pytest.fixture
def simple_second_page_navigator(
        simple_pagetextnavigators,  # pylint:disable=W0621
) -> texmex.PageTextNavigator:
    return utila.select_page(simple_pagetextnavigators, page=1)


@pytest.fixture
def simple_second_page_size(simple_contentborder) -> iamraw.Border:  # pylint:disable=W0621
    return simple_contentborder[1]


@pytest.fixture
def simple_toc():
    result = sections.feature.toc.work(SIMPLE_ONELINE_TEXT)
    return result


@pytest.fixture
def simple_whitepage():
    result = sections.feature.whitepage.work(
        SIMPLE_TEXT,
        SIMPLE_TEXT_POSITION,
        SIMPLE_FOOTERS,
    )
    return result


@pytest.fixture
def simple_title():
    result = sections.feature.title.work(
        SIMPLE_ONELINE_TEXT,
        SIMPLE_ONELINE_FONT_HEADER,
        SIMPLE_ONELINE_FONT_CONTENT,
    )
    return result


@pytest.fixture
def simple_index():
    result = sections.feature.index.work(SIMPLE_ONELINE_TEXT)
    return result


@pytest.fixture
def simple_chapter():
    result = sections.feature.chapter.work(
        SIMPLE_TEXT,
        SIMPLE_TEXT_POSITION,
        SIMPLE_TOC,
    )

    # ensure that all chapters are detected
    tests.fixtures.assert_chapter_count(
        serializeraw.load_likelihood(result),
        tests.resources.HOWTO_PYPORTING_CHAPTER_PAGE_COUNT,
    )
    return result


@pytest.fixture
def simple_sections():
    result = sections.feature.section.extract_sections_frompath(
        tests.resources.HOWTO_PYPORTING)
    return result
