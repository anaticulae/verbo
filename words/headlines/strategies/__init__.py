# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import re
import statistics

import configo
import elements
import elements.headline
import iamraw
import texmex

import words.headlines
import words.headlines.utils as whu

SMALLEST_HEADLINE_DISTANCE = 1.05  # TODO: HOLY VALUE
SMALLEST_HEADLINE_TEXTSIZE = 1.0

MAX_HEADLINE_TEXTFEED = 0.0  # TODO: HOLY VALUE

HEADLINE_MIN_LENGTH = configo.HV_INT_PLUS(7).value
HEADLINE_WORDCOUT_MAX = 20


def headline_decoration(navigator, containerid: int) -> int:
    if not navigator:
        # HACK
        return None
    before = navigator[containerid - 1] if containerid > 0 else None
    # after = navigator[containerid + 1] if containerid + 1 < len(navigator) else None
    if before and elements.headline.noheadline_pattern(before.text):
        return containerid - 1
    return None


def filter_headlines(items: iamraw.PagesHeadlineList):
    if isinstance(items, list):
        items = {index: value for index, value in enumerate(items)}
    result = collections.defaultdict(list)
    for chapter, content in items.items():
        chapter_headlines = []
        for headline in content:
            if headline.title.count('.') > 5 or '. .' in headline.title:
                # Skip toc line entries
                continue
            parsed = whu.parse_headline(headline.title)
            if parsed:
                raw_level = parsed['level']
                headline.level = elements.level_numbered(raw_level)
                headline.raw_level = raw_level
                headline.title = headline.title.replace(raw_level, '').strip()
                chapter_headlines.append(headline)
                continue
            if headline.decoration is not None:
                # Kapitel 1\nEinleitung
                headline.level = 1  # pylint:disable=R0204
                chapter_headlines.append(headline)
                continue
            if elements.isheadline(headline.title):
                chapter_headlines.append(headline)
                continue
        result[chapter].extend(chapter_headlines)
    # require KeyError
    result = dict(result)  # pylint:disable=R0204
    return result


def issentence(line: str):
    # TODO: IMPROVE THIS
    # TODO: USE BIG FIVE FEATURES
    return line.strip().endswith('.')
