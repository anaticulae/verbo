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
import utila
import utilatest

import tests
import tests.fixtures.headlines
import tests.fixtures.restruct
import words.feature
import words.feature.headlines
import words.headlines
import words.headlines.nolevel
import words.headlines.strategies

# NOTE: WHAT SHOULD WE DO WITH THE RAW_LEVEL?
EXPECTED = [
    [
        iamraw.Headline(
            container=1,
            level=1,
            page=6,
            raw='RestructuredText Tutorial',
            raw_level=None,
            title='RestructuredText Tutorial',
        ),
    ],
    [
        iamraw.Headline(
            container=1,
            level=1,
            page=8,
            raw='RestructuredText Guide',
            raw_level=None,
            title='RestructuredText Guide',
        ),
        iamraw.Headline(
            container=2,
            level=2,
            page=8,
            raw='Basics',
            raw_level=None,
            title='Basics',
        ),
        iamraw.Headline(
            container=0,
            level=2,
            page=9,
            raw='Blockquotes',
            raw_level=None,
            title='Blockquotes',
        ),
        iamraw.Headline(
            container=16,
            level=2,
            page=9,
            raw='Code: Block',
            raw_level=None,
            title='Code: Block',
        ),
    ],
]


def test_headlines_extract_headlines():
    path = power.link(power.DOCU27_PDF)
    section = tests.fixtures.restruct.restructured_sections_manual()
    content = serializeraw.create_pagetextcontentnavigators_frompath(path)
    extractor = words.headlines.nolevel.NoLevelHeadlineExtractor(
        sectionlist=section,
        contentnavigators=content,
        chapters=[0, 1, 2, 3, 4, 5, 6, 7],
    )
    # check only the start, TODO: increase check later?
    extracted = extractor.result()[0:2]
    assert len(extracted) == len(EXPECTED)

    assert [len(item) for item in extracted] == [len(item) for item in EXPECTED]
    assert extracted == EXPECTED


def test_headlines_work():
    sections_ = tests.fixtures.restruct.restructured_sections()
    src = power.link(power.DOCU27_PDF)
    dumped, _ = words.feature.headlines.work(
        text=iamraw.path.text(src),
        text_position=iamraw.path.textposition(src),
        font_content=iamraw.path.fontcontent(src),
        font_header=iamraw.path.fontheader(src),
        oneline_text=iamraw.path.text(src, prefix='oneline'),
        oneline_text_position=iamraw.path.textposition(src, prefix='oneline'),
        oneline_font_content=iamraw.path.fontcontent(src, prefix='oneline'),
        oneline_font_header=iamraw.path.fontheader(src, prefix='oneline'),
        boxes=iamraw.path.boxed(src),
        headerfooters=iamraw.path.headerfooters(src),
        sectionlist=sections_,
        sizeandborder=iamraw.path.sizeandborder(src),
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
    expected_headlines = [
        ('1.', 'Einleitung'),
        ('2.', ('Das Social Web und die Privatsphäre – '
                'Selbstdarstellungsverhalten der Nutzer aus Sicht von '
                'Massenmedien und Literatur')),
        ('3.', ('Systemtheorie und moderne Netzwerksoziologie – '
                'zentrale Ansätze und Begriffe für den Themen- '
                'komplex Social Media')),
        ('4.', ('Privatheit und Identitätsbildung im Social Web – '
                'funktional betrachtet')),
        ('5.', 'Schlussbetrachtung und Fazit'),
        ('', 'Literaturverzeichnis'),
        ('', 'Eidesstattliche Erklärung'),
    ]
    # headlines of first element in section
    headlines_text = [(item[0].raw_level, item[0].title) for item in headlines]
    assert headlines_text == expected_headlines, str(headlines_text)


@utilatest.skip_longrun
def test_features_headlines_work_master72pages_subsections():
    master72 = power.link(power.MASTER072_PDF)
    headlines = words.feature.headlines.headlines_frompath(master72)

    subsections = [item[1:] for item in headlines]
    subsections_count = [len(item) for item in subsections]

    # See: test_features_headlines_work_master72pages_headlines
    expected_subsection_count = [2, 8, 10, 5, 0, 0, 0]
    assert subsections_count == expected_subsection_count


def test_features_headlines_filter_headlines():
    example = tests.fixtures.headlines.EXAMPLE

    filtered = words.headlines.strategies.filter_headlines(example)

    filtered = [item for item in filtered.values()]  # dict to list

    subsections = [item[1:] for item in filtered]
    subsections_count = [len(item) for item in subsections]

    expected_subsection_count = [2, 5, 7, 5, 2]
    assert subsections_count == expected_subsection_count


def test_headlines_container_logical_indexing():
    """Ensure that headlines are parsed as logical headlines, this means
    that header and footer is ignored for determining the container id
    of headlines."""
    source = power.link(power.BACHELOR128_PDF)
    headlines = words.feature.headlines.headlines_frompath(source)
    headlines = utila.flatten(headlines)
    first = headlines[0]
    assert first.container == 0, first.container

    source = power.link(power.BACHELOR090_PDF)
    headlines = words.feature.headlines.headlines_frompath(source)
    headlines = utila.flatten(headlines)
    headline_system = headlines[5]
    assert headline_system.container == 1, headline_system.container
