# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import serializeraw
import texmex
import utila

import tests.fixtures.restruct
import tests.resources
import words.feature
import words.feature.text
import words.headlines
import words.text
import words.undefined


def test_text_work():
    headlines = tests.fixtures.restruct.restructured_headlines()
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


def test_text_dump_and_load_text():
    headlines = tests.fixtures.restruct.restructured_headlines()
    textexample = tests.fixtures.restruct.restructured_textexample()
    assert textexample is not None
    assert headlines is not None
    headlines = serializeraw.load_headlines(headlines)
    dumped = serializeraw.dump_text(textexample)
    loaded = serializeraw.load_text(dumped, headlines)

    # TODO: REMOVE AFTER FIXING DUMP/LOAD
    loaded = [
        words.text.PageContentPageTextDetected(
            page=page,
            content=[
                words.text.TextSection(headline=headline, content=item)
                for headline, item in content
            ],
        )
        for page, content in loaded
    ]
    for first, second in zip(loaded, textexample):
        assert first == second, '\n\n%s\n%s\n\n\n' % (first, second)
    assert loaded == textexample


def test_text_extractor_titles():
    result = tests.fixtures.restruct.restructured_textexample()
    # page6
    page6 = utila.select_page(result, 6)
    assert page6.content[0].headline.text == 'CHAPTER 1'
    assert page6.content[1].headline.text == 'RestructuredText Tutorial'

    # page8
    page8 = utila.select_page(result, 8)
    assert page8.content[0].headline.text == 'CHAPTER 2'
    assert page8.content[1].headline.text == 'RestructuredText Guide'
    assert page8.content[2].headline.text == 'Basics'

    # page9
    page9 = utila.select_page(result, 9)
    assert page9.content[0].headline.text == 'Blockquotes'
    assert page9.content[1].headline.text == 'Code: Block'

    # page10
    page10 = utila.select_page(result, 10)
    assert page10.content[0].headline.text == 'CHAPTER 3'
    assert page10.content[1].headline.text == 'RestructuredText Customizations'

    # page12
    page12 = utila.select_page(result, 12)
    assert page12.content[0].headline.text == 'CHAPTER 4'
    assert page12.content[1].headline.text == 'Sphinx Tutorial'
    assert page12.content[2].headline.text == 'Step 1'

    # page13
    # is merged to page12

    # page14
    page14 = utila.select_page(result, 14)
    assert page14.content[0].headline.text == 'Documenting a Project'

    # page15
    page15 = utila.select_page(result, 15)
    assert page15.content[0].headline.text == 'Aside: Other formats'

    # page16
    page16 = utila.select_page(result, 16)
    assert page16.content[0].headline.text == 'Step 2'
    assert not page16.content[0].content  # headline only, no content
    assert page16.content[1].headline.text == 'Referencing Code'

    # page17
    # is merged to page 16

    # page18
    page18 = utila.select_page(result, 18)
    assert page18.content[0].headline.text == 'CHAPTER 5'
    assert page18.content[1].headline.text == 'Sphinx Guide'


@pytest.mark.xfail(reason='unable to merge undefined sections correctly')
def test_text_convert_undefined_to_text():
    """Test to replace undefined `uindex` on last page."""
    headlines = tests.fixtures.restruct.restructured_headlines()
    textexample = tests.fixtures.restruct.restructured_textexample()

    text = iamraw.path.text(tests.resources.RESTRUCT)
    text = serializeraw.load_document(text)

    textpositions = iamraw.path.textposition(tests.resources.RESTRUCT)
    textpositions = serializeraw.load_textpositions(textpositions)

    border = iamraw.path.sizeandborder(tests.resources.RESTRUCT)
    border = serializeraw.load_pageborders(border)

    headerfooters = iamraw.path.headerfooters(tests.resources.RESTRUCT)
    headerfooters = serializeraw.load_headerfooter(headerfooters)

    contentborder = words.headlines.contentborder(border, headerfooters)
    assert textexample is not None
    assert headlines is not None
    headlines = serializeraw.load_headlines(headlines)

    dumped = serializeraw.dump_text(textexample)
    loaded = serializeraw.load_text(dumped, headlines)

    undefined = words.undefined.extract_undefined(
        loaded,
        text,
        textpositions,
        contentborder=contentborder,
    )

    last_item = undefined[-1]
    text = [item.text.strip() for item in last_item[0][2][0][0][1]]
    expected = [
        '• genindex',
        '• modindex',
        '• search',
    ]
    assert text == expected, str(text)
