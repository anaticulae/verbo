# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import serializeraw
import texmex

import textflow.alignment.style
import textflow.serialize


def work(
        text: str,
        textpositions: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text,
        textpositions,
        pages=pages,
        mode=texmex.PageTextNavigatorMode.HORIZONTAL,
    )
    expected = textflow.alignment.style.document_linealignments_expected(
        navigators)

    expected = [
        textflow.serialize.PageContent(page=page, content=content)
        for page, content in expected
    ]

    dumped = dump_alignment(expected)
    return dumped, ''


@textflow.serialize.dumpme
def dump_alignment(items) -> str:
    try:
        dumped = [str(item) for item in items]
    except TypeError:
        dumped = str(items)
    return dumped


@textflow.serialize.loadme
def load_alignment(items):
    loaded = [item for item in items]
    return loaded
