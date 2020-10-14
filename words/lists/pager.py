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
import utila

import words.lists.strategies.regex

# TODO: CHECK TO REMOVE THIS UNSED STRATEGY


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
            potentiallist = words.lists.strategies.regex.extract_lists(
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
