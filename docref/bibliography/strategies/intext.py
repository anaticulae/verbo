# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw

PAGES = r"""
    (
        \d+|            # single page
        \d+ff\.|        # single page with following
        \d+\-\d+        # from x till y
    )"""

PATTERN = r"""
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
"""

AUTHOR_AND_YEAR = r"""
    \(
        (vgl[.][ ])
        (?P<author>\b[\w/]+?)
        [ ]
        (?P<year>\d{4})
    \)
"""


def parse(raw: str) -> iamraw.BibliographyReferences:
    result = []
    for current in [PATTERN, AUTHOR_AND_YEAR]:
        parsed = _parse(raw, current)
        result.extend(parsed)
    return result


def _parse(raw: str, pattern) -> iamraw.BibliographyReferences:
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
        link = iamraw.BibliographyReference(
            authors=[author],
            year=year,
            page=pages,
        )
        result.append(link)
    return result
