# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
import words.headlines.cluster
import words.headlines.strategies
import words.headlines.utils

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


def extract_page(data, page) -> iamraw.Headlines:
    """Extract headlines on selected page."""
    pagecontent = utila.select_page(data.ptcns, page)
    result = []
    grouped = texmex.group_page_by_size_distance(pagecontent)
    befores = [None] + grouped
    for items, before in zip(grouped, befores):
        if wrong_position(items):
            continue
        if invalid_headline_group(items):
            continue
        raw = plain(items)
        parsed = parse_headline(raw, before)
        if not parsed:
            continue
        title, level, rawlevel = parsed
        if level == 1:
            # first level headline
            if items.size <= 12.0:
                continue
        if words.headlines.strategies.noheadline(title):
            continue
        headline = iamraw.Headline(
            container=headline_range(items),
            level=level,
            page=pagecontent.page,
            raw=raw,
            raw_level=rawlevel,
            title=utila.normalize_whitespaces(title),
        )
        # add decorating if required
        if before:
            before = plain(before)
            chapter = words.headlines.strategies.headline_blacklisted(before)
            if chapter:
                headline.decoration = headline.start - 1
        result.append(headline)
    return result


def headline_range(items):
    if len(items) == 1:
        # single line headline
        container = items.firstid
    else:
        container = (items.firstid, items.firstid + len(items) - 1)
    return container


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


def parse_headline(raw: str, before=None):  # pylint:disable=R0911
    parsed = words.headlines.utils.parse_headline(raw)
    if parsed:
        rawlevel, title = parsed['level'], parsed['text']
        level = groupme.toc.group.numbered_level(rawlevel)
        if level is False:
            return None
        return title, level, rawlevel
    parsed = words.headlines.utils.parse_chapter_level(raw)
    if parsed:
        title, rawlevel = parsed
        level = 1  # pylint:disable=R0204
        if 'anhang' in rawlevel.lower():
            # ANHANG
            #   ANHANG 1: ZUSAMMENFASSUNG
            #   ANHANG 2: SUMMARY
            level = 2
        return title, level, rawlevel
    if words.headlines.isheadline(raw):
        return raw, 1, ''
    if before:
        # look back and check for `Kapitel-X-Pattern`
        before = plain(before)
        chapter = words.headlines.strategies.headline_blacklisted(before)
        if chapter:
            return raw, 1, ''
    if raw not in words.headlines.WHITELIST:
        return None
    return raw, None, ''


def filter_headlines(result: iamraw.PagesHeadlineList) -> int:
    """Convert chapter level based on text distances to logical level
    (1,2,3,4,...).

    Hint: This function updates the level
    TODO: copy items
    """
    utila.call('convert_level')
    if (not result or not any(result.values()) or
            not any([item for item in result.values()])):
        # check that result pages are empty
        utila.info('empty PageHeadlineList')
        return {}
    assert isinstance(result, dict), type(result)

    nolevel = []
    for item in result.values():
        nolevel.extend(item)
    level = [item for item in nolevel if isinstance(item.level, int)]

    if not level:
        result = words.headlines.cluster.cluster_headline_level(result)
    return result
