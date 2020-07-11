# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import configo
import iamraw
import serializeraw.sections
import utila
import yaml


@functools.lru_cache(configo.CACHE_SMALL)
def load_sections(
        content: str,
        onerror: callable = None,
        pages: tuple = None,
) -> iamraw.Sections:
    """Load sections from path or str.

    Args:
        content(str): path or yaml representation of `Sections`
        pages(tuple): tuple of page numbers to load - if none, load all
        onerror(callable): if `CTOR` is not found, onerror is called for
                           a second try.
    Return:
        loaded Sections
    """
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)

    result = iamraw.Sections()
    for section in loaded:
        inside, section_pages = inside_section(section, pages)
        if not inside:
            # no part of current section is inside
            continue
        if len(section_pages) == len(inside):
            # every page of section is inside, add all
            result.append(
                serializeraw.sections.load_item(
                    section,
                    onerror=onerror,
                ))
            continue
        # some parts are inside, shrink section with reduced content
        complete = serializeraw.sections.load_item(section, onerror=onerror)
        shrinked = serializeraw.sections.shrink_section(complete, pages)
        result.append(shrinked)
    return result


def inside_section(section: dict, pages: tuple) -> list:
    """\
    # selective page inside
    >>> inside_section({'start' : 0, 'end': 4}, pages=(3, 4, 5))
    ([3], (0, 1, 2, 3))

    # single page selected
    >>> inside_section({'start' : 2, 'end': 2}, pages=(1, 2, 3, 4))
    ([2], (2,))

    # no page inside
    >>> inside_section({'start' : 2, 'end': 10}, pages=(12, 13, 14))
    ([], (2, 3, 4, 5, 6, 7, 8, 9))
    """
    start, end = section['start'], section['end']
    if start == end:
        end = end + 1
    section_pages = tuple(range(start, end))
    inside = [
        page for page in section_pages if not utila.should_skip(page, pages)
    ]
    return inside, section_pages


serializeraw.load_sections = load_sections
