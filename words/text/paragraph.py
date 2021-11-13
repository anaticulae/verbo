# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex
import utila

import words.boxed
import words.feature
import words.feature.word
import words.headlines
import words.lookup


def collect_paragraph(
    first: iamraw.Headline,
    second: iamraw.Headline,
    pcn: texmex.PageTextContentNavigator,
    boxes: words.boxed.BoxedChecker,
    lists: 'ListLookUp',
    magics: words.lookup.PageLineLookup = None,
    formulas: iamraw.PageContentRawFormulas = None,
) -> iamraw.ChapterText:
    """Extract paragraphs between defined headlines.

    Hint: The Headlines/Container are numbered in absolute indies. Accessing
    the content requires to subtract the offset which is produced by the
    header.
    """
    # convert to content coordiante, and step one element further cause of
    # current element is the headline and we want to start with content
    start = first.end + 1
    # determine end mark
    if second and first.page == second.page:
        end = second.start
    else:
        end = len(pcn)
    if first.start == -1 and second and second.start != -1:
        # start with None-Container followed by Headline container
        # TODO: Check theses indexes
        end = second.start
    if second is not None and start + 1 == second.start:
        # no content between headlines, skip range(start, end)
        end = start
    # collect content after headline
    result = determine_chunktypes(
        pcn,
        start,
        end,
        magics,
        lists,
        boxes,
    )
    if formulas:
        result = insert_formulas(
            result,
            formulas=utila.select_page(
                formulas,
                page=pcn.page,
                default=[],
            ),
        )
    return result


def insert_formulas(
    content: list,
    formulas: iamraw.PageContentRawFormula,
) -> list:
    result = []
    result.extend(content)
    return result


def determine_chunktypes(pcn, start, end, magics, lists, boxes) -> list:
    result = []
    for index in range(start, end):
        try:
            item = pcn[index]
        except IndexError:
            # TODO: REMOVE LATER
            error = (start, end, len(pcn), pcn.page)
            utila.error(f'oneline-normal headline problem: {error}')
            break
        chunktype = content_type(
            boxes,
            lists,
            pcn.page,
            item.bounding,
            index,
            magics,
        )
        if chunktype == iamraw.PageContentType.TEXT:  # TODO: AND BLOCKQUOTE?
            container = iamraw.Paragraph(
                content=item,
                bounding=item.bounding,
            )
        else:
            container = iamraw.Undefined(
                container=index,
                bounding=item.bounding,
            )
        result.append(container)
    return result


def content_type(
    boxed: words.boxed.BoxedChecker,
    lists: words.feature.word.ListLookUp,
    page: int,
    bounding: iamraw.BoundingBox,
    index: int,
    magics: words.lookup.PageLineLookup = None,
) -> iamraw.PageContentType:
    matched_list = lists.search(page, None, undefined=index)
    if matched_list is not None:
        return iamraw.ContentType.LIST
    if boxed.contains(page, bounding):
        return iamraw.PageContentType.BOXED
    magic = magics(page=page, line=index)
    if magic:
        return magic
    return iamraw.PageContentType.TEXT
