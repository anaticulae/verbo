# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.path
import iamraw.path
import pytest
import sections.feature.section
import serializeraw
from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from iamraw import Document
from iamraw.sections import PERCENT_100
from iamraw.sections import Sections
from sections.creator import add_chapter
from sections.creator import add_content
from sections.creator import add_index
from sections.creator import add_introduction
from sections.creator import add_table
from sections.creator import add_text
from sections.creator import add_title
from sections.creator import add_toc
from sections.creator import add_whitepage
from sections.feature.chapter import work as chapter_work
from sections.feature.index import work as index_work
from sections.feature.legal import work as legal_work
from sections.feature.section import work as section_work
from sections.feature.title import work as title_work
from sections.feature.toc import work as toc_work
from sections.feature.whitepage import work as whitepage_work

import tests.fixtures
import tests.resources
import words.feature
import words.feature.boxed
import words.headlines
import words.loader.input
from words.feature.boxed import dump_boxedcontent
from words.feature.boxed import process_content as boxed_process_content
from words.feature.headlines import work as headlines_work
from words.feature.list import process as list_process
from words.text.chapter import extract_texts as text_extract_texts

RESTRUCT_BOXES = iamraw.path.boxed(tests.resources.RESTRUCT)
RESTRUCT_FONT_CONTENT = iamraw.path.fontcontent(tests.resources.RESTRUCT)
RESTRUCT_FONT_HEADER = iamraw.path.fontheader(tests.resources.RESTRUCT)
RESTRUCT_FOOTERS = iamraw.path.headerfooters(tests.resources.RESTRUCT)
RESTRUCT_HORIZONTAL = iamraw.path.horizontals(tests.resources.RESTRUCT)
RESTRUCT_ONELINE_FONT_CONTENT = iamraw.path.fontcontent(
    tests.resources.RESTRUCT,
    prefix='oneline',
)
RESTRUCT_ONELINE_FONT_HEADER = iamraw.path.fontheader(
    tests.resources.RESTRUCT,
    prefix='oneline',
)
RESTRUCT_ONELINE_TEXT = iamraw.path.text(
    tests.resources.RESTRUCT,
    prefix='oneline',
)
RESTRUCT_PAGESIZE = iamraw.path.sizeandborder(tests.resources.RESTRUCT)
RESTRUCT_TEXT = iamraw.path.text(tests.resources.RESTRUCT)
RESTRUCT_TEXT_POSITION = iamraw.path.textposition(tests.resources.RESTRUCT)
RESTRUCT_TOC = iamraw.path.toc(tests.resources.RESTRUCT)
RESTRUCT_PAGENUMBERS = groupme.path.pagenumbers(tests.resources.RESTRUCT)


@pytest.fixture
def restructured_chapter():
    result = chapter_work(RESTRUCT_TEXT, RESTRUCT_TEXT_POSITION, RESTRUCT_TOC)
    return result


@pytest.fixture
def restructured_text() -> Document:
    loaded = serializeraw.load_document(RESTRUCT_TEXT)
    return loaded


@pytest.fixture
def restructured_fontstore() -> FontStore:
    lookup = create_fontstore(RESTRUCT_FONT_HEADER, RESTRUCT_FONT_CONTENT)
    return lookup


def restructured_fontstore_fixture() -> FontStore:
    # TODO: Remove with new pytest - this is required, because pytest carn't
    # use pytest.fixture in paramertized tests.
    lookup = create_fontstore(RESTRUCT_FONT_HEADER, RESTRUCT_FONT_CONTENT)
    return lookup


@pytest.fixture
def restructured_pagenumbers():
    loaded = serializeraw.load_pagenumbers(RESTRUCT_PAGENUMBERS)
    return loaded


@pytest.fixture
def restructured_horizontals():
    loaded = serializeraw.load_horizontals(RESTRUCT_HORIZONTAL)
    return loaded


@pytest.fixture
def restructured_index():
    result = index_work(RESTRUCT_ONELINE_TEXT)
    return result


@pytest.fixture
def restructured_pagetextnavigators():
    navigators = tests.fixtures.create_pagetextnavigators(tests.resources.RESTRUCT) # yapf:disable
    return navigators


@pytest.fixture
def restructured_headlines():
    sections_ = restructured_sections()

    dumped = headlines_work(
        sections=sections_,
        text=RESTRUCT_TEXT,
        text_position=RESTRUCT_TEXT_POSITION,
        font_header=RESTRUCT_FONT_HEADER,
        font_content=RESTRUCT_FONT_CONTENT,
        sizeandborder=RESTRUCT_PAGESIZE,
        boxes=RESTRUCT_BOXES,
        headerfooters=RESTRUCT_FOOTERS,
    )
    return dumped


