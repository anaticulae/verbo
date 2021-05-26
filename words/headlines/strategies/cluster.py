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

import doctextstyle.features
import doctextstyle.features.headline
import doctextstyle.parser
import doctextstyle.utils
import elements
import iamraw
import utila

import words.headlines.strategies
import words.headlines.strategies.multiline


def filter_headlines(parsed) -> dict:  # pylint:disable=R0914
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

    _, clusters = headlines
    clusters = [cluster for cluster in clusters if valid_cluster(cluster)]
    clusters = [{item.hashed for item in level} for level in clusters]

    result = collections.defaultdict(list)
    for number, chapter in parsed.items():
        for page in chapter:
            for containerid, line in enumerate(page.hashed):
                current = search_level(line, clusters)
                if current == -1:
                    continue
                if elements.noheadline(
                        line,
                        wordcount_max=words.headlines.strategies.
                        HEADLINE_WORDCOUT_MAX,
                ):
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
    result = dict(result)  # pylint:disable=R0204
    return result


NO_HEADLINE_CHARS = '+_'


def valid_cluster(cluster) -> bool:
    content = {item.hashed for item in cluster}
    # unique = len(content)
    special = special_char_rate(content, specials=NO_HEADLINE_CHARS)
    if special > 0.25:  # TODO: HOLY VALUE
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
