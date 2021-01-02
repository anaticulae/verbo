# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation
============

List
----

DUDEN Whitelist
~~~~~~~~~~~~~~~

Common accepted German abbreviations. For example: "z.B., etc., ...".

Abbreviation Table List
~~~~~~~~~~~~~~~~~~~~~~~

The `Abbreviation Table List` contains a list of extracted abbreviations
out of the abbreviation table. The list is used to improve the
confidence of the abbreviation parser. The improvements are especially
reached in short lower-case words.
"""

import groupme.abbreviation
import groupme.abbreviation.lists
import serializeraw

import words.abbreviation.parser


def work(text: str, headlines: str, pages: tuple = None) -> str:
    headlines = serializeraw.load_headlines(headlines, pages=pages)

    loaded = serializeraw.load_text(text, headlines, pages=pages)
    # TODO: Load parsed data from abbreviation table
    lookup = groupme.abbreviation.lists.AbbreviationListLookup.fromparsed()

    parsed = words.abbreviation.parser.parses(loaded, lookup)

    dumped = serializeraw.dump_text_abbreviations(parsed)
    return dumped
