# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest

import docref.bibliography.strategies.intext as ll

BibRef = iamraw.BibliographyReference

TEXT = """
(vgl. Abels 2010: 94ff.).
(vgl. ebd.: 85).
(vgl. ebd.: 161ff.).
(vgl. Mead 1973: 300).
(Kettner 2004: 222)
(vgl. Havelock 1986: 77; Robinson/Hawpe 1986: 124)
(ebd.: 18; vgl. hierzu auch Havelock 1963: 47)
(vgl. Plat. Men.: 97a-98c).
(vgl. ebd.: 6; Havelock 1982: 186; Murray/Wilson 2004: 1)
(vgl. Dierse 1977: 2-6).
(Meier 2007: 192).
(vgl. McQuail 2010: 467; Schenk 2007: 41; Perse 2001: 3).
(vgl. Bonfadelli 2004: 33)
Luhmann (2005a)
""".splitlines()[1:]

INLINE = """
ästhetische Inhalte beliebig oft zu reproduzieren (vgl. Benjamin 1939), sondern auch
Konsens (vgl. McQuail 2010: 454). Auch ist der eindeutige Nachweis von Medienef
Vordergrund (vgl. McQuail 2010: 456-459). Der rezipientenorientierte Ansatz in der
ierten Realität sinnhaft aneignet (vgl. McQuail 2010: 459). Die sinnliche Erfassung und
tens (vgl. McQuail 2010: 467; Schenk 2007: 41; Perse 2001: 3). Obgleich sich die psy
sens ausgeweitet (vgl. Dierse 1977: 2-6).
"""

FOOTER = """
^143 s. Luhmann 1995: 144f.
^144 ebd.: 153
^145 s. Luhmann 1994: 429
"""


@pytest.mark.parametrize('line, expected', [
    (
        '(vgl. Abels 2010: 94ff.).',
        BibRef(authors=['Abels'], year=2010, page='94ff.'),
    ),
    (
        '(vgl. ebd.: 85).',
        BibRef(authors=['ebd.'], year=None, page='85'),
    ),
    (
        '(vgl. ebd.: 161ff.).',
        BibRef(authors=['ebd.'], year=None, page='161ff.'),
    ),
    (
        '(vgl. Mead 1973: 300).',
        BibRef(authors=['Mead'], year=1973, page='300'),
    ),
    (
        '(Kettner 2004: 222)',
        BibRef(authors=['Kettner'], year=2004, page='222'),
    ),
    (
        '(vgl. Havelock 1986: 77; Robinson/Hawpe 1986: 124)',
        [
            BibRef(authors=['Havelock'], year=1986, page='77'),
            BibRef(authors=['Robinson/Hawpe'], year=1986, page='124'),
        ],
    ),
    (
        '(ebd.: 18; vgl. hierzu auch Havelock 1963: 47)',
        [
            BibRef(authors=['ebd.'], year=None, page='18'),
            BibRef(authors=['hierzu auch Havelock'], year=1963, page='47'),
        ],
    ),
    (
        '(vgl. Plat. Men.: 97a-98c).',
        BibRef(
            authors=['Plat. Men.'],
            year=None,
            page='97a-98c',
        ),
    ),
    (
        '(vgl. ebd.: 6; Havelock 1982: 186; Murray/Wilson 2004: 1)',
        [
            BibRef(authors=['ebd.'], year=None, page='6'),
            BibRef(authors=['Havelock'], year=1982, page='186'),
            BibRef(authors=['Murray/Wilson'], year=2004, page='1'),
        ],
    ),
    (
        '(vgl. Dierse 1977: 2-6).',
        BibRef(authors=['Dierse'], year=1977, page='2-6'),
    ),
    (
        '(Meier 2007: 192).',
        BibRef(authors=['Meier'], year=2007, page='192'),
    ),
    (
        '(vgl. McQuail 2010: 467; Schenk 2007: 41; Perse 2001: 3).',
        [
            BibRef(authors=['McQuail'], year=2010, page='467'),
            BibRef(authors=['Schenk'], year=2007, page='41'),
            BibRef(authors=['Perse'], year=2001, page='3'),
        ],
    ),
    (
        '(vgl. Bonfadelli 2004: 33)',
        BibRef(authors=['Bonfadelli'], year=2004, page='33'),
    ),
])
def test_parse_bibliographylink(line, expected):
    # (
    #         'Luhmann (2005a)',
    #     BibRef(authors=['Luhmann', year=2005, page='192'),
    # ),
    if not isinstance(expected, list):
        expected = [expected]
    parsed = ll.parse(line)
    assert parsed == expected


def test_parse_bibliographylink_in_text():
    expected = [
        BibRef(authors=['McQuail'], year=2010, page='454'),
        BibRef(authors=['McQuail'], year=2010, page='456-459'),
        BibRef(authors=['McQuail'], year=2010, page='459'),
        BibRef(authors=['McQuail'], year=2010, page='467'),
        BibRef(authors=['Schenk'], year=2007, page='41'),
        BibRef(authors=['Perse'], year=2001, page='3'),
        BibRef(authors=['Dierse'], year=1977, page='2-6'),
        # TODO: FIX ORDER AFTER MERGING DIFFERENT REGEX PATTERN
        BibRef(authors=['Benjamin'], year=1939),
    ]
    parsed = ll.parse(INLINE)
    assert parsed == expected


RAW = """\
Das Stadtgebiet von Neunkirchen war schon in keltischer Zeit besiedelt
wovon Grabstätten in den Stadtteilen Mühlfeld und Steinfeld Zeugnis
ablegen. Nach dem Einmarsch der Römer errichteten sie anstelle der
Keltenburg ein steinernes Kastellum sowie Wohn- und Wirtschaftsgebäude
rund um den Holz- und Hauptplatz – hiervon zeugen Funde von römischen
Grabsteinen und Münzen (vgl. Arbeitsgemeinschaft 900 Jahre Neunkirchen,
S. 50).

Im Jahre 872 soll nach Schweickhadt, Ritter von Sickingen, die
heutige Pfarrkirche erbaut worden sein, hierfür gibt es aber weder
Beweise durch Inschriften noch durch schriftliche Quellen, 1036 wurde
die Siedlung durch König Konrad II. zum Markt erhoben, 1136 wurde das
Münzrecht verliehen und 1139 von Papst Innozenz II. bestätigt. Die erste
urkundliche Erwähnung geht auf das Jahr 1094 zurück wo Neunkirchen als
„Niuwenchirgun“, als „Neue Kirche“, bezeichnet wird (vgl. BOUS (1933),
S. 3 ff).
"""


@pytest.mark.xfail(reason='wait for nltk')
def test_parse_biblink_fulltext():
    parsed = ll.parse(RAW)
    assert len(parsed) == 2
