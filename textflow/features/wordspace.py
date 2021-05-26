# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import textflow.serialize
import textflow.wordspace


def work(
    text: str,
    textpositions: str,
    sizeandborderpath: str,
    headerfooterpath: str,
    magic: str,
    wordspaces: str,
    pages: tuple,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborderpath,
        headerfooterpath,
        pages=pages,
    )
    magic = serializeraw.load_types(
        magic,
        pages=pages,
    )
    wordspaces = serializeraw.load_wspaces(wordspaces, pages=pages)

    result = textflow.wordspace.extract(ptcns, magic, wordspaces)

    dumped = textflow.serialize.dump_wordspaces(result)
    return dumped
