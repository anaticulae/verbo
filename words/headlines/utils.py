# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import texmex
import utila


def document_textdistance(
        navigators: texmex.PageTextContentNavigators,
        digits: int = 1,
) -> float:
    """Determine the most common text distance"""
    result = []
    for navigator in navigators:
        if not navigator:
            # empty page
            continue
        bounds = texmex.textbounds(navigator, navigator.content)
        # ignore empty content
        bounds = [item.bounds for item in bounds if item.text.strip()]
        ydist = [item.bottomdist for item in bounds]
        for yfirst, ysecond in zip(ydist[:-1], ydist[1:]):
            distance = yfirst - ysecond
            result.append(distance)
    result = utila.roundme(result, digits=digits, convert=False)  # pylint:disable=R0204
    mode = utila.modes(result)
    return mode
