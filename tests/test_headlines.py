# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import power
import pytest
import sections.path
import serializeraw
import utila
import utilatest

import tests.fixtures.headlines
import tests.fixtures.restruct
import tests.resources
import words.feature
import words.feature.headlines
import words.headlines
import words.headlines.nolevel
import words.loader.basic

# NOTE: WHAT SHOULD WE DO WITH THE RAW_LEVEL?
EXPECTED = [
    [
        iamraw.Headline(
            text='CHAPTER 1',
            level=1,
            rawlevel=None,
            container=0,
            page=6,
        ),
        iamraw.Headline(
            text='RestructuredText Tutorial',
            level=2,
            rawlevel=None,
            container=1,
            page=6,
        ),
    ],
    [
        iamraw.Headline(
            text='CHAPTER 2',
            level=1,
            rawlevel=None,
            container=0,
            page=8,
        ),
        iamraw.Headline(
            text='RestructuredText Guide',
            level=2,
            rawlevel=None,
            container=1,
            page=8,
        ),
        iamraw.Headline(
            text='Basics',
            level=3,
            rawlevel=None,
            container=2,
            page=8,
        ),
        iamraw.Headline(
            text='Blockquotes',
            level=3,
            rawlevel=None,
            container=1,
            page=9,
        ),
        iamraw.Headline(
            text='Code: Block',
            level=3,
            rawlevel=None,
            container=17,
            page=9,
        ),
    ],
]


@pytest.mark.xfail(reason='determining the level due text distance is a bad'
                   ' approach')
def test_headlines_extract_headlines():
    # TODO: Require new approach, may look into table of content
    section = tests.fixtures.restruct.restructured_sections_manual()
    basic = words.loader.basic.load_basic_frompath(power.link(power.DOCU27_PDF))
    extractor = words.headlines.nolevel.NoLevelHeadlineExtractor(
        sectionlist=section,
        basic=basic,
        chapters=[0, 1],
    )
    extracted = extractor.result()
    assert len(extracted) == len(EXPECTED)

    assert [len(item) for item in extracted] == [len(item) for item in EXPECTED]
    assert extracted == EXPECTED


def test_headlines_work():
    sections_ = tests.fixtures.restruct.restructured_sections()
    dumped = words.feature.headlines.work(
        boxes=iamraw.path.boxed(power.link(power.DOCU27_PDF)),
        font_content=iamraw.path.fontcontent(power.link(power.DOCU27_PDF)),
        font_header=iamraw.path.fontheader(power.link(power.DOCU27_PDF)),
        headerfooters=iamraw.path.headerfooters(power.link(power.DOCU27_PDF)),
        sectionlist=sections_,
        sizeandborder=iamraw.path.sizeandborder(power.link(power.DOCU27_PDF)),
        text=iamraw.path.text(power.link(power.DOCU27_PDF)),
        text_position=iamraw.path.textposition(power.link(power.DOCU27_PDF)),
    )
    # dump some headlines
    assert len(dumped) > 2100, str(dumped)


def test_headlines_dump_and_load_headlines():
    """Dump and load the example above"""
    dumped = serializeraw.dump_headlines(EXPECTED)
    loaded = serializeraw.load_headlines(dumped)

    assert loaded == EXPECTED


def extract_master72_headlines(root: str):
    master72 = power.link(power.MASTER072_PDF)
    sections_ = sections.path.sections_(master72)
    text = iamraw.path.text(master72)
    text_positions = iamraw.path.textposition(master72)
    font_header = iamraw.path.fontheader(master72)
    font_content = iamraw.path.fontcontent(master72)
    sizeandborder = iamraw.path.sizeandborder(master72)
    boxed = iamraw.path.boxed(master72)
    headerfooters = iamraw.path.headerfooters(master72)

    headlines = words.feature.headlines.work(
        sections_,
        text,
        text_positions,
        font_header,
        font_content,
        sizeandborder,
        boxes=boxed,
        headerfooters=headerfooters,
    )
    headlines_outpath = os.path.join(root, 'headlines_result.yaml')
    utila.file_create(headlines_outpath, headlines)

    assert len(headlines) > 400, str(headlines)
    result = serializeraw.load_headlines(headlines)

    return result


@utilatest.skip_longrun
def test_features_headlines_work_master72pages(testdir):
    root = str(testdir)
    headlines_loaded = extract_master72_headlines(root)

    # TODO: CHANGE AFTER SUPPORTING LITERATURVERZEICH AND ERKLARUNG
    assert len(headlines_loaded) == 5, str(headlines_loaded)

    expected_headlines = [
        '1. Einleitung',
        ('2. Das Social Web und die Privatsphäre – '
         'Selbstdarstellungsverhalten der Nutzer aus Sicht von '
         'Massenmedien und Literatur'),
        ('3. Systemtheorie und moderne Netzwerksoziologie – '
         'zentrale Ansätze und Begriffe für den Themen- '
         'komplex Social Media'),
        ('4. Privatheit und Identitätsbildung im Social Web – '
         'funktional betrachtet'),
        '5. Schlussbetrachtung und Fazit',
    ]
    # headlines of first element in section
    headlines_text = [item[0].text for item in headlines_loaded]
    assert headlines_text == expected_headlines, str(headlines_text)


def test_features_headlines_work_master72pages_subsections(testdir):
    root = str(testdir)
    headlines_loaded = extract_master72_headlines(root)
    expected_subsection_count = [2, 8, 10, 5, 0]

    subsections = [item[1:] for item in headlines_loaded]
    subsections_count = [len(item) for item in subsections]

    assert subsections_count == expected_subsection_count


def test_features_headlines_filter_headlines():
    example = tests.fixtures.headlines.EXAMPLE

    filtered = words.headlines.standard.filter_headlines(example)

    filtered = [item for item in filtered.values()]  # dict to list

    subsections = [item[1:] for item in filtered]
    subsections_count = [len(item) for item in subsections]
    expected_subsection_count = [2, 5, 7, 5, 2]

    assert subsections_count == expected_subsection_count
