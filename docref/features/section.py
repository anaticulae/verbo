# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import docref.figure
import docref.serialize


def work(text: str, headlines: str, pages: tuple = None) -> str:
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    text = serializeraw.load_text(text, headlines=headlines, pages=pages)

    parsed = parse_text(text)
    dumped = docref.serialize.dump_docref(parsed)
    return dumped


PATTERN = (
    'Abschnitt 1',
    'Abschnitt 1.',
    'Punkt 4.1.4',
    'siehe Punkt 4.7',
    'siehe Punkt 4.2.2.',
    'siehe auch Punkt 4.3.2.',
)


def parse_text(text) -> docref.serialize.DocRefs:
    return docref.figure.parse_text(text, pattern=PATTERN)
