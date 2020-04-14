#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import collections
import os
import statistics

import iamraw
import texmex
import texmex.text
import utila

__version__ = '0.1.7'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS = 'words'
PACKAGE = PROCESS

HEADLINE_STEP = 'headlines'
HEADLINE_STEP_RESULT = 'headlines'
HEADLINES = f'{HEADLINE_STEP}_{HEADLINE_STEP_RESULT}'

WORDS_HEADLINES = f'{PROCESS}__{HEADLINES}.yaml'


# TODO: MOVE TO TEXMEX
@utila.todo(
    version=iamraw.__version__,
    major=1,
    minor=23,
    description='replace with iamraw',
)
def fontdistance_textbounds(bounds: texmex.text.TextBoundsList) -> utila.Floats:
    assert isinstance(bounds, list)
    assert all(isinstance(item, texmex.TextBounds) for item in bounds)
    distance = [
        utila.roundme(first.bottomdist - second.bottomdist)
        for (first), (second) in zip(bounds[0:], bounds[1:])
    ]
    if bounds:
        # add distance from first content to page start
        # xdist, ydist(1), width, height, fontsize
        # distance.insert(0, bounds[0].bottomdist)
        distance.insert(0, 0)
    distance.append(0)  # TODO: CHECK AGAIN
    return distance


texmex.fontdistance_textbounds = fontdistance_textbounds


@utila.todo(
    version=iamraw.__version__,
    major=1,
    minor=23,
    description='replace with iamraw',
)
def document_textdistance(navigators, borders: iamraw.Borders) -> int:
    """Determine the most common text distance"""
    result = []
    for _, (navigator, contentborder) in utila.sync_pages([navigators, borders]): # yapf:disable
        if not navigator:
            # empty page
            continue
        bounds = texmex.textbounds(navigator, contentborder.border)
        # ignore empty content
        bounds = [item.bounds for item in bounds if len(item.text)]
        ydist = [item.bottomdist for item in bounds]
        for yfirst, ysecond in zip(ydist[:-1], ydist[1:]):
            distance = yfirst - ysecond
            result.append(distance)
    mode = modes(result, minimize=True)
    return mode
    # print(mode)
    # print(result)
    # try:
    #     return statistics.mode(result)
    # except statistics.StatisticsError:
    #     print(result)
    #     # TODO: Multiply add distances as often as characters are in line?
    #     # TODO: Handle equal count, see StatisticsError [12, 11, 12, 11, 148,
    #     # 17, 4, 51, 129, 58, 8, 41]
    #     # Raise StategyError and try again with different strategy
    #     assert 0, 'not decided yet'


texmex.document_textdistance = document_textdistance


# TODO: MOVE TO UTILA
def modes(
        data: 'utila.math.number.Numbers',
        minimize: bool = True,
) -> 'utila.math.number.Number':
    """Return the most common data point from discrete or nominal data.

    It is possible to have multiple common data points. To extract a
    unique point `minimize` enables to decide which number is used.

    See: statistics.mode

    Args:
        data: list of numbers
        minimize(bool): if True the biggest common number is used, if
                        not the smallest is used.
    Raises:
        StatisticsError: if data is empty
    Returns:
        Most common number.
    """
    if not data:
        raise statistics.StatisticsError('no mode for empty data')
    table = statistics._counts(data)  # pylint:disable=W0212
    if len(table) == 1:
        return table[0][0]
    current = sorted([item[0] for item in table], reverse=not minimize)
    return current


utila.modes = modes


def document_textfeed(
        navigators: texmex.PageTextNavigators,
        count: int = 1,
        left: bool = True,
) -> 'utils.Ints':
    assert count >= 1, f'require none negative count, got: {count}'
    counter = collections.Counter()
    for navigator in navigators:
        for item in navigator:
            if not item.text.strip():
                continue
            if left:
                counter[item.bounding[0]] += 1
            else:
                right = utila.roundme(item.bounding[2])
                counter[right] += 1
    result = counter.most_common(count)
    result = [item for item, _ in result]
    if count == 1:
        return result[0]
    return result[0:count]


texmex.document_textfeed = document_textfeed
