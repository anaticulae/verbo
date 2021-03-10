# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utila
import utilatest

import tests.fixtures.restruct
import tests.resources
import words.feature
import words.feature.text
import words.headlines
import words.path
import words.text
import words.undefined


def test_text_work():
    headlines = tests.fixtures.restruct.restructured_headlines()
    result = words.feature.text.work(
        boxes=iamraw.path.boxed(power.link(power.DOCU27_PDF)),
        lists=words.path.lists(power.link(power.DOCU27_PDF)),
        fontcontent=iamraw.path.fontcontent(power.link(power.DOCU27_PDF)),
        fontheader=iamraw.path.fontheader(power.link(power.DOCU27_PDF)),
        headerfooters=iamraw.path.headerfooters(power.link(power.DOCU27_PDF)),
        headlines=headlines,
        pagesizes=iamraw.path.sizeandborder(power.link(power.DOCU27_PDF)),
        text=iamraw.path.text(power.link(power.DOCU27_PDF)),
        textposition=iamraw.path.textposition(power.link(power.DOCU27_PDF)),
    )
    assert len(result) > 6000, str(result)


def test_text_extractor_titles():
    result = tests.fixtures.restruct.restructured_textexample(
        require_headlinelevel=
        False,  # TODO: SET TO TRUE TO IMPROVE HEADLINE PARSER
    )

    # page6
    page6 = utila.select_page(result, 6)
    # assert page6.content[0].headline.title is None
    assert page6.content[0].headline.title == 'RestructuredText Tutorial'

    # page8
    page8 = utila.select_page(result, 8)
    assert page8.content[1].headline.title == 'RestructuredText Guide'
    assert page8.content[2].headline.title == 'Basics'

    # page9
    page9 = utila.select_page(result, 9)
    assert page9.content[0].headline.title == 'Blockquotes'
    assert page9.content[1].headline.title == 'Code: Block'

    # page10
    page10 = utila.select_page(result, 10)
    assert page10.content[0].headline.title == 'RestructuredText Customizations'

    # page12
    page12 = utila.select_page(result, 12)
    assert page12.content[0].headline.title is None
    assert page12.content[1].headline.title == 'Sphinx Tutorial'
    assert page12.content[2].headline.title == 'Step 1'

    # page13
    # is merged to page12

    # page14
    page14 = utila.select_page(result, 14)
    assert page14.content[0].headline.title == 'Documenting a Project'

    # page15
    page15 = utila.select_page(result, 15)
    assert page15.content[0].headline.title is None
    assert page15.content[1].headline.title == 'Aside: Other formats'

    # page16
    page16 = utila.select_page(result, 16)
    assert page16.content[1].headline.title == 'Step 2'
    assert not page16.content[1].content  # headline only, no content
    assert page16.content[2].headline.title == 'Referencing Code'

    # page17
    # is merged to page 16

    # page18
    page18 = utila.select_page(result, 18)
    assert page18.content[1].headline.title == 'Sphinx Guide'


@utilatest.longrun
def test_text_convert_undefined_to_text():
    """Test to replace undefined `uindex` on last page."""
    headlines = tests.fixtures.restruct.restructured_headlines()
    textexample = tests.fixtures.restruct.restructured_textexample()

    headlines = serializeraw.load_headlines(headlines)
    dumped = serializeraw.dump_text(textexample)
    loaded = serializeraw.load_text(dumped, headlines)

    source = power.link(power.DOCU27_PDF)
    ptcns = serializeraw.create_pagetextcontentnavigators_frompath(source)

    undefined = words.undefined.extract_undefined(loaded, ptcns)

    last_item = undefined[-1]
    text = [item.text.strip() for item in last_item[0][2][0][0][1]]
    expected = [
        '• genindex',
        '• modindex',
        '• search',
    ]
    assert text == expected, str(text)
