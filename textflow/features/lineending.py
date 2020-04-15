# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import iamraw
import serializeraw
import texmex
import utila
import yaml

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
            lastchar_bounding = line.bounding
            endings.append((char, lastchar_bounding))
        result.append(
            PageContentLineEnding(
                page=navigator.page,
                content=endings,
            ))
    dumped = dump_lineendings(result)
    return dumped


def dump_lineendings(items) -> str:
    result = []
    for page in items:
        rawpage = []
        for line in page.content:
            char, bounding = line
            bounding = tuple(bounding)
            raw = '%s %s %s %s %s' % (char, *bounding)
            rawpage.append(raw)
        result.append({'page': page.page, 'content': rawpage})
    dumped = yaml.dump(result)
    return dumped


def load_lineendings(raw: str, pages: tuple = None) -> PageContentLineEndings:
    raw = utila.from_raw_or_path(raw, ftype='yaml')
    loaded = yaml.load(raw, Loader=yaml.FullLoader)
    result = []
    for page in loaded:
        pagenumber = int(page.page)
        if utila.should_skip(pages, pagenumber):
            continue
        content = []
        for line in page:
            char, bounding = line.split(maxsplit=1)
            bounding = iamraw.BoundingBox(utila.parse_tuple(bounding))
            content.append((char, bounding))
        result.append(PageContentLineEnding(page=pagenumber, content=content))
    return result
