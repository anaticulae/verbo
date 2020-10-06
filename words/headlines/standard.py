# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import re

import groupme.toc.group
import iamraw
import utila

import words.headlines

SMALLEST_HEADLINE_DISTANCE = 1.05  # TODO: HOLY VALUE
SMALLEST_HEADLINE_TEXTSIZE = 1.0

MAX_HEADLINE_TEXTFEED = 0.0  # TODO: HOLY VALUE


class StandardHeadlineExtractor(words.headlines.HeadlineExtractorStrategy):

    def smallest_headlinedistance(self):
        return utila.roundme(self.textdistance * SMALLEST_HEADLINE_DISTANCE)

    def smallest_textsize(self):
        return utila.roundme(self.textsize * SMALLEST_HEADLINE_TEXTSIZE)

    def should_skip(
            self,
            distance_tosmall,
            headline_tosmall,
            textfeed,
            lastitem,
    ):
        if textfeed > MAX_HEADLINE_TEXTFEED:
            # skip numbered lists
            return True

        if distance_tosmall:
            return True

        if headline_tosmall:
            return True
        return False

    def filter(self, items):
        items = super().filter(items)
        items = filter_headlines(items)
        return items


def filter_headlines(items: iamraw.PagesHeadlineList):
    if isinstance(items, list):
        items = {index: value for index, value in enumerate(items)}
    result = collections.defaultdict(list)
    for chapter, content in items.items():
        chapter_headlines = []
        for headline in content:
            if headline.title.count('.') > 5:
                # Skip toc line entries
                continue
            parsed = parse_headline(headline.title)
            if parsed:
                raw_level = parsed['level']
                headline.level = groupme.toc.group.numbered_level(raw_level)
                headline.raw_level = raw_level
                headline.title = headline.title.replace(raw_level, '').strip()
                chapter_headlines.append(headline)
                continue
            if headline.title in words.headlines.WHITELIST:
                chapter_headlines.append(headline)
                continue
        result[chapter].extend(chapter_headlines)
    # require KeyError
    result = dict(result)  # pylint:disable=R0204
    return result


# TODO: CODE DUPLICATION, COLLECT DIFFERENT HEADLINE PARSING APPROACHES
# AND CONVERT TO SINGLE ONE.
HEADLINE = re.compile(
    ('^'
     r'(?P<level>(\d{1,2}\.?)+\d{0,2})'
     r'[ ]{1,5}'
     r'(?P<text>.+?)'
     '$'),
    re.VERBOSE,
)


def parse_headline(line):
    line = line.strip()
    return re.match(HEADLINE, line)
    parsed = whs.parse_headline(raw)
