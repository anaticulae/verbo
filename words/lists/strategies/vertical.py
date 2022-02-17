# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import texmex
import utila

import words.lists.regex
import words.lists.strategies.geometry


def analyze_page(ptcn, headlines):
    # TODO: RUN GROUPING A FEW TIMES AND SELECT "BEST" ONE?
    if not ptcn:
        return []
    remove_headline_content(ptcn, headlines)
    lists = group_and_parse(ptcn)
    result = create_lists(lists)
    return result


def remove_headline_content(ptcn, headlines):
    synced = words.lists.strategies.geometry.sync_headlines(ptcn, headlines)
    for index, line in enumerate(synced):
        if line:
            continue
        # invalidate headline content
        ptcn.data[index].text = ''


def group_and_parse(ptcn):
    grouped = texmex.group_linedistances_complex(ptcn)
    collected = []
    for group in grouped:
        rawgroup = [ptcn[item].text for item in group]
        content = ''.join(rawgroup)
        if not content.strip():
            collected.append(None)
            continue
        parsed = words.lists.regex.parse_single(content)
        # parsed = fix_lastone(parsed)
        if parsed:
            # TODO: GROUP DOES NOT REPRESENT THE COLLECTED LINES, GROUPS
            # CONTAINS THE WHOLE CONTENT CHUNK
            indexes = group_indexes(rawgroup, parsed, offset=min(group))
            collected.append((parsed, indexes))
        else:
            collected.append(None)
    lists = utila.groupby_none(collected)
    return lists


# skip list if more empty items are parsed
EMPTY_ITEM_RATE_MAX = configo.HV_PERCENT_PLUS(default=20)
# disable empty rate check for fewer empty items
EMPTY_ITEM_LENGTH_MIN = configo.HV_INT_PLUS(default=5)


def create_lists(lists) -> list:
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
        rate = empty_list_rate(current)
        if rate > EMPTY_ITEM_RATE_MAX:
            continue
        result.append(current)
    return result


def empty_list_rate(list_single: iamraw.PageList) -> float:
    empty = len([item for item in list_single if not item[1]])
    if not empty:
        return 0.0
    if empty < EMPTY_ITEM_LENGTH_MIN:
        return 0.0
    rate = empty / len(list_single)
    return rate


LAST_ONE_DISTANCE_MAX = configo.HV_PERCENT_PLUS(default=10)


def fix_lastone(items):
    """Workaround to ensure that last list item is not expanded into the
    text.

    NOTE: this is only a first approach.
    """
    # TODO: DO WE REALY REQUIRE THIS?
    if not items:
        return items
    last = items[-1][0] if isinstance(items[-1], tuple) else items[-1]
    splitted = last.splitlines()
    connected = [splitted[0]]
    for item in splitted[1:]:
        if len(item) > (len(connected[-1]) * (1.0 + LAST_ONE_DISTANCE_MAX)):
            break
        connected.append(item)
    # update last one
    updated = '\n'.join(connected)
    if isinstance(items[-1], tuple):
        items[-1] = (updated, items[-1][1])
    else:
        items[-1] = updated
    return items


DIFF_MAX = configo.HV_FLOAT_PLUS(default=0.6)


def group_indexes(group, parsed, offset: int) -> tuple:
    # TODO: O^2 RUNTIME
    # TODO: BUGGY
    group = [line.strip() for line in group]
    result = []
    for index, item in enumerate(group):
        for parse in parsed:
            parse = parse if isinstance(parse, str) else parse[0]  # HACK:
            if utila.similar(
                    item,
                    parse,
                    maxdiff=DIFF_MAX,
            ) or item in parse:
                result.append(index + offset)
    result = utila.make_unique(result)
    result = utila.longest(utila.groupby_diff(result))
    return tuple(result)
