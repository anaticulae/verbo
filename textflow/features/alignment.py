# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

    expected = extract_expected(navigators)
    expected_dumped = dump_alignment(expected)

    current = extract_current(navigators)
    current_dumped = dump_alignment(current)
    return current_dumped, expected_dumped


def extract_expected(navigators):
    expected = textflow.alignment.style.document_linealignments_expected(
        navigators)
    expected = [
        textflow.serialize.PageContent(page=page, content=content)
        for page, content in expected
    ]
    return expected


def extract_current(navigators):
    border = textflow.alignment.style.document_textfeed(navigators)
    result = [
        textflow.serialize.PageContent(
            page=navigator.page,
            content=textflow.alignment.style.page_linealignments(
                navigator,
                *border,
            ),
        ) for navigator in navigators
    ]
    return result


@textflow.serialize.dumpme
def dump_alignment(items) -> str:
    try:
        dumped = [str(item) for item in items]
    except TypeError:
        dumped = str(items)
    return dumped


@textflow.serialize.loadme
def load_alignment(items):
    items = items.replace('TextAlignment.', '')
    return textflow.alignment.style.TextAlignment[items]


def extract_alignment_frompath(path, prefix, pages: tuple = None):
    navigators = serializeraw.create_pagetextnavigators_frompath(
        path,
        prefix=prefix,
        pages=pages,
    )
    current = extract_current(navigators)
    return current
