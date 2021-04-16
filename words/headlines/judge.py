# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import configo
import elements
import utila

import words.headlines.machine
import words.headlines.visitor


def run(results):
    """\
        1. Compare Multiline and NoLevel - prefer multiline over NoLevel
        2. Compare result of 1. with StandardHeadlineExtractor
        3. Select best one one remaing strategies # TODO: VERIFY
    """
    report_results(results)
    # remove invalid result
    results = [
        item if not (invalid_extraction(item) or too_many_error(item)) else []
        for item in results
    ]

    best = results[1]
    if any([len(item) for item in results[0]]):
        # if any item is detected with multiline strategy, choose
        # multiline over NoLevelheadline
        best = results[0]

    # longest common text selection
    best_flat = score_headlines(best)
    standard_flat = score_headlines(results[2])
    cluster_flat = score_headlines(results[3])

    maxed = max(best_flat, standard_flat) * 2
    if cluster_flat > maxed:
        # backup strategy
        return results[3]
    return best if best_flat > standard_flat else results[2]


def report_results(results: list):
    for strategy, result in zip(words.headlines.machine.STRATEGIES, results):
        utila.debug(strategy.__name__)
        utila.debug(f'score: {score_headlines(result)}')
        utila.debug(f'error: {score_levelerror(result)}')
        utila.debug()

    for strategy, result in zip(words.headlines.machine.STRATEGIES, results):
        utila.debug(strategy.__name__)
        for item in utila.flatten(result):
            utila.debug(item.raw)
        utila.debug('')
        utila.debug('')


def score_headlines(items) -> int:
    score = 0
    for item in utila.flatten(items):
        score += len(item.title)
        if item.level is not None:
            # prefer headline with extracted level over headlines without
            # level
            score += len(item.title)
    return score


def score_levelerror(items: list) -> int:
    """Determine holes in ascending headline level. This is may
    indicated by user, but mostly by selecting the wrong headline
    determination algorithm."""
    flat = utila.flatten(items)
    flat = utila.flatten(flat, append=True)
    error = 0
    rawlevel = [
        item.raw_level
        for item in flat
        if item.raw_level and elements.level_numbered(item.raw_level)
    ]
    rawlevel = utila.notempty(rawlevel)
    grouped = words.headlines.visitor.groupby_level(rawlevel)
    for groups in grouped:
        for group in groups:
            group = [patch(item) for item in group]
            if group[0] != 1:
                error += 1
            diffs = utila.diffs(group) if len(group) > 1 else []
            diffs = [item for item in diffs if item != 1]
            error += len(diffs)
    return error


def patch(raw: str) -> int:
    """\
    >>> patch('1.4.2')
    2
    >>> patch('1.0.')
    0
    >>> patch('1.')
    1
    """
    if not raw:
        return None
    splitted = [item for item in raw.rsplit('.') if item]
    if not splitted:
        return None
    with contextlib.suppress(ValueError):
        return int(splitted[-1])
    return 0


MAX_LEVELONE_IN_A_ROW = configo.HV_INT_PLUS(4).value


def invalid_extraction(headlines) -> bool:
    """Judge extracted strategy and decide if result can be valid.

    1. Strategy: Check longest sequence of level one headlines.
    """
    headlines = utila.flatten(headlines)
    # too many level ones in a row
    levels = [item.level for item in headlines if item.level is not None]
    grouped = utila.groupby_diff(levels, diff=0, sort=False)
    longest_levelone = utila.longest([item for item in grouped if item[0] == 1])
    if len(longest_levelone) > MAX_LEVELONE_IN_A_ROW:  # TODO: HOLY VALUE
        return True
    return False


ERROR_MAX = configo.HolyTable(
    [
        (0, 0),
        (10, 1),
        (20, 2),
        (30, 3),
        (50, 4),
    ],
    strategy=utila.Strategy.LOWER,
    left_outranges_none=False,
    right_outranges_none=False,
)


def too_many_error(headlines) -> bool:
    if not headlines:
        return False
    headline_count = len(utila.flatten(headlines))
    if headline_count < 10:  # TODO: MAGIC NUMBER
        # TODO: THINK ABOUT THIS
        # disable check for too few headlines
        return False
    error = score_levelerror(headlines)
    error_max = ERROR_MAX(headline_count)
    return error > error_max
