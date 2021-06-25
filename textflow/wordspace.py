# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""WordSpace
=========

Exclude:

* Headline
* Figures

Source:

* PageTextContentNavigator
* Magic content
"""

import iamraw
import texmex
import utila


def extract(
    ptcns: texmex.PageTextContentNavigators,
    magics: iamraw.PageContentContentTypes,
    wordspaces,
) -> iamraw.PageContents:
    result = []
    for page, (ptcn, magic, wordspace) in utila.sync_pages(
            iterators=[ptcns, magics, wordspaces],
            numbers=True,
    ):
        # white pages do not have any word space or magic content
        wordspace = wordspace.content if wordspace else []
        magic = magic.content if magic else {}
        extracted = extract_page(ptcn, magic, wordspace)
        result.append(iamraw.PageContent(page=page, content=extracted))
    return result


def extract_page(ptcn, magic, wordspace) -> list:
    if not ptcn:
        # empty page
        return []
    magic = {number for number, typ in magic if typ in INVALID}
    result = []
    for number, line in enumerate(ptcn):
        if number in magic:
            continue
        bounding = line.bounding
        inline = [
            item for item in wordspace
            if utila.rectangle_inside(bounding, item)
        ]
        if not inline:
            continue
        result.append((number, inline))
    return result


INVALID = {
    iamraw.PageContentType.FIGURE,
    iamraw.PageContentType.FORMULA,
    iamraw.PageContentType.LIST,
    iamraw.PageContentType.TABLE,
}
