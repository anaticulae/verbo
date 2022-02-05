# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import itertools
import re

import configo
import elements
import utila

import words.headlines.machine
import words.headlines.strategies
import words.headlines.visitor


@utila.log_return
def run(results):
    """\
        1. Compare Multiline and NoLevel - prefer multiline over NoLevel
        2. Compare result of 1. with StandardHeadlineExtractor
        3. Select best one one remaining strategies # TODO: VERIFY
    """
    results = prepare_results(results)
    # run selection
    best = results[1]
    if any(len(item) for item in results[0]):
        # if any item is detected with multiline strategy, choose
        # multiline over NoLevelheadline
        best = results[0]
    # longest common text selection
    best_flat = score_headlines(best)
    standard_flat = score_headlines(results[2])
    cluster_flat = score_headlines(results[3])
    magic_flat = score_headlines(results[4])
    maxed = max(best_flat, standard_flat) * 2
    # select best result
    if magic_flat > maxed:
        # TODO: CLARIFY DOCS
        # backup strategy???
        return results[4]
    if cluster_flat > maxed:
        # backup strategy???
        return results[3]
    if best_flat > standard_flat:
        return best
    return results[2]


def prepare_results(results: list) -> list:
    largenumber = results[5]
    if largenumber:
        # multiline
        results[0] = merge_ifrequired(results[0], largenumber)
        # nolevel
        # !no_merge!
        # standard
        results[2] = merge_ifrequired(results[2], largenumber)
        # cluster
        results[3] = merge_ifrequired(results[3], largenumber)
        # cluster
        results[4] = merge_ifrequired(results[4], largenumber)

    removed = remove_invalids(results)
    if not any(removed):
        # if no results are left, try with higher accepted error rate
        removed = remove_invalids(results, second=True)
    report_results(removed)
    return removed


def report_results(results: list):
    # print score
    for strategy, result in zip(words.headlines.machine.STRATEGIES, results):
        utila.debug(strategy.__name__)
        utila.debug(f'score: {score_headlines(result)}')
        utila.debug(f'error: {score_levelerror(result)}')
        utila.debug()
    # print result
    for strategy, result in zip(words.headlines.machine.STRATEGIES, results):
        utila.debug(strategy.__name__)
        for item in utila.flatten(result):
            utila.debug(item.raw.strip())
        utila.debug()
        utila.debug()


def merge_ifrequired(result: list, largenumber: list) -> list:
    """If chapter does not contain any first level headlines and
    largenumber extraction delivers first level headlines, merge them to
    improve extraction.
    """
    # TODO: WE DO NOT MERGE IF LARGE NUMBER IS NOT DETECTED IN CHAPTER
    # WHERE OTHER HEADLINES ARE EXTRACTED.
    if not largenumber:
        # no append is possible
        return result
    # remove empty headline level
    firstlevel = any(
        words.headlines.strategies.isfirstlevel(item[0])
        for item in result
        if item)
    if firstlevel:
        # no first level append is required
        return result
    flat = utila.flatten(result)
    # copy list to avoid changing
    merged = [list(headliner) for headliner in largenumber]
    for current, after in itertools.zip_longest(merged, merged[1:]):
        firstpage = current[0].page
        lastpage = after[0].page if after else utila.INF
        for item in flat:
            # TODO: lastpage expect that largenumber starts on a new page
            if firstpage <= item.page < lastpage:
                current.append(item)
    # give debug information
    utila.debug('merge firstlevel into extraction without firstlevel')
    utila.debug(largenumber)
    return merged


def remove_invalids(items: list, second: bool = False) -> list:
    result = []
    for item, strategy in zip(items, words.headlines.machine.STRATEGIES):
        utila.debug(strategy.__name__)
        if too_many_error(item, second=second):
            result.append([])
            continue
        if invalid_extraction(item):
            result.append([])
            continue
        result.append(item)
    return result


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
    >>> patch('d.')
    4
    >>> patch('Kapitel 6:') # TODO: SHOULD RETURN 1?
    6
    """
    if not raw:
        return None
    if 'KAPITEL' in raw.upper():
        matched = re.match(r'KAPITEL (\d)', raw, re.IGNORECASE)
        if matched:
            return int(matched[1])
    splitted = [item for item in raw.rsplit('.') if item]
    if not splitted:
        return None
    with contextlib.suppress(ValueError):
        last = splitted[-1]
        for index, char in enumerate('abcdefgh', start=1):
            last = last.replace(char, str(index))
        return int(last)
    return 0


LEVELONE_IN_A_ROW_MAX = configo.HV_INT_PLUS(default=4)

INVALID_ENDING_MAX = configo.HolyTable(
    [
        (0, 1),
        (10, 2),
        (50, 7),
        (120, 10),
    ],
    strategy=utila.Strategy.LINEARISE,
    right_outranges_none=False,
)


def invalid_extraction(headlines) -> bool:
    """Judge extracted strategy and decide if result can be valid.

    1. Strategy: Check longest sequence of level one headlines.
    2. Strategy: Check headline ends with awkward characters.
    """
    headlines = utila.flatten(headlines)
    if all(item.level == 1 for item in headlines):
        # level one extraction strategy
        return False
    # too many level ones in a row
    levels = [item.level for item in headlines if item.level is not None]
    grouped = utila.groupby_diff(levels, maxdiff=0, sort=False)
    longest_levelone = utila.longest([item for item in grouped if item[0] == 1])
    if len(longest_levelone) > LEVELONE_IN_A_ROW_MAX:
        utila.debug('skip invalid extraction, too many first levels in a row')
        return True
    # too many invalid characters at title end
    titles = [item.title.lower().strip() for item in headlines]
    invalid_endings = len([item for item in titles if item[-1] in ',./;:)-'])
    if invalid_endings > INVALID_ENDING_MAX(len(titles)):
        utila.debug(f'skip invalid extraction: {invalid_endings} {len(titles)}')
        return True
    return False


ERROR_MAX = configo.HolyTable(
    [
        (0, 0),
        (10, 1),
        (20, 2),
        (30, 4),
        (50, 6),
        (70, 7),
        (90, 9),
        (100, 10),
        (120, 12),
    ],
    strategy=utila.Strategy.LOWER,
    left_outranges_none=False,
    right_outranges_none=False,
)
# give some tolerance if first appraoch was not good enough
ERROR_MAX_PLUS = configo.HV_PERCENT_PLUS(default=150)


def too_many_error(headlines, second: bool = False) -> bool:
    if not headlines:
        return False
    headline_count = len(utila.flatten(headlines))
    if headline_count < 10:  # TODO: MAGIC NUMBER
        # TODO: THINK ABOUT THIS
        # disable check for too few headlines
        return False
    error = score_levelerror(headlines)
    error_max = ERROR_MAX(headline_count)
    if second:
        # increase max error rate
        error_max = int(error_max * ERROR_MAX_PLUS)
    if error <= error_max:
        # valid extraction
        return False
    utila.debug('skip invalid, too many error: '
                f'{error}/{error_max}:{headline_count}:second:{second}')
    return True
