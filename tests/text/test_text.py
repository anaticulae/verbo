# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import texmex

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
    # is merged to page12

    # page14
    assert result[5][1][0][0].text == 'Documenting a Project'

    # page15
    assert result[6].content[0].headline.text == 'Aside: Other formats'

    # page16
    assert result[7].content[0].headline.text == 'Step 2'
    assert not result[7].content[0].content  # headline only, no content
    assert result[7].content[1].headline.text == 'Referencing Code'

    # page17
    # is merged to page 16

    # page18
    assert result[8].content[0].headline.text == 'CHAPTER 5'
    assert result[8].content[1].headline.text == 'Sphinx Guide'


def test_text_convert_undefined_to_text():
    headlines = tests.fixtures.restruct.restructured_headlines()
    textexample = tests.fixtures.restruct.restructured_textexample()
    text = serializeraw.load_document(
        iamraw.path.text(tests.resources.RESTRUCT))
    text_positions = serializeraw.load_textpositions(
        iamraw.path.textposition(tests.resources.RESTRUCT))

    border = serializeraw.load_pageborders(
        iamraw.path.sizeandborder(tests.resources.RESTRUCT))
    headerfooters = serializeraw.load_headerfooter(
        iamraw.path.headerfooters(tests.resources.RESTRUCT))

    contentborder = words.headlines.contentborder(border, headerfooters)
    assert textexample is not None
    assert headlines is not None
    headlines = serializeraw.load_headlines(headlines)

    dumped = serializeraw.dump_text(textexample)
    loaded = serializeraw.load_text(dumped, headlines)

    undefined = words.undefined.extract_undefined(
        loaded,
        text,
        text_positions,
        contentborder=contentborder,
    )

    expected_list = [
        texmex.TextInfo(
            bounding=iamraw.BoundingBox(
                x0=88.44, y0=332.13, x1=133.28, y1=344.14),
            bounding_mean=12.01,
            text='• genindex',
            style=texmex.TextStyle.create(start=0, end=11, size=9.96),
        ),
        texmex.TextInfo(
            bounding=iamraw.BoundingBox(
                x0=88.44, y0=350.07, x1=136.61, y1=362.07),
            bounding_mean=12.0,
            text='• modindex',
            style=texmex.TextStyle.create(start=0, end=11, size=9.96),
        ),
        texmex.TextInfo(
            bounding=iamraw.BoundingBox(
                x0=88.44, y0=368.00, x1=122.35, y1=380.00),
            bounding_mean=12.0,
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
    text = [item.text.strip() for item in last_item[0][2][0][0][1]]
    expected = [
        '• genindex',
        '• modindex',
        '• search',
    ]
    assert text == expected, str(text)
