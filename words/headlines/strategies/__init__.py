# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import elements
import iamraw

import words.headlines.utils


def filter_headlines(items: iamraw.PagesHeadlineList):
    if isinstance(items, list):
        items = dict(enumerate(items))
    result = collections.defaultdict(list)
    for chapter, content in items.items():
        chapter_headlines = []
        for headline in content:
            if headline.title.count('.') > 5 or '. .' in headline.title:
                # Skip toc line entries
                continue
            parsed = words.headlines.utils.parse_headline(headline.title)
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
