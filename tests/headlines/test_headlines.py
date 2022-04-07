# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import utila
import utilatest

import tests.fixtures.docu27
import tests.fixtures.headlines
import words.feature.headlines
import words.headlines.strategies


@utilatest.nightly
def test_headlines_work():
    sections_ = tests.fixtures.docu27.sections()
    src = power.link(power.DOCU027_PDF)
    normal, _ = words.feature.headlines.work(
        textx=iamraw.path.text(src),
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
    assert len(normal) > 1000, str(normal)


@utilatest.nightly
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


@utilatest.nightly
def test_features_headlines_work_master72pages_subsections():
    master72 = power.link(power.MASTER072_PDF)
    headlines = words.feature.headlines.headlines_frompath(master72)

    subsections = [item[1:] for item in headlines]
    subsections_count = [len(item) for item in subsections]

    # See: test_features_headlines_work_master72pages_headlines
    expected_subsection_count = [2, 8, 10, 5, 0, 0, 0]
    assert subsections_count == expected_subsection_count


def test_filter_headlines():
    example = tests.fixtures.headlines.EXAMPLE
    filtered = words.headlines.strategies.filter_headlines(example)
    filtered: list = list(filtered.values())  # dict to list
    # subsections
    subsections = [item[1:] for item in filtered]
    subsections_count = [len(item) for item in subsections]
    expected_subsection_count = [2, 5, 7, 5, 2]  # BETTER
    assert subsections_count == expected_subsection_count


@utilatest.nightly
def test_headlines_container_logical_indexing():
    """Ensure that headlines are parsed as logical headlines, this means
    that header and footer is ignored for determining the container id
    of headlines."""
    source = power.link(power.BACHELOR128_PDF)
    headlines = words.feature.headlines.headlines_frompath(source)
    headlines = utila.flatten(headlines)
    first = headlines[0]
    assert first.container == 0, first.container  # pylint:disable=C2001

    source = power.link(power.BACHELOR090_PDF)
    headlines = words.feature.headlines.headlines_frompath(source)
    headlines = utila.flatten(headlines)
    headline_system = headlines[5]
    assert headline_system.container == 1, headline_system.container


@utilatest.longrun
def test_headlines_master110page18():
    source = power.link(power.MASTER110_PDF)
    headlines = words.feature.headlines.headlines_frompath(
        source,
        pages=utila.rtuple(18, 20),
    )
    headlines = utila.flatten(headlines)
    first = headlines[0]
    # assert first.decoration is not None
    assert first.title == 'Einleitung'
    assert first.level == 1
