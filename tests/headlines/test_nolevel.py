# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utilatest

import words.headlines.machine
import words.headlines.strategies.nolevel

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
            decoration=0,
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
            decoration=0,
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


def test_headlines_no_level_docu027():
    source = power.DOCU027_PDF
    chapters = [0, 1, 2, 3, 4, 5, 6, 7]
    result = nolevel(source, chapters=chapters)
    # check only the start, TODO: increase check later?
    extracted = result[0:2]
    assert len(extracted) == len(EXPECTED)
    assert [len(item) for item in extracted] == [len(item) for item in EXPECTED]
    assert extracted == EXPECTED


@utilatest.longrun
def test_headlines_no_level_book173():
    source = power.BOOK173_PDF
    chapters = None
    result = nolevel(source, chapters)
    expected = [8, 7, 17, 11, 9, 9, 6]  # VALIDATED, extend after increase 0:100
    counted = [len(item) for item in result]
    assert counted == expected


def nolevel(source, chapters: tuple = None):
    utilatest.fixture_requires(source)
    path = power.link(source)
    section = serializeraw.load_sections(path)
    content = serializeraw.ptcn_frompath(path)
    result = words.headlines.machine.headlines(
        ptcns=content,
        sectionlist=section,
        strategies=[words.headlines.strategies.nolevel],
        chapters=chapters,
    )[0]
    return result
