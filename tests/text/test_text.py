# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import hey.undefined
import iamraw
import pytest
import serializeraw
import texmex
import utila

import tests.resources
import words.feature
import words.feature.text
import words.text.chapter as wtc
# pylint:disable=W0611
# pylint:disable=ungrouped-imports
from tests.fixtures.restruct import restructured_contentborder
from tests.fixtures.restruct import restructured_headerfooter
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_pagenumbers
from tests.fixtures.restruct import restructured_sizeandborder
from tests.fixtures.restruct import restructured_text
from tests.fixtures.restruct import restructured_text_positions
from tests.fixtures.restruct import restructured_textexample


def test_text_work(
        restructured_headlines,  # pylint:disable=W0621
):
    headlines = restructured_headlines
    result = words.feature.text.work(
        boxes=iamraw.path.boxed(tests.resources.RESTRUCT),
        fontcontent=iamraw.path.fontcontent(tests.resources.RESTRUCT),
        fontheader=iamraw.path.fontheader(tests.resources.RESTRUCT),
        headerfooters=iamraw.path.headerfooters(tests.resources.RESTRUCT),
        headlines=headlines,
        pagesizes=iamraw.path.sizeandborder(tests.resources.RESTRUCT),
        text=iamraw.path.text(tests.resources.RESTRUCT),
        textposition=iamraw.path.textposition(tests.resources.RESTRUCT),
    )
    assert len(result) > 6000, str(result)


def test_text_dump_and_load_text(
        restructured_headlines,  # pylint:disable=W0621
        restructured_textexample,  # pylint:disable=W0621
):
    headlines = restructured_headlines
    textexample = restructured_textexample
    assert textexample is not None
    assert headlines is not None
    headlines = serializeraw.load_headlines(headlines)

    dumped = serializeraw.dump_text(restructured_textexample)
    loaded = serializeraw.load_text(dumped, headlines)

    for first, second in zip(loaded, textexample):
        assert first == second, '\n\n%s\n%s\n\n\n' % (first, second)
    assert loaded == textexample


def test_text_extractor_titles(
        restructured_textexample,  # pylint:disable=W0621
):
    result = restructured_textexample
    # page6
    assert result[0][1][0][0].text == 'CHAPTER 1'
    assert result[0][1][1][0].text == 'RestructuredText Tutorial'

    # page8
    assert result[1][1][0][0].text == 'CHAPTER 2'
    assert result[1][1][1][0].text == 'RestructuredText Guide'
    assert result[1][1][2][0].text == 'Basics'

    # page9
    assert result[2][1][0][0].text == 'Blockquotes'
    assert result[2][1][1][0].text == 'Code: Block'

    # page10
    assert result[3][1][0][0].text == 'CHAPTER 3'
    assert result[3][1][1][0].text == 'RestructuredText Customizations'

    # page12
    assert result[4][1][0][0].text == 'CHAPTER 4'
    assert result[4][1][1][0].text == 'Sphinx Tutorial'
    assert result[4][1][2][0].text == 'Step 1'

    # page13
    assert result[5][1][0][0].text is None

    # page14
    assert result[6][1][0][0].text == 'Documenting a Project'

    #page15
    assert result[7][1][0][0].text is None
    assert result[7][1][1][0].text == 'Aside: Other formats'

    #page16
    assert result[8][1][0][0].text is None
    assert result[8][1][1][0].text == 'Step 2'
    assert result[8][1][2][0].text == 'Referencing Code'

    #page17
    assert result[9][1][0][0].text is None

    #page18
    assert result[10][1][0][0].text == 'CHAPTER 5'
    assert result[10][1][1][0].text == 'Sphinx Guide'


@pytest.mark.parametrize(
    'current_page,current_headline,expected_start,expected_end',
    [
        pytest.param(
            8,
            2,
            ([]),  # no content after headline
            ('u19'),
            id='page8',
        ),
        pytest.param(
            13,
            7,
            ('Getting Started'),
            ('make html is the main way you will '
             'build HTML documentation locally. It is simply a wrapper '
             'around a more complex call to Sphinx.'),
            id='page13',
            marks=pytest.mark.xfail(reason='dont know why'),
        ),
        pytest.param(
            14,
            8,
            ('Now that we have our basic skeleton, let’s document the project. '
             'As you might have guessed from the name, we’ll be documenting a'
             ' basic web crawler.'),
            ('Include the following in your install.rst:'),
            id='page14',
            marks=pytest.mark.xfail(reason='require selective approach'),
        ),
        pytest.param(
            15,
            9,
            ('u0'),
            (None),
            id='page15',
        ),
        pytest.param(
            16,
            10,
            ('Make a manpage'),
            ('u21'),
            id='page16',
            marks=pytest.mark.xfail(reason='dont know why'),
        ),
    ])
