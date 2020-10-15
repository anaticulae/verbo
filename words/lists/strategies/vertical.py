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


def analyze_page(ptcn):
    grouped = texmex.group_linedistances_complex(ptcn)

    collected = []
    for group in grouped:
        rawgroup = [ptcn[item].text for item in group]
        content = ''.join(rawgroup)
        parsed = words.lists.strategies.regex.parse_single(content)
        parsed = fix_lastone(parsed)

        if parsed:
            # TODO: GROUP DOES NOT REPRESENT THE COLLECTED LINES, GROUPS
            # CONTAINS THE WHOLE CONTENT CHUNK
            indexes = group_indexes(rawgroup, parsed, offset=min(group))
            collected.append((parsed, indexes))
        else:
            collected.append(None)
    lists = utila.groupby_none(collected)

    result = []
    for listgroup in lists:
        current = iamraw.PageList()
        for row, indexs in listgroup:
            for item in row:
                # assert len(item) == 2, str(item)
                if len(item) == 2:
                    current.append(*item)
                else:
                    current.append(item)
            current.area.extend(indexs)  # pylint:disable=E1101
        if len(current) <= 1:
            # SKIP PARSED HEADLINE
            # TODO: THINK ABOUT SMARTER CONCEPT TO COVER SINGLE ITEM LIST
            # TODO: IS SINGLE ITEM LIST NECESSARY?
            continue
        result.append(current)
    return result


def fix_lastone(items):
    """Workaround to ensure that last list item is not expanded into the
    text.

    NOTE: this is only a first approach.
    """
    if not items:
        return items
    last = items[-1][0] if isinstance(items[-1], tuple) else items[-1]
    splitted = last.splitlines()
    connected = [splitted[0]]
    for item in splitted[1:]:
        if len(item) > (len(connected[-1]) * 1.1):  # TODO: HOLY VALUE
            break
        else:
            connected.append(item)
    # update last one
    updated = '\n'.join(connected)
    if isinstance(items[-1], tuple):
        items[-1] = (updated, items[-1][1])
    else:
        items[-1] = updated
    return items


def group_indexes(group, parsed, offset: int) -> tuple:
    # TODO: O^2 RUNTIME
    # TODO: BUGGY
    group = [line.strip() for line in group]
    result = []
    for index, item in enumerate(group):
        for parse in parsed:
            parse = parse if isinstance(parse, str) else parse[0]  # HACK:
            # TODO: HOLY VALUE
            if utila.similar(item, parse, maxdiff=0.6) or item in parse:
                result.append(index + offset)
    result = utila.make_unique(result)
    result = utila.longest(utila.groupby_diff(result))
    return tuple(result)
