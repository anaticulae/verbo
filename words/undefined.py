# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import texmex
import utila


def extract_undefined(pages, text, text_position, contentborder: dict):  # pylint:disable=R0914
    """Fill `undefined items` with TextContent and BoundingBox.
    Returns replaced pages with grouped replaced undefined items
    """
    # assert isinstance(contentborder, Border), type(contentborder)
    pagetextnavigators = texmex.create_pagetextnavigators(
        text=text,
        text_positions=text_position,
    )
    result = []
    for (page, pagecontent) in pages:
        navigator = utila.select_page(pagetextnavigators, page)
        ptcn = texmex.PageTextContentNavigator(
            navigator,
            content=utila.select_page(contentborder, page=page),
        )
        _pagecontent = []
        for index, (_, paragraph) in enumerate(pagecontent):
            # split the undefined groups
            # TODO: CHECK HERE FOR BOXING
            splitted_paragraph = splitter(paragraph)
            # fill undefined groups with text content
            paragraph_items = [(uindex, [
                ptcn[intindex(item)] for item in undefineds
            ]) for (uindex, undefineds) in enumerate(splitted_paragraph)]

            paragraph_undefined = [[
                int(intindex(item)) for item in undefineds
            ] for (uindex, undefineds) in enumerate(splitted_paragraph)]

            if paragraph_items:
                _pagecontent.append((
                    page,
                    index,
                    (paragraph_items, paragraph_undefined),
                ))
        # skip empty elements
        if _pagecontent:
            result.append(_pagecontent)
    return result


def intindex(index: str) -> int:
    """Convert undefined index `'31u'` to int index `31"""
    assert index[-1] == 'u', str(index)
    return int(index[:-1])


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
