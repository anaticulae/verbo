# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import utila


def run(results):
    """\
        1. Compare Multiline and NoLevel - prefer multiline over NoLevel
        2. Compare result of 1. with StandardHeadlineExtractor
    """
    # remove invalid result
    results = [item if not invalid_extraction(item) else [] for item in results]

    best = results[1]
    if any([len(item) for item in results[0]]):
        # if any item is detected with multiline strategy, choose
        # multiline over NoLevelheadline
        best = results[0]

    # longest common text selection
    best_flat = score_headlines(best)
    standard_flat = score_headlines(results[2])

    if best_flat > standard_flat:
        return best
    return results[2]


def score_headlines(items):
    score = 0
    for item in utila.flatten(items):
        score += len(item.title)
        if item.level is not None:
            # prefer headline with extracted level over headlines without
            # level
            score += len(item.title)
    return score


MAX_LEVELONE_IN_A_ROW = configo.HV_INT_PLUS(4).value


def invalid_extraction(headlines) -> bool:
    """Judge extracted strategy and decide if result can be valid.

    1. Strategy: Check longest sequence of level one headlines.
    """
    headlines = utila.flatten(headlines)
    levels = [item.level for item in headlines if item.level is not None]
    grouped = utila.groupby_diff(levels, diff=0, sort=False)  # pylint:disable=unexpected-keyword-arg

    longest_levelone = utila.longest([item for item in grouped if item[0] == 1])
    if len(longest_levelone) > MAX_LEVELONE_IN_A_ROW:  # TODO: HOLY VALUE
        return True
    return False
