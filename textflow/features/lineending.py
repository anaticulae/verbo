# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import serializeraw
import texmex
import utila

import textflow.serialize

PageContentLineEnding = collections.namedtuple(
    'PageContentLineEnding',
    'content, page',
)
PageContentLineEndings = typing.List[PageContentLineEnding]


def work(text: str, textpositions: str, pages: tuple = None) -> str:
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text,
        textpositions,
        pages=pages,
        mode=texmex.PageTextNavigatorMode.HORIZONTAL,
    )
    result = []
    for navigator in navigators:
        # remove empty line
        lines = [item for item in navigator if item.text.strip()]
        endings = []
        for line in lines:
            char = line.text.strip()[-1]
            lastchar_bounding = tuple(line.bounding)
            endings.append((char, lastchar_bounding))
        result.append(
            PageContentLineEnding(
                page=navigator.page,
                content=endings,
            ))
    dumped = dump_lineendings(result)
    return dumped


@textflow.serialize.dumpme
def dump_lineendings(item) -> str:
    char, bounding = item
    raw = '%s %s %s %s %s' % (char, *bounding)
    return raw


@textflow.serialize.loadme(ctor=PageContentLineEnding)
def load_lineendings(item):
    char, bounding = item.split(maxsplit=1)
    parsed = utila.parse_tuple(bounding)
    return (char, parsed)
