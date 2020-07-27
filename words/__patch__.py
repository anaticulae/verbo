# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import utila


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


def should_skip(page: 'PageNumbers', pages: tuple) -> bool:  # pylint:disable=W0621
    """Determine if `page` is invalid.

    If `pages` is None, every page is accepted.
    If `pages` is a tuple, only the elements in tuple are valid and
    return False.

    Args:
        page(int): check to skip this page number
        pages(tuple): tuple with accepted pages, !require tuple to serialize!
    Returns:
        return True if `page` is in `pages` or pages is None else False

    Examples:
    >>> should_skip(5, (1, 2, 3))
    True
    >>> should_skip(5, None)
    False
    >>> should_skip(6, 5)
    True
    >>> should_skip((4, 5, 6), [1, 2, 3, 4, 5])
    True
    >>> should_skip((0.0, 0.5), (0, 1, 2, 3))
    False
    >>> should_skip((0.0, 0.5), (0,))
    True
    >>> should_skip((0.0, 0.5), (0, 1))
    False
    """
    if pages is None:
        return False
    if not isinstance(pages, tuple):
        pages = (pages,)
    # support multiple pages
    if isinstance(page, tuple):
        # ensure that all (page..) are in range, all selected and all inside
        start, end = min(page), max(page)
        start, end = math.floor(start), math.ceil(end)
        return any([should_skip(pp, pages) for pp in range(start, end + 1)])
    return not page in pages


utila.should_skip = should_skip
