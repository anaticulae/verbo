# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import docref.bibliography.strategies.intext
import docref.bibliography.strategies.tech


def parse(item: str) -> iamraw.BibliographyReference:
    parsed = docref.bibliography.strategies.tech.parse(item)
    if parsed:
        return parsed
    parsed = docref.bibliography.strategies.intext.parse(item)
    if parsed:
        return parsed
    return None
