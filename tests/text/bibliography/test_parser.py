# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import words.links.bibliography as ll

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


@pytest.mark.parametrize(
    'line, expected',
    [
        (
            '(vgl. Abels 2010: 94ff.).',
            ll.BibliographyLink(author='Abels', year=2010, pages='94ff.'),
        ),
        (
            '(vgl. ebd.: 85).',
            ll.BibliographyLink(author='ebd.', year=None, pages='85'),
        ),
        (
            '(vgl. ebd.: 161ff.).',
            ll.BibliographyLink(author='ebd.', year=None, pages='161ff.'),
        ),
        (
            '(vgl. Mead 1973: 300).',
            ll.BibliographyLink(author='Mead', year=1973, pages='300'),
        ),
        (
            '(Kettner 2004: 222)',
            ll.BibliographyLink(author='Kettner', year=2004, pages='222'),
        ),
        (
            '(vgl. Havelock 1986: 77; Robinson/Hawpe 1986: 124)',
            [
                ll.BibliographyLink(author='Havelock', year=1986, pages='77'),
                ll.BibliographyLink(
                    author='Robinson/Hawpe', year=1986, pages='124'),
            ],
        ),
        (
            '(ebd.: 18; vgl. hierzu auch Havelock 1963: 47)',
            [
                ll.BibliographyLink(author='ebd.', year=None, pages='18'),
                ll.BibliographyLink(
                    author='hierzu auch Havelock',
                    year=1963,
                    pages='47',
                ),
            ],
        ),
        (
            '(vgl. Plat. Men.: 97a-98c).',
            ll.BibliographyLink(
                author='Plat. Men.',
                year=None,
                pages='97a-98c',
            ),
        ),
        (
            '(vgl. ebd.: 6; Havelock 1982: 186; Murray/Wilson 2004: 1)',
            [
                ll.BibliographyLink(author='ebd.', year=None, pages='6'),
                ll.BibliographyLink(author='Havelock', year=1982, pages='186'),
                ll.BibliographyLink(
                    author='Murray/Wilson',
                    year=2004,
                    pages='1',
                ),
            ],
        ),
        (
            '(vgl. Dierse 1977: 2-6).',
            ll.BibliographyLink(author='Dierse', year=1977, pages='2-6'),
        ),
        (
            '(Meier 2007: 192).',
            ll.BibliographyLink(author='Meier', year=2007, pages='192'),
        ),
        (
            '(vgl. McQuail 2010: 467; Schenk 2007: 41; Perse 2001: 3).',
            [
                ll.BibliographyLink(author='McQuail', year=2010, pages='467'),
                ll.BibliographyLink(author='Schenk', year=2007, pages='41'),
                ll.BibliographyLink(author='Perse', year=2001, pages='3'),
            ],
        ),
        (
            '(vgl. Bonfadelli 2004: 33)',
            ll.BibliographyLink(author='Bonfadelli', year=2004, pages='33'),
        ),
        # (
        #         'Luhmann (2005a)',
        #     ll.BibliographyLink(author='Luhmann', year=2005, pages='192'),
        # ),
    ])
def test_parse_bibliographylink(line, expected):
    if not isinstance(expected, list):
        expected = [expected]
    parsed = ll.parse(line)
    assert parsed == expected


def test_parse_bibliographylink_in_text():
    expected = [
        ll.BibliographyLink(author='McQuail', year=2010, pages='454'),
        ll.BibliographyLink(author='McQuail', year=2010, pages='456-459'),
        ll.BibliographyLink(author='McQuail', year=2010, pages='459'),
        ll.BibliographyLink(author='McQuail', year=2010, pages='467'),
        ll.BibliographyLink(author='Schenk', year=2007, pages='41'),
        ll.BibliographyLink(author='Perse', year=2001, pages='3'),
        ll.BibliographyLink(author='Dierse', year=1977, pages='2-6'),
        # TODO: FIX ORDER AFTER MERGING DIFFERENT REGEX PATTERN
        ll.BibliographyLink(author='Benjamin', year=1939),
    ]
    parsed = ll.parse(INLINE)
    assert parsed == expected
