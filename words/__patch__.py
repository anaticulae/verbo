# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
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


def isnumber(item: str) -> bool:
    """Check if `item` is a number.

    >>> isnumber('ten')
    False
    >>> isnumber(10.5)
    True
    >>> isnumber('3.5')
    True
    """
    with contextlib.suppress(ValueError):
        _ = float(str(item))
        return True
    return False


utila.isnumber = isnumber


def near_dims(
        item: tuple,
        dims: tuple,
        nears: tuple,
        allow_none: bool = False,
) -> bool:
    """\
    >>> near_dims((5, 5), [(4, 6), (4, 7), (10, 10)], [(1, 1), (1, 1), (0, 0)])
    0
    >>> near_dims((5, 5, 5),
    ...           dims=[(4, 6, 10), (4, 7, 30), (10, 10, 50)],
    ...           nears=[(1, 1, 0), (1, 1, 0), (5, 5, 45)])
    2
    >>> near_dims((5, 5), [(4,6), (4, 7)], [(0, 0), (0, 0)]) is None
    True
    """
    assert_equal_dim(item, dims)
    dims = list(dims)
    nears = list(nears)
    matches = utila.make_tuple(len(dims))
    for index, check in enumerate(item):
        if not dims:
            return None
        old_dims, dims = dims, []
        old_news, nears = nears, []
        old_matches, matches = matches, []
        for dim, near_, match in zip(old_dims, old_news, old_matches):
            if dim[index] is None or check is None and allow_none:
                # None item always pass the test
                pass
            elif not utila.near(dim[index], check, near_[index]):
                continue
            dims.append(dim)
            nears.append(near_)
            matches.append(match)
    if matches:
        matches = matches[0] if len(matches) == 1 else matches
        return matches
    return None


def assert_equal_dim(item, dims) -> int:
    unique = {len(item) for item in dims}
    assert len(unique) == 1, str(unique)
    expected = unique.pop()
    assert len(item) == expected, f'{len(item)} != {expected}'


utila.near_dims = near_dims
