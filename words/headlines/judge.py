# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def run(results):
    """\
        1. Compare Multiline and NoLevel - prefer multiline over NoLevel
        2. Compare result of 1. with StandardHeadlineExtractor
    """
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
