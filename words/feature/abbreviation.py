# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation
============

List
----

DUDEN lookup
~~~~~~~~~~~~

Common accepted German abbreviations. For example: "z.B., etc., ...".

Abbreviation Table List
~~~~~~~~~~~~~~~~~~~~~~~

The `Abbreviation Table List` contains a list of extracted abbreviations
out of the abbreviation table. The list is used to improve the
confidence of the abbreviation parser. The improvements are especially
reached in short lower-case words.
"""

import iamraw
import konradus
import serializeraw

import words.abbreviation.parser


def work(sentencer: str, pages: tuple = None) -> str:
    sentences = serializeraw.load_text(sentencer, pages=pages)
    # TODO: Load parsed data from abbreviation table
    other = [iamraw.AbbreviationList(data=konradus.ABBREVIATION_LOWER)]
    lookup = iamraw.AbbreviationListLookup.fromparsed(other=other)
    parsed = words.abbreviation.parser.parses(
        sentences,
        lookup,
    )
    dumped = serializeraw.dump_text_abbreviations(parsed)
    return dumped
