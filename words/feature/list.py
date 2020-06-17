# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""There are 2 different types of list:

    * the ordered (1.,2.,3.,...)
    * dotted, plus, minus - list (* Bratwurst, * Currwurst, +, -.)

     - load extracted text
     - filter undefined areas
     - check undefined area that area is list
"""

import iamraw
import serializeraw
import texmex
import utila

import words.lists.regex
import words.lists.strategy
import words.loader.input


@utila.checkdatatype
def work(
        text: str,
        textpositions: str,
        border: str,
        headlines: str,
        headerfooters: str,
        pages: tuple = None,
) -> str:
    """Combine `extracted_text` and check the `undefined` fields for lists.

    extracted_text(str): document with `undefined fields` from `text`
                         module of `words`
    """
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=border,
        headerfooterpath=headerfooters,
        pages=pages,
    )
    headlines = serializeraw.load_headlines(headlines)

    result = words.lists.strategy.extract_lists(ptcns, headlines)

    merged = merge_overlapping_lists(result)

    # TODO: REMOVE CONVERSION AFTER CHANGING UPPER ALGO
    result = []
    for page, content in merged:
        collected = []
        for paragraph, merged, listinstance in content:
            listinstance.paragraph = paragraph
            listinstance.merged = merged
            collected.append(listinstance)
        result.append(iamraw.PageContentList(page=page, content=collected))
    dumped = serializeraw.dump_lists(result)
    return dumped


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
        else:
            result.append(item)
        if item[1][1:]:
            # more than one list per page
            result.append([currentpage, item[1][1:], item[2]])

    # remove navigator length entree
    result = [tuple(item[0:2]) for item in result]
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


def process_page(
        pagecontent,
        contentborder: iamraw.Border,
) -> iamraw.PageContentList:
    """Merges parameter  according due `pagecontent`

    Format:
        page 5
            paragraphnumber, mergednumber, list
            0                1             []
            0                3             []
            0                4             []
            3                1             []
    """
    # TODO: REMOVE METHOD?
    result, page = [], -1
    for paragraph in pagecontent:
        page, paragraphnumber, (content, uindexs) = paragraph
        zipped = enumerate(zip(content, uindexs))
        for mergednumber, ((_, items), uindex) in zipped:
            items = [
                texmex.TextBoundsInfo(
                    bounds=item.bounding,
                    text=item.text,
                ) for item in items
            ]
            potentiallist = words.lists.regex.extract_lists(
                items,
                utila.select_page(contentborder, page=page),
                uindex,
            )
            if not potentiallist:
                # could not extract any list
                continue
            for listitem in potentiallist:
                listitem.merged = mergednumber
                listitem.paragraph = paragraphnumber
            result.extend(potentiallist)
    if not result:
        return None
    return iamraw.PageContentList(page=page, content=result)
