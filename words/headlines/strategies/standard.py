# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import groupme.toc.group
import iamraw
import texmex

import words.headlines.standard as whs
import words.headlines.strategies


def extract_headline(
        textinfo,
        textdistances,
        textfeeds,
        ptcn: texmex.PageTextContentNavigator,
        containerid: int,
        **kwargs,
):  # pylint:disable=R0914
    text = textinfo.text
    fontdistance = textdistances[containerid + 1]
    if containerid:
        # for non page start check distance before and after
        fontdistance += textdistances[containerid]
        fontdistance = fontdistance / 2.0

    textfeed = textfeeds[containerid]
    textsize = texmex.TextStyle.textsizes(textinfo.style)

    distance_tosmall = fontdistance < kwargs['textdistance']
    headline_tosmall = textsize < kwargs['textsize']

    level = groupme.toc.group.numbered_level(text)
    # print(text.strip(), level)
    higher_equalthree = level is not None and level >= 3
    if higher_equalthree:
        # deactivate distance check for 3.1.1. etc. cause it is a very
        # expressive pattern and these headlines can be very small.
        distance_tosmall = False
        headline_tosmall = False

    lastitem = (containerid + 1) == len(ptcn)
    if len(text) < words.headlines.strategies.HEADLINE_MIN_LENGTH:
        return None

    skip = should_skip(
        distance_tosmall=distance_tosmall,
        headline_tosmall=headline_tosmall,
        textfeed=textfeed,
        lastitem=lastitem,
    )

    if words.headlines.strategies.headline_blacklisted(text):
        return None

    if skip and not higher_equalthree:
        return None

    dist_top = textdistances[containerid]
    dist_bottom = None if lastitem else textdistances[containerid + 1]

    style = dict(
        textsize=textsize,
        before=dist_top,
        after=dist_bottom,
        feed=textfeed,
    )
    decoration = words.headlines.strategies.headline_decoration(
        navigator=ptcn,
        containerid=containerid,
    )
    headline = iamraw.Headline(
        container=containerid,
        level=style,
        page=ptcn.page,
        raw=text.strip(),
        title=text.strip(),
        decoration=decoration,
    )
    return headline


def should_skip(
        distance_tosmall,
        headline_tosmall,
        textfeed,
        lastitem,  # pylint:disable=W0613
):
    if textfeed > words.headlines.strategies.MAX_HEADLINE_TEXTFEED:
        # skip numbered lists
        return True

    if distance_tosmall:
        return True

    if headline_tosmall:
        return True
    return False


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
            parsed = whs.parse_headline(headline.title)
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
