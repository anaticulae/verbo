# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex

import words.lists.geometry
import words.lists.vertical


def extract_lists(ptcns, headlines):
    textfeed = texmex.document_textfeed(ptcns)

    result = []
    for navigator in ptcns:
        pageslist = extract_best(navigator, headlines, textfeed)
        if not pageslist:
            continue
        result.append([navigator.page, pageslist, len(navigator)])

    merged = merge_overlapping_lists(result)

    result = pagecontentlist(merged)
    return result


def extract_best(navigator, headlines, textfeed):
    geo = words.lists.geometry.analyze_page(navigator, headlines, textfeed)
    vertical = words.lists.vertical.analyze_page(navigator)
    # TODO: CHOOSE BETTER SELECTOR
    geo_score = sum([len(item.area) for item in geo])
    vertical_score = sum([len(item.area) for item in vertical])
    # prefere result which explains more areas
    selected = geo if geo_score > vertical_score else vertical
    result = []
    for lists in selected:
        # TODO: REPLACE 0,0 with correct one
        result.append((0, 0, lists))
    return result


def merge_overlapping_lists(items):
    if not items:
        return []
    result = [items[0]]
    for item in items[1:]:
        lastpage, content, lastlength = result[-1]
        lastlist = content[-1][2]
        pageplus = pagerange(lastlist.area)

        currentpage, currentlist = item[0], item[1][0][2]
        pagestart = currentlist.area[0] == 0
        connected = all((
            ((lastpage + pageplus) == currentpage),
            ((lastlength - 1) == lastlist.area[-1]),
        ))

        if pagestart and connected:
            # merge lists
            for entree in currentlist:
                lastlist.append(*entree)
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
            collected.append(listinstance)
        result.append(iamraw.PageContentList(page=page, content=collected))
    return result


def pagerange(items) -> int:
    """\
    >>> pagerange([1, 2, 3, 0, 1, 2, 3, 4, 0, 1])
    3
    """
    if not items:
        return 0
    # TODO: REPLACE WITH UTILA CODE
    result = [[items[0]]]
    for item in items[1:]:
        if item < result[-1][-1]:
            result.append([item])
        else:
            result[-1].append(item)
    return len(result)