@pytest.fixture
def restructured_sections_manual() -> Sections:
    result = Sections()

    def analyse(section, start, end):
        return section(result, start, end, PERCENT_100)
        # TODO: reactivate [start, START] later
        # return section(result, [start, START], [end, END], PERCENT_100)

    def add_children(parent, ctor, start, end):
        # new = ctor(parent, [start, START], [end, END], PERCENT_100)
        new = ctor(parent, start, end, PERCENT_100)
        return new

    # Page, Start
    # Intro
    intro = analyse(add_introduction, 0, 1)
    add_children(intro, add_title, 0, 0)
    add_children(intro, add_whitepage, 1, 1)

    # First pages with tables
    table_first = analyse(add_table, 2, 5)
    add_children(table_first, add_toc, 2, 2)
    add_children(table_first, add_whitepage, 3, 3)
    add_children(table_first, add_text, 4, 4)
    add_children(table_first, add_whitepage, 5, 5)

    # Content starts here
    content = analyse(add_content, 6, 25)
    add_chapter(content, 6, 7, number=1)
    add_chapter(content, 8, 9, number=2)
    add_chapter(content, 10, 11, number=3)
    add_chapter(content, 12, 17, number=4)
    add_chapter(content, 18, 19, number=5)
    add_chapter(content, 20, 21, number=6)
    add_chapter(content, 22, 23, number=7)
    add_chapter(content, 24, 25, number=8)

    # Second pages with table
    table_second = analyse(add_table, 26, 26)
    add_children(table_second, add_index, 26, 26)

    return result


@pytest.fixture
def restructured_sizeandborder():
    loaded = serializeraw.load_pageborders(RESTRUCT_PAGESIZE)
    return loaded


@pytest.fixture
def restructured_text_positions():
    loaded = serializeraw.load_textpositions(RESTRUCT_TEXT_POSITION)
    return loaded


@pytest.fixture
def restructured_title():
    result = title_work(
        RESTRUCT_ONELINE_TEXT,
        RESTRUCT_ONELINE_FONT_HEADER,
        RESTRUCT_ONELINE_FONT_CONTENT,
    )
    return result


@pytest.fixture
def restructured_toc():
    result = toc_work(RESTRUCT_ONELINE_TEXT)
    return result


def restructured_text_fixture() -> Document:
    loaded = serializeraw.load_document(RESTRUCT_TEXT)
    return loaded


@pytest.fixture
def restructured_whitepage():
    result = whitepage_work(
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        footers=RESTRUCT_FOOTERS,
    )
    return result


def restructured_sections():
    extracted = sections.feature.section.extract_sections_frompath(
        tests.resources.RESTRUCT)
    dumped = serializeraw.dump_sections(extracted)
    return dumped


@pytest.fixture
def restructured_textexample(restructured_headlines):  # pylint:disable=W0621
    headlines = restructured_headlines
    loaded = words.feature.load_resources(
        text=RESTRUCT_TEXT,
        textposition=RESTRUCT_TEXT_POSITION,
        fontheader=RESTRUCT_FONT_HEADER,
        fontcontent=RESTRUCT_FONT_CONTENT,
        headlines=headlines,
        pagesizes=RESTRUCT_PAGESIZE,
        headerfooters=RESTRUCT_FOOTERS,
        boxes=RESTRUCT_BOXES,
    )
    extracted = text_extract_texts(loaded)
    assert extracted is not None
    return extracted


@pytest.fixture
def restructured_textexample_dumped(
        # pylint:disable=W0621
        restructured_textexample) -> str:
    return serializeraw.dump_text(restructured_textexample)


@pytest.fixture
def restructured_headerfooter():
    headerfooter = serializeraw.load_headerfooter(RESTRUCT_FOOTERS)
    return headerfooter


@pytest.fixture
def restructured_boxed(
        # pylint:disable=W0621
        restructured_textexample_dumped,
        restructured_headlines,
):
    headlines = restructured_headlines
    undefined = restructured_textexample_dumped
    extracted, _ = words.loader.input.load_resources(
        undefined,
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        border=RESTRUCT_PAGESIZE,
        headlines=headlines,
        headerfooters=RESTRUCT_FOOTERS,
    )
    boxes = serializeraw.load_boxes(RESTRUCT_BOXES)
    result = boxed_process_content(extracted, boxes)
    return result


@pytest.fixture
def restructured_boxed_dumped(
        # pylint:disable=W0621
        restructured_boxed) -> str:
    dumped = dump_boxedcontent(restructured_boxed)
    return dumped


@pytest.fixture
def restructured_contentborder(
        # pylint:disable=W0621
        restructured_headerfooter,
        restructured_sizeandborder,
):
    border = restructured_sizeandborder
    headerfooter = restructured_headerfooter
    result = words.headlines.contentborder(border, headerfooter)
    return result


@pytest.fixture
def restructured_list_work(
        # pylint:disable=W0621
        restructured_textexample_dumped,
        restructured_headlines,
):
    headlines = restructured_headlines
    undefined = restructured_textexample_dumped

    extracted, contentborder = words.loader.input.load_resources(
        undefined,
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        headlines=headlines,
        border=RESTRUCT_PAGESIZE,
        headerfooters=RESTRUCT_FOOTERS,
    )
    result = list_process(extracted, contentborder)
    return result


@pytest.fixture
def restructured_list_dumped(
        restructured_list_work,  # pylint:disable=W0621
) -> str:
    assert restructured_list_work
    result = restructured_list_work
    dumped = serializeraw.dump_lists(result)
    return dumped
