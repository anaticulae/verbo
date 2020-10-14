# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Multiple Page List Extractor
============================

This strategy is required to parse lists which are very long and
expanded over multiple pages. If the content of some list steps is so
huge, that only one content line is on the page, it is very
hard/impossible to detect this as a valid list, cause most of the
strategies expect more than one list item on a page. Furthermore it is
hard to distinguish between lists and headlines.

To solve this issue we expand the horizon from page to multiple page
level. We comebine `CHUNK_SIZE` pages to one big page and use or default
one page strategies to detect the huge lists on this single huge page.

It is important to run this strategy twice. The second run is done with
a offset to catch lists which are placed on the border of `CHUNK_SIZE`.
Using `CHUNK_SIZE` with the document length should solve this issue.
The problem of using a very long `CHUNK_SIZE` is selecting best result
uses only one extraction strategy for all content.

Furthermore `CHUNK_SIZE` limit the maximum length of detected list. If
we use `CHUNK_SIZE` one, we run our default strategies in single page
mode.
"""

import collections

import iamraw
import texmex
import utila

import words.lists.strategies.bestpage

CHUNK_SIZE = 30

# TODO: RUN THIS STRATEGY TWICE!!!


def extract_lists(ptcns, headlines) -> iamraw.PageContentLists:
    textfeed = texmex.document_textfeed(ptcns)
    chunked = split(ptcns)

    result = []
    for chunk in chunked:
        extracted = words.lists.strategies.bestpage.extract_best_page(
            chunk,
            headlines,
            textfeed,
        )
        # if extracted:
        result.append(extracted)

    adjusted = adjust_pagenumbers(result, chunked, ptcns)
    return adjusted


def adjust_pagenumbers(extracted, chunked, ptcns) -> iamraw.PageContentLists:  # pylint:disable=R0914
    """Add pagenumber to extracted lists. The lists does not have the
    correct page number, cause there extracted with big connected page
    chunk."""
    lookup, local = chunk_lookup(chunked, ptcns)
    matched = collections.defaultdict(list)
    for index, chunk in enumerate(extracted):
        for paragraph, merged_, listi in chunk:
            listi.paragraph = paragraph
            listi.merged = merged_
            first_area = listi.area[0]
            starting_page = lookup[index][first_area]
            matched[starting_page].append(listi)
            # convert to local content navigator area
            area = [local[index][relativ] for relativ in listi.area]
            splitted = utila.groupby_ascending(area)
            listi.area = splitted
    pages = [
        iamraw.PageContentList(page=page, content=content)
        for page, content in matched.items()
    ]
    return pages


def split(ptcns, offset=0):  # pylint:disable=W0613
    splitted = utila.chunks(ptcns, size=CHUNK_SIZE)
    grouped = []
    for item in splitted:
        grouped.append(merge(item))
    return grouped


def merge(navigators: texmex.PageTextNavigators) -> texmex.PageTextNavigator:
    """Merge more than one pagenavigators to a single huge navigator to
    detect multi page lists."""
    if not navigators:
        return None
    if navigators[0]:
        header = navigators[0][0].bounding[1]  # y0
    else:
        # starts on empty page without any content and no header
        header = 0
    y0 = header
    result = []
    for page in navigators:
        offset = y0 - header
        for item in page:
            # avoid side effects to other content
            item = item.copy()
            item.bounding.y0 = utila.roundme(item.bounding.y0 + offset)
            item.bounding.y1 = utila.roundme(item.bounding.y1 + offset)
            result.append(item)
        footer = page.content.bottom
        y0 += footer - header

    navigator = texmex.PageTextNavigator()
    navigator.data = result
    navigator.page = navigators[0].page
    return navigator


def chunk_lookup(chunked, ptcns):
    if not chunked:
        return {}
    # TODO: WHAT A CRAZY APPROACH
    pages = []
    local = []
    for navigator in ptcns:
        for index, _ in enumerate(navigator):
            pages.append(navigator.page)
            local.append(index)
    result = collections.defaultdict(dict)
    local_chunk = collections.defaultdict(dict)
    globalindex = 0
    for chunkid, chunk in enumerate(chunked):
        for index, _ in enumerate(chunk):
            result[chunkid][index] = pages[globalindex]
            local_chunk[chunkid][index] = local[globalindex]
            globalindex += 1
    converted = dict(result)  # enable KeyError
    local_chunk = dict(local_chunk)  # pylint:disable=R0204
    return converted, local_chunk
