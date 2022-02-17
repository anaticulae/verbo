# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import geostrat
import iamraw
import texmex
import utila

import words.lists.strategies.regex


def analyze_page(ptcn: texmex.PTCN, headlines: list, textfeed: float) -> list:
    """Use Geometry-Strategy to detect lists on current page.

    Args:
        ptcn(PTCN): content navigator with content of current page
        headlines(list): list of document headlines
        textfeed(float): distance to left page border
    Returns:
        Extracted lists on current page.
    """
    grouped = groupby_textfeed(ptcn, headlines, textfeed)
    result = []
    for group in grouped:
        data = [item[1] for item in group]
        try:
            parsed = geostrat.al_parse_pages([data])
        except geostrat.AlternateGeometryException:
            continue
        indexes = [item[0] for item in group]
        # TODO: VERIFY[0]
        parsed = parsed[0]
        extracted = extract_list(parsed, indexes)
        if not extracted:
            utila.debug(f'could not extract possible:\n{parsed}')
            continue
        result.append(extracted)
    return result


def extract_list(possible_list, indexes):
    result = iamraw.PageList()
    start = 0
    index = 0
    for group in possible_list:
        content = utila.NEWLINE.join([item.text.strip() for item in group])
        parsed = words.lists.strategies.regex.parse_single(content)
        if not parsed:
            # TODO: START NEW LIST HERE?
            start += len(group)
            continue
        for listitemx in parsed:
            if isinstance(listitemx, str):
                item_content, item_level = listitemx, index
            else:
                item_content, item_level = listitemx
            areas = find_area(group, item_content, startindex=start)
            result.area.extend([indexes[it] for it in areas])
            result.append(item_content, item_level)
            index = index + 1
        start += len(group)
    return result


def find_area(items: list, detected: str, startindex: int) -> list:
    # TODO: CHANGE TO AREA_AFTERWARDS VALIDATION, USE START AND END OF
    # CONTENT, NOT PREFECT, BUT OK FOR NOW.
    # TODO: REPLACE WITH UTILA CODE?
    splitted = detected.splitlines()
    if len(splitted) == 1:
        start, end = splitted[0], splitted[0]
    else:
        start, end = splitted[0], splitted[-1]
    start = find_withbackup(items, start)
    end = find_withbackup(items, end)
    if not isinstance(start, int):
        utila.error(f'could not find {start} in: {items}')
        return []
    if not isinstance(end, int):
        utila.error(f'could not find {end} in: {items}')
        return []
    end = end + 1  # ranged list
    result = utila.rlist(start + startindex, end + startindex)
    return result


def find_withbackup(items, find):
    for similar in (utila.verysimilar, utila.similar):
        for index, item in enumerate(items):
            if similar(item.text, find):
                return index
    return None


# Aligned to page text feed
FEEDED_DIFF_MAX = configo.HV_FLOAT_PLUS(default=5.0)
# Text feed does not align with page text feed
NOT_FEEDED_DIFF_MAX = configo.HV_FLOAT_PLUS(default=20.0)
# Max diff to left text feed to be in feed
LEFT_FEED_DIFF_MAX = configo.HV_FLOAT_PLUS(default=5.0)


def groupby_textfeed(ptcn, headlines, textfeed: float):
    result = []
    for index, line in enumerate(sync_headlines(ptcn, headlines)):
        if line is None:
            # headline, start new group
            result.append([(index, line)])
            continue
        # determine feed of line before
        before = feed_before(result)
        if before is None:
            # Before is a headline or current line is first line on the page.
            result.append([(index, line)])
            continue
        if feed_changes(current=line, before=before, textfeed=textfeed):
            # create a new group
            result.append([(index, line)])
            continue
        # add to current group
        result[-1].append((index, line))
    # remove headlines
    result = [item for item in result if item[0][1] is not None]
    return result


def feed_before(result: list) -> float:
    try:
        before = result[-1][-1][1].bounding.x0
    except AttributeError:
        # Headline/None-item before
        before = None
    except IndexError:
        # empty result list, first item
        before = None
    return before


def feed_changes(current, before, textfeed) -> bool:
    # current x-feed
    x0 = current.bounding.x0
    if not before:
        # No line before, therefore no change is possible
        return False
    feeded = any((
        utila.near(x0, textfeed, diff=LEFT_FEED_DIFF_MAX),
        utila.near(before, textfeed, diff=LEFT_FEED_DIFF_MAX),
    ))
    if feeded:
        # current line or line before is in the near of the page feed.
        # Distance to left page border is tight.
        maxdiff = FEEDED_DIFF_MAX
    else:
        # current line or line before is not aligned to page left feed.
        maxdiff = NOT_FEEDED_DIFF_MAX
    if not utila.near(x0, before, diff=maxdiff.value):
        return True
    return False


def ranges(item):
    # TODO: REPLACE WITH UTILA CODE
    container = item.container
    try:
        start, end = container
    except TypeError:
        start, end = container, container
    end = end + 1
    return range(start, end)


def sync_headlines(navgiator, headlines):
    if not navgiator:
        return
    page = navgiator.page
    headlines = utila.flatten(headlines)
    headlines = [ranges(item) for item in headlines if item.page == page]
    headlines = set(utila.flatten(headlines))  # pylint:disable=R0204
    for index, line in enumerate(navgiator):
        if index in headlines:
            yield None
        else:
            yield line
