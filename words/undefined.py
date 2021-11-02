# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import texmex
import utila

import words.text


def extract_undefined(
    pages: words.text.PageContentPageTextDetectedList,
    ptcns: texmex.PageTextContentNavigators,
):
    """Fill `undefined items` with TextContent and BoundingBox.
    Returns replaced pages with grouped replaced undefined items
    """
    result = []
    for pageitem in pages:
        ptcn = utila.select_page(ptcns, pageitem.page)
        content = []
        for index, (_, paragraph) in enumerate(pageitem.content):
            # split the undefined groups
            # TODO: CHECK HERE FOR BOXING
            splitted_paragraph = splitter(paragraph)
            # fill undefined groups with text content
            try:
                paragraph_items = [
                    (uindex, [ptcn[intindex(item)]
                              for item in undefineds])
                    for (uindex, undefineds) in enumerate(splitted_paragraph)
                ]
            except IndexError:
                utila.error('IndexError')
                paragraph_items = []

            try:
                paragraph_undefined = [[
                    intindex(item) for item in undefineds
                ] for (uindex, undefineds) in enumerate(splitted_paragraph)]
            except IndexError:
                utila.error('IndexError X')
                paragraph_undefined = []

            if paragraph_items:
                content.append((
                    pageitem.page,
                    index,
                    (paragraph_items, paragraph_undefined),
                ))
        # skip empty elements
        if content:
            result.append(content)
    return result


def intindex(index: str) -> int:
    """Convert undefined index `'31u'` to int index `31.

    >>> intindex('31u')
    31
    >>> intindex('1') is None
    True
    """
    with contextlib.suppress(ValueError, IndexError):
        if index[-1] == 'u':
            return int(index[:-1])
    return None


def listindex(index: str) -> int:
    """Convert list index `'10l'` to int index `10.

    >>> listindex('10l')
    10
    >>> listindex('5l17')
    (5, 17)
    """
    with contextlib.suppress(ValueError, IndexError):
        splitted = index.split('l')
        if not splitted[1]:
            return int(splitted[0])
        return int(splitted[0]), int(splitted[1])
    return None


def splitter(items):
    """Create groups of undefined items separated by content items"""
    result, current = [], []
    for item in items:
        try:
            _, char = int(item[0:-1]), item[-1]
            if char != 'u':
                continue
            current.append(item)
        except ValueError:
            if current:
                result.append(current)
                current = []
    if current:
        result.append(current)
    return result
