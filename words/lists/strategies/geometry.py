# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import geostrat
import iamraw
import utila

import words.lists.strategies.regex


def analyze_page(ptcn, headlines, textfeed):
    result = []
    grouped = groupby_textfeed(ptcn, headlines, textfeed)
    for group in grouped:
        data = [item[1] for item in group]
        indexes = [item[0] for item in group]
        try:
            parsed = geostrat.al_parse_pages([data])
        except geostrat.AlternateGeometryException:
            continue
        parsed = parsed[0]
        extracted = extract_list(parsed, indexes)
        if not extracted:
            utila.debug(f'could not extract possible:\n{parsed}')
            continue
        result.append(extracted)
    return result


def extract_list(possible_list, indexes):
    result = iamraw.PageList(area=indexes)
    index = 0
    for listitem in possible_list:
        content = utila.NEWLINE.join([item.text.strip() for item in listitem])
        parsed = words.lists.strategies.regex.parse_single(content)
        if not parsed:
            # utila.error(f'could not extract list step:\n{content}')
            continue
        for item in parsed:
            if isinstance(item, str):
                result.append(item, index)
            else:
                content, level = item
                result.append(content, level)
            index = index + 1
    return result


def groupby_textfeed(ptcn, headlines, textfeed):
    result = []
    for index, line in enumerate(sync_headlines(ptcn, headlines)):
        if line is None:
            result.append([(index, line)])
            continue
        x0 = line.bounding.x0
        try:
            before = result[-1][-1][1].bounding.x0
        except AttributeError:
            # Headline/None-item before
            before = None
        except IndexError:
            # empty result list, first item
            before = None
        feeded = before and any((
            utila.near(x0, textfeed, diff=5.0),
            utila.near(before, textfeed, diff=5.0),
        ))
        maxdiff = 5.0 if feeded else 20.0  # TODO: HOLY VALUE
        if before is None:
            # After headline of first item on page
            result.append([(index, line)])
        elif not utila.near(x0, before, diff=maxdiff):
            # textfeed changes
            result.append([(index, line)])
        else:
            result[-1].append((index, line))
    result = [item for item in result if item[0][1] is not None]
    return result


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
    page = navgiator.page
    headlines = utila.flatten(headlines)
    headlines = [ranges(item) for item in headlines if item.page == page]
    headlines = set(utila.flatten(headlines))  # pylint:disable=R0204

    for index, line in enumerate(navgiator):
        if index in headlines:
            yield None
        else:
            yield line
