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
import texmex.navigator
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
        formulas_paragraph = select_formulas(formulas, first, second, pcn)
        if formulas_paragraph:
            result = insert_formulas(
                result,
                formulas=formulas_paragraph,
            )
    return result


def insert_formulas(
    content: list,
    formulas: iamraw.PageContentRawFormula,
) -> list:
    result = list(content)
    if not formulas:
        return result
    for index, item in enumerate(formulas):
        position = texmex.navigator.insert_position(
            item.bounding,
            result,
        )
        result.insert(
            position,
            iamraw.DFormula(bounding=item.bounding, content=index),
        )
    return result


def select_formulas(formulas, first, second, pcn):
    formulas = utila.select_page(
        formulas,
        page=pcn.page,
        default=[],
    )
    if not formulas:
        return []
    # all formuals valid from page start
    start = 0
    if first and first.container not in (0, -1):
        start = pcn[inrange(first.container, pcn, maxi=False)].bounding[1]
    # all formuals valid till page end
    end = 2048  # LARGE NUMBER
    if second and second.container not in (0, -1):
        end = pcn[inrange(second.container, pcn)].bounding[3]
    # select formulas between headlines "inside paragraph"
    formulas = [
        item for item in formulas.content if utila.isinside(
            value=(item.bounding[1] + item.bounding[3]) / 2,
            left=start,
            right=end,
        )
    ]
    return formulas


def inrange(index, pcn, maxi: bool = True):
    # maxi: use start or end
    # TODO: REMOVE AFTER FIXING ONELINE NORMAL CONVERTING
    if isinstance(index, tuple):
        utila.error(f'tuple {index}')
        if maxi:
            index = index[-1]
        else:
            index = index[0]
    if index >= len(pcn):
        error = (index, len(pcn), pcn.page)
        utila.error(f'~oneline-normal headline problem: {error}')
        index = len(pcn) - 1
    return index


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
