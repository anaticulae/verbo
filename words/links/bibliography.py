# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import re
import typing

PAGES = r'''
    (
        \d+|            # single page
        \d+ff\.|        # single page with following
        \d+\-\d+        # from x till y
    )'''

PATTERN = r'''
    (vgl[.][ ])?
    (?P<author>
        (
            ebd[.]|
            \b[\w /\.]+?
        )
    )
    [ ]?
    (?P<year>\d{4})?
    (
        [:]                         # optional collon between author and year
        [ ]                         # space between collon and pages
        (?P<pages>
            (
                \d+(a|b|c|d)[-]\d+(a|b|c|d)| # from x till y
                \d+[-]\d+|                   # from x till y
                \d+ff[.]|                    # single page with following
                \d+                          # single page
            )
        )
    )
'''

AUTHOR_AND_YEAR = r"""
    \(
        (vgl[.][ ])
        (?P<author>\b[\w/]+?)
        [ ]
        (?P<year>\d{4})
    \)
"""


@dataclasses.dataclass
class LLPages:
    start: int = None
    start_info: str = None
    end: int = None
    end_info: str = None
    follow: str = None
    raw: str = None


@dataclasses.dataclass
class BibliographyLink:
    author: str = None
    year: int = None
    pages: int = None
    raw: str = None


BibliographyLinks = typing.List[BibliographyLink]


def parse(raw: str) -> BibliographyLinks:
    result = []

    for current in [PATTERN, AUTHOR_AND_YEAR]:
        parsed = _parse(raw, current)
        result.extend(parsed)
    return result


def _parse(raw: str, pattern) -> BibliographyLinks:
    matched = re.finditer(pattern, raw, re.VERBOSE)
    if not matched:
        return []

    result = []
    for item in matched:
        author = item['author']
        year = int(item['year']) if item['year'] else None
        try:
            pages = item['pages']
        except IndexError:
            pages = None
        link = BibliographyLink(
            author=author,
            year=year,
            pages=pages,
        )
        result.append(link)
    return result
