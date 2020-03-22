# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex

import words.boxed
import words.feature
import words.headlines


def collect_paragraph(
        first: iamraw.Headline,
        second: iamraw.Headline,
        page: int,
        pcn: texmex.PageTextContentNavigator,
        fcs: iamraw.FontContentStore,  # pylint:disable=W0613
        boxes: words.boxed.BoxedChecker,
) -> iamraw.ChapterText:
    """Extract paragraphs between defined headlines.

    Hint: The Headlines/Container are numbered in absolute indies. Accessing
    the content requires to subtract the offset which is produced by the
    header.
    """
    # TODO: fcs is not required anymore?
    # convert to content coordiante, and step one element further cause of
    # current element is the headline and we want to start with content
    start = first.end + 1 - pcn.offset[0]
    # determine end mark
    if second and first.page == second.page:
        end = second.end - 1
    else:
        end = len(pcn)

    if first.start == -1 and second and second.start != -1:
        # start with None-Container followed by Headline container
        # TODO: Check theses indexes
        end = second.start
    # collect content after headline
    result = []
    for index in range(start, end):
        item = pcn[index]
        contenttype = content_type(boxes, page, item.bounding, item.text)
        if contenttype == iamraw.ContentType.PARAGRAPH:
            result.append(iamraw.Paragraph(content=item))
        else:
            result.append(iamraw.Undefined(container=index))
    return result


def content_type(
        boxed: words.boxed.BoxedChecker,
        page: int,
        bounding: iamraw.BoundingBox,
        content: str,
):
    if iamraw.DOT in content:
        return iamraw.ContentType.LIST
    if boxed.contains(page, bounding):
        return iamraw.ContentType.BOXED
    return iamraw.ContentType.PARAGRAPH
