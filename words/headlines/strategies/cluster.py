# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Cluster Strategy
================

Hint: THIS STRATGY INVOCATION IS A HACK TO PASS THE STRATEGY. WE MUST
      THINK THIS OVER.
"""

import collections

import configo
import doctextstyle.features
import doctextstyle.features.headline
import doctextstyle.parser
import doctextstyle.utils
import elements
import iamraw
import utila

import words.headlines.strategies
import words.headlines.strategies.multiline
import words.headlines.strategies.singlepage

HEADLINE_WORDCOUT_MAX = configo.HV_INT_PLUS(default=20)


def filter_headlines(parsed) -> dict:
    flat = utila.flatten(parsed.values())
    flat = doctextstyle.utils.flatten(flat)
    headlines = doctextstyle.features.headline.headlines(
        flat,
        returncluster=True,
        distance_before_min=1.05,
        distance_after_min=0.80,
    )
    if not headlines:
        utila.error('empty headlines for strategy cluster')
        return {}
    clusters = [cluster for cluster in headlines[1] if valid_cluster(cluster)]
    clusters = [{item.hashed for item in level} for level in clusters]
    result = collections.defaultdict(list)
    for number, chapter in parsed.items():
        for page in chapter:
            for containerid, line in enumerate(page.hashed):
                current = headline_level(line, clusters)
                if current is None:
                    continue
                parsed = words.headlines.strategies.multiline.parse_headline(line) # yapf:disable
                if parsed:
                    title, level, rawlevel = parsed
                else:
                    title, level, rawlevel = line, current + 1, ''
                headline = iamraw.Headline(
                    title=title,
                    level=level,
                    page=page.page,
                    raw=line,
                    raw_level=rawlevel,
                    container=containerid,
                )
                result[number].append(headline)
    # enable KeyError
    result: dict = dict(result)
    return result


def headline_level(line, clusters) -> int:
    current = search_level(line, clusters)
    if current == -1:
        return None
    # TODO: MOVE TO doctextstyle.features
    if elements.noheadline(
            line,
            wordcount_max=HEADLINE_WORDCOUT_MAX,
    ):
        return None
    return current


def check_surrounding(headlines: dict, ptcns):
    for headline in utila.flatten(headlines.values()):
        headline_expand(
            headline,
            ptcn=utila.select_page(ptcns, page=headline.page),
        )
    return headlines


def second_try(headlines: dict, ptcns):
    singlepage = words.headlines.strategies.singlepage.pagewise(ptcns=ptcns)
    for headline in singlepage:
        for chapter in headlines.values():
            if headline_insert(chapter, headline):
                break
    return headlines


def headline_insert(chapter: list, headline: iamraw.Headline) -> bool:
    if not chapter:
        return False
    if headline in chapter:
        utila.debug(f'already detected: {headline}')
        return True
    start, end = chapter[0].page, chapter[-1].page
    if start <= headline.page <= end:
        chapter.append(headline)
        # sort by container and page
        chapter.sort(key=lambda x: x.start)
        chapter.sort(key=lambda x: x.page)
        return True
    return False


def headline_expand(headline, ptcn):
    container = headline.container
    current = ptcn[container]
    # before = ptcn[container - 1] if container > 0 else None
    after = ptcn[container + 1] if container - 1 < len(ptcn) else None
    merge_after = after and (utila.near(
        current=after.bounding_mean,
        expected=current.bounding_mean,
        diff=2.0,
    )) and current.style.fontid == after.style.fontid
    if merge_after:
        headline.title = f'{headline.title} {after.text}'
        headline.raw = f'{headline.raw} {after.text}'
        headline.container = (headline.container, container + 1)


NO_HEADLINE_CHARS = '+_'

SPECIAL_RATE_MAX = configo.HV_PERCENT_PLUS(default=25.0)


def valid_cluster(cluster) -> bool:
    content = {item.hashed for item in cluster}
    # unique = len(content)
    special = special_char_rate(content, specials=NO_HEADLINE_CHARS)
    if special > SPECIAL_RATE_MAX:
        return False
    return True


def special_char_rate(items, specials: str = '') -> float:
    # TODO: MOVE TO UTILA
    if not items:
        return 0.0
    special = [item for item in items if any(char in item for char in specials)]
    return len(special) / len(items)


def extract_page(data, page):
    ptcn = utila.select_page(data.ptcns, page=page)
    parsed = doctextstyle.parser.parse(ptcn, magic=[])
    return [parsed]


def search_level(line, clusters):
    # TODO: ADD MECHANISM TO CHECK IF ITEM IS NEAR TO CLUSTER TO FIND
    # MORE HEADLINES
    for index, cluster in enumerate(clusters):
        if line in cluster:
            return index
    return -1
