# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utilatest

import tests.fixtures.headlines
import tests.fixtures.restruct
import words.feature
import words.feature.headlines
import words.headlines
import words.headlines.nolevel
import words.loader.basic

# NOTE: WHAT SHOULD WE DO WITH THE RAW_LEVEL?
EXPECTED = [
    [
        iamraw.Headline(
            text='RestructuredText Tutorial',
            level=1,
            rawlevel=None,
            container=1,
            page=6,
        ),
    ],
    [
        iamraw.Headline(
            text='RestructuredText Guide',
            level=1,
            rawlevel=None,
            container=1,
            page=8,
        ),
        iamraw.Headline(
            text='Basics',
            level=2,
            rawlevel=None,
            container=2,
            page=8,
        ),
        iamraw.Headline(
            text='Blockquotes',
            level=2,
            rawlevel=None,
            container=1,
            page=9,
        ),
        iamraw.Headline(
            text='Code: Block',
            level=2,
            rawlevel=None,
            container=17,
            page=9,
        ),
    ],
]


def test_headlines_extract_headlines():
    section = tests.fixtures.restruct.restructured_sections_manual()
    basic = words.loader.basic.load_basic_frompath(power.link(power.DOCU27_PDF))
    extractor = words.headlines.nolevel.NoLevelHeadlineExtractor(
        sectionlist=section,
        basic=basic,
        chapters=[0, 1, 2, 3, 4, 5, 6, 7],
    )
    # check only the start, TODO: increase check later?
    extracted = extractor.result()[0:2]
    assert len(extracted) == len(EXPECTED)

    assert [len(item) for item in extracted] == [len(item) for item in EXPECTED]
    assert extracted == EXPECTED


def test_headlines_work():
    sections_ = tests.fixtures.restruct.restructured_sections()
    docu27 = power.link(power.DOCU27_PDF)
    dumped = words.feature.headlines.work(
        boxes=iamraw.path.boxed(docu27),
        font_content=iamraw.path.fontcontent(docu27),
        font_header=iamraw.path.fontheader(docu27),
        headerfooters=iamraw.path.headerfooters(docu27),
        sectionlist=sections_,
        sizeandborder=iamraw.path.sizeandborder(docu27),
        text=iamraw.path.text(docu27),
        text_position=iamraw.path.textposition(docu27),
    )
    # dump some headlines
    assert len(dumped) > 1740, str(dumped)


def test_headlines_dump_and_load_headlines():
    """Dump and load the example above"""
    dumped = serializeraw.dump_headlines(EXPECTED)
    loaded = serializeraw.load_headlines(dumped)

    assert loaded == EXPECTED


@utilatest.skip_longrun
def test_features_headlines_work_master72pages_headlines():
    master72 = power.link(power.MASTER072_PDF)
    headlines = words.feature.headlines.headlines_frompath(master72)

    # TODO: Adjust later, when it is possible to separate two appendix
    # headlines as single main headlines
    # Appendix does not have any main headline
    headlines = headlines[0:-1]

    # TODO: CHANGE AFTER SUPPORTING LITERATURVERZEICH AND ERKLARUNG
    assert len(headlines) == 5, str(headlines)

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
    headlines_text = [item[0].text for item in headlines]
    assert headlines_text == expected_headlines, str(headlines_text)


def test_features_headlines_work_master72pages_subsections():
    master72 = power.link(power.MASTER072_PDF)
    headlines = words.feature.headlines.headlines_frompath(master72)

    grouped, none_grouped = headlines[0:-1], headlines[-1]

    subsections = [item[1:] for item in grouped]
    subsections_count = [len(item) for item in subsections]

    expected_subsection_count = [2, 8, 10, 5, 0]
    assert subsections_count == expected_subsection_count

    # Literaturverzeichnis, Eidesstattliche Erklärung
    assert len(none_grouped) == 2


def test_features_headlines_filter_headlines():
    example = tests.fixtures.headlines.EXAMPLE

    filtered = words.headlines.standard.filter_headlines(example)

    filtered = [item for item in filtered.values()]  # dict to list

    subsections = [item[1:] for item in filtered]
    subsections_count = [len(item) for item in subsections]

    expected_subsection_count = [2, 5, 7, 5, 2]
    assert subsections_count == expected_subsection_count
