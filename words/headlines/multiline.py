# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import statistics

import configo
import german
import groupme.toc.group
import iamraw
import texmex
import utila

import words.headlines
import words.headlines.standard as whs

# longer word chains may be a sentence or something else
MAX_HEADLINE_TOKEN_LENGTH = configo.HV_INT_PLUS(20)
# assume that headlines does not contain many numbers
MAX_NUMBERS_IN_HEADLINE = configo.HV_INT_PLUS(5)

HEADLINE_MEDIAN = configo.HolyTable(  # TODO: HOLY VALUE
    items=[
        (10, 40),
        (12, 35),
        (14, 30),
        (16, 26),
        (22, 16),
    ],
    left_outranges_none=False,
    right_outranges_none=False,
)


class MultiLine(words.headlines.HeadlineExtractorStrategy):

    def should_skip(
            self,
            distance_tosmall,
            headline_tosmall,
            textfeed,
            lastitem,
    ):
        if distance_tosmall and headline_tosmall:
            return True
        if headline_tosmall:
            return True
        return False

    def smallest_headlinedistance(self):
        return 0

    def smallest_textsize(self):
        return utila.roundme(self.textsize)

    def extract_page(
            self,
            pagecontent: texmex.PageTextNavigator,
    ) -> iamraw.Headlines:
        """Extract headlines on selected page

        Args:
            pagecontent: content of page to extract headlines
        Returns:
            Extracted list of iamraw.Headline.
        """
        result = []
        grouped = texmex.group_page_by_size_distance(pagecontent)
        for items in grouped:
            if wrong_position(items):
                continue
            if invalid_headline_group(items):
                continue
            raw = plain(items)
            parsed = parse_headline(raw)
            if not parsed:
                continue
            title, level, rawlevel = parsed
            if noheadline(title):
                continue
            headline = iamraw.Headline(
                container=headline_range(items),
                level=level,
                page=pagecontent.page,
                raw=raw,
                raw_level=rawlevel,
                title=utila.normalize_whitespaces(title),
            )
            result.append(headline)
        return result


def headline_range(items):
    if len(items) == 1:
        # single line headline
        container = items.firstid
    else:
        container = (items.firstid, items.firstid + len(items) - 1)
    return container


def noheadline(text: str) -> bool:
    text = text.strip()
    if not text:
        return True
    if issentence(text):
        # ignore extracted lists which are interpreted as headlines
        return True
    if text.count('.') > 5:
        return True
    wordslength = [len(word) for word in text.split()]
    mean_words_length = statistics.mean(wordslength)
    if mean_words_length <= 3.0:
        return True
    return False


def invalid_headline_group(items) -> bool:
    text = ' '.join([item.text for item in items])
    words_ = german.split_words(text, validate_sentences=False)
    if len(words_) >= MAX_HEADLINE_TOKEN_LENGTH:
        # maybe a sentence cause headlines are not so long
        return True

    number_count = len([item for item in words_ if utila.isnumber(item)])
    if number_count >= MAX_NUMBERS_IN_HEADLINE:  # TODO: HOLY VALUE
        # assume that headlines does not contain many numbers
        return True

    if len(items) >= 2:  # multiline
        # In general, multiline headlines fill the whole line. If this
        # does not happen, it is other content which is false positive
        # parsed as headline.
        line_length = [len(item.text) for item in items.text]
        median = statistics.median(line_length)
        if median <= HEADLINE_MEDIAN(items.size):
            return True
    return False


def issentence(line: str):
    # TODO: IMPROVE THIS
    # TODO: USE BIG FIVE FEATURES
    return line.strip().endswith('.')


def wrong_position(
        items,
        max_x0: float = 200.0,  # HOLY VALUE
) -> bool:
    """We assume that headlines start on the left side of the document.
    This should skip false possitive headline extraction.

    TODO: RUN SECOND EXTRACTION WITHOUT LEFTSTARTED AND COMPARE TO
    SUPPORT RIGHT ALIGNED HEADLINES?
    """
    return items.bounding[0] >= max_x0


def plain(items: list) -> str:
    # TODO: REPLACE WITH UTILA CODE
    raw = ' '.join([item.text.strip() for item in items])
    return raw


def parse_headline(raw: str):
    parsed = whs.parse_headline(raw)
    if parsed:
        rawlevel, title = parsed['level'], parsed['text']
        level = groupme.toc.group.numbered_level(rawlevel)
        if level is False:
            return None
        return title, level, rawlevel
    if raw not in words.headlines.WHITELIST:
        return None
    return raw, None, ''