def test_extract_texts_page_x(  # pylint:disable=too-many-locals
        current_page,
        current_headline,
        expected_start,
        expected_end,
        restructured_headlines,  # pylint:disable=W0621
):
    headlines = restructured_headlines
    loaded = words.feature.load_resources(
        boxes=iamraw.path.boxed(tests.resources.RESTRUCT),
        fontcontent=iamraw.path.fontcontent(tests.resources.RESTRUCT),
        fontheader=iamraw.path.fontheader(tests.resources.RESTRUCT),
        headerfooters=iamraw.path.headerfooters(tests.resources.RESTRUCT),
        headlines=headlines,
        pagesizes=iamraw.path.sizeandborder(tests.resources.RESTRUCT),
        text=iamraw.path.text(tests.resources.RESTRUCT),
        textposition=iamraw.path.textposition(tests.resources.RESTRUCT),
    )

    def join_output(paragraph):
        try:
            joined = ''.join([item for (item, _) in paragraph.content])
            return joined.replace(utila.NEWLINE, ' ')
        except TypeError:
            return 'u%d' % paragraph.container

    # fill headlines
    pages = [item.page for item in loaded.textnavigators]
    headlines = wtc.insert_empty_pages(loaded.headlines, maxpage=max(pages))
    # ensure that all collect headlines are from page `current_page`
    current = headlines[current_headline]
    assert all([item.page == current_page for item in current])

    analyzed = wtc.analyze_page(
        current,
        loaded.fontstore,
        loaded.textnavigators,
        loaded.border,
        loaded.boxes,
    )
    page, content = analyzed.page, analyzed.content
    assert page == current_page, 'wrong extracted page: %d' % page

    first_headline, first_output = content[0][0], content[0][1]  # pylint:disable=E1136
    last_headline, last_output = content[-1][0], content[-1][1]  # pylint:disable=E1136
    # msg = 'invalid returned value due `analyze_page`'
    # assert headline.text == current[0].text, '%s\n%s' % (msg, output)
    assert first_headline.page == current_page
    assert last_headline.page == current_page

    if expected_start == []:
        # empty content on Headlines without content is possible
        assert first_output == expected_start
    else:
        assert first_output, str(first_output)
        first_line = join_output(first_output[0])
        assert first_line == expected_start
    last_line = join_output(last_output[-1]) if last_output else None
    assert last_line == expected_end


def test_text_convert_undefined_to_text(  # pylint:disable=R0914
        restructured_headlines,  # pylint:disable=W0621
        restructured_textexample,  # pylint:disable=W0621
        restructured_text,  # pylint:disable=W0621
        restructured_text_positions,  # pylint:disable=W0621
        restructured_contentborder,  # pylint:disable=W0621
):
    headlines = restructured_headlines
    textexample = restructured_textexample
    text = restructured_text
    text_positions = restructured_text_positions
    contentborder = restructured_contentborder
    assert textexample is not None
    assert headlines is not None
    headlines = serializeraw.load_headlines(headlines)

    dumped = serializeraw.dump_text(restructured_textexample)
    loaded = serializeraw.load_text(dumped, headlines)

    undefined = hey.undefined.extract_undefined(
        loaded,
        text,
        text_positions,
        contentborder=contentborder,
    )

    expected_list = [
        texmex.TextInfo(
            bounding=iamraw.BoundingBox(
                x0=88.44, y0=332.13, x1=133.28, y1=344.13),
            text='• genindex',
            style=texmex.TextStyle.create(start=0, end=11, size=9.96),
        ),
        texmex.TextInfo(
            bounding=iamraw.BoundingBox(
                x0=88.44, y0=350.07, x1=136.61, y1=362.07),
            text='• modindex',
            style=texmex.TextStyle.create(start=0, end=11, size=9.96),
        ),
        texmex.TextInfo(
            bounding=iamraw.BoundingBox(
                x0=88.44, y0=368.00, x1=122.35, y1=380.00),
            text='• search',
            style=texmex.TextStyle.create(start=0, end=9, size=9.96),
        ),
    ]
    expected = [
        (
            24,
            1,
            (
                [(0, expected_list)],
                [[2, 3, 4]],
            ),
        ),
    ]
    last_item = undefined[-1]
    # TODO: REMOVE LATER?
    for item in last_item[0][2][0][0][1]:
        item.text = item.text.strip()
    assert last_item == expected
