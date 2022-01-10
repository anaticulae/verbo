# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import words.headlines.strategies.multiline
import words.headlines.strategies.standard
import words.headlines.utils


def filter_headlines(items):  # pylint:disable=R0201
    """Convert level etc."""
    # TODO: IMprove this
    result = {}
    for number, chapter in items.items():
        # skip `normal` headlines, we want to analyze NoLevelHeadlines
        items = [
            item for item in chapter
            if not words.headlines.utils.parse_headline(item.title)
        ]
        result[number] = items
    # TODO: USE DICT CONVERTER HERE
    result = words.headlines.strategies.multiline.filter_headlines(result)
    return result


def should_skip(distance_tosmall, headline_tosmall, **kwargs):  # pylint:disable=W0613
    if distance_tosmall and headline_tosmall:
        return True
    if headline_tosmall:
        return True
    return False


def extract_headline(**kwargs):
    kwargs['textdistance'] = kwargs['textdistance'] * 1.2
    kwargs['textsize'] = kwargs['textsize'] * 1.05
    return words.headlines.strategies.standard.extract_headline(
        **kwargs,
        skipper=should_skip,
    )
