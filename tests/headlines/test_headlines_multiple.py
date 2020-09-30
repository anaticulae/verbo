# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import sections.feature.section
import serializeraw
import utila
import utilatest

import words.headlines.multiline


@utilatest.skip_longrun
def test_headlines_multiple_master72_extract_pages_5_7():
    path = power.link(power.MASTER072_PDF)
    pages = utila.ranged_tuple(5, 7)
    headlines = parse_multiline(path, pages)

    expected = [
        ('1.2', 'Aufbau der Arbeit', 2),
        ('2.', ('Das Social Web und die Privatsphäre – '
                'Selbstdarstellungsverhalten der Nutzer aus Sicht von '
                'Massenmedien und Literatur'), 1),
        ('2.1', ('Web 2.0, Social Web und Social Media: Abgrenzungen und '
                 'Definitionen'), 2),
    ]
    assert headlines == expected


@utilatest.skip_longrun
def test_headlines_multiple_master72_extract_pages_13_14():
    path = power.link(power.MASTER072_PDF)
    pages = utila.ranged_tuple(13, 15)
    headlines = parse_multiline(path, pages)
    assert len(headlines) == 3
    expected = [
        ('2.4', 'Einführung in das Konzept der Privatheit', 2),
        ('2.5', 'Darstellungen in Massenmedien und Literatur', 2),
        ('2.5.1', 'Selbstdarstellung und Privatheit als Problemfelder', 3),
    ]
    assert headlines == expected


@utilatest.skip_longrun
def test_headlines_multiple_master72_extract_pages_20_22():
    """The headline extractor strategy extracts footnotes as headlines."""
    path = power.link(power.MASTER072_PDF)
    pages = utila.ranged_tuple(20, 23)
    headlines = parse_multiline(path, pages)
    assert len(headlines) == 2
    expected = [
        ('2.5.3', 'Privacy Paradox und Post-Privacy', 3),
        ('3.', ('Systemtheorie und moderne Netzwerksoziologie'
                ' – zentrale Ansätze und Begriffe für den Themen'
                '- komplex Social Media'), 1),
    ]
    assert headlines == expected


@utilatest.skip_longrun
def test_headlines_multiple_master72_extract_pages_38_42():
    """The headline extractor strategy extracts list with sentences."""
    path = power.link(power.MASTER072_PDF)
    pages = utila.ranged_tuple(38, 43)
    headlines = parse_multiline(path, pages)
    assert len(headlines) == 2
    expected = [
        ('3.6.2', 'Identitätsdimensionen', 3),
        ('3.6.3', 'Soziale Netzwerke beinhalten Stories', 3),
    ]
    assert headlines == expected


def parse_multiline(path: str, pages: tuple):
    chapters = None
    sections_ = sections.feature.section.load_section_likelihood_frompath(
        path,
        pages=pages,
    )
    loaded = serializeraw.create_pagetextcontentnavigators_frompath(
        path,
        pages=pages,
    )
    strategy = words.headlines.multiline.MultiLine(
        sectionlist=sections_,
        contentnavigators=loaded,
        chapters=chapters,
    )
    result = strategy.result(pages=pages)
    result = utila.flatten(result)
    headlines = [(item.raw_level, item.title, item.level) for item in result]
    return headlines
