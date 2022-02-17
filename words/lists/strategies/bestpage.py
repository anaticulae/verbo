# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex
import utila

import words.lists.strategies.geometry
import words.lists.strategies.vertical
import words.lists.utils


def run(ptcns, headlines) -> iamraw.PageContentLists:
    textfeed = texmex.document_textfeed(ptcns)
    textdistance = texmex.document_textdistance_from_contentnavigators(ptcns)
    result = []
    for navigator in ptcns:
        pageslist = extract_best_page(
            navigator,
            headlines,
            textfeed,
            textdistance,
        )
        if not pageslist:
            continue
        result.append([navigator.page, pageslist, len(navigator)])
    merged = merge_overlapping_lists(result)
    result = pagecontentlist(merged)
    return result


def extract_best_page(navigator, headlines, textfeed, textdistance):
    geo = words.lists.strategies.geometry.analyze_page(
        navigator,
        headlines,
        textfeed,
    )
    geo = [
        item for item in geo if words.lists.utils.valid_area(item.area) and
        words.lists.utils.valid_list_content(item.data)
    ]
    vertical = words.lists.strategies.vertical.analyze_page(
        navigator,
        headlines,
        textdistance,
    )
    vertical = [
        item for item in vertical if words.lists.utils.valid_area(item.area) and
        words.lists.utils.valid_list_content(item.data)
    ]
    selected = utila.zip_optimizer(  # pylint:disable=E1101
        geo,
        vertical,
        selector=lambda x: x.area,
    )
    result = []
    # single: iamraw.PageList
    for single in selected:
        count_newline = [
            content.count(utila.NEWLINE) + 1 for _, content in single
        ]
        single.area_length = count_newline
        # TODO: REPLACE 0,0 with correct one
        result.append((0, 0, single))
    return result


def merge_overlapping_lists(items):
    if not items:
        return []
    result = [items[0]]
    for item in items[1:]:
        lastpage, content, lastlength = result[-1]
        lastlist = content[-1][2]
        pageplus = words.lists.utils.pagerange(lastlist.area)

        currentpage, currentlist = item[0], item[1][0][2]
        pagestart = utila.iszero(currentlist.area[0])
        connected = all((
            ((lastpage + pageplus) == currentpage),
            ((lastlength - 1) == lastlist.area[-1]),
        ))

        if pagestart and connected:
            # merge lists
            for entree in currentlist:
                lastlist.append(level=entree[0], title=entree[1])
            lastlist.area.extend(currentlist.area)
            # update length of page navigation where list is located to
            # merge more than two pages.
            result[-1][2] = lastlength

            if item[1][1:]:
                # more than one list per page
                result[-1][1].extend(item[1][1:])
                result[-1][2] = item[2]
        else:
            result.append(item)

    # remove navigator length entree
    result = [tuple(item[0:2]) for item in result]
    return result


def pagecontentlist(pages) -> iamraw.PageContentLists:
    result = []
    for page, content in pages:
        collected = []
        for paragraph, merged_, listinstance in content:
            listinstance.paragraph = paragraph
            listinstance.merged = merged_
            listinstance.area = utila.groupby_ascending(listinstance.area)
            collected.append(listinstance)
        result.append(iamraw.PageContentList(page=page, content=collected))
    return result
