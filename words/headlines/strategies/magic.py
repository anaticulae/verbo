# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import doctextstyle
import iamraw
import utila

import words.headlines.strategies.multiline
import words.headlines.utils


@utila.selbstwirksamkeit
def document(ptcns, fontstore, magics, pages) -> dict:
    headlines = doctextstyle.headlines_fromdata(
        navigators=ptcns,
        fontstore=fontstore,
        magics=magics,
    )
    headlines = [item if valid_cluster(item) else [] for item in headlines]
    # TODO: SORTING IS NOT REQUIRED?
    flat = sorted(
        utila.flatten(headlines),
        key=lambda x: utila.alphabetically(x.text),
    )
    result = collections.defaultdict(list)
    for page in ptcns:
        for containerid, line in enumerate(page):
            if line not in flat:
                continue
            line = line.text
            parsed = words.headlines.strategies.multiline.parse_headline(line)
            if parsed:
                title, level, rawlevel = parsed
            else:
                title, level, rawlevel = line, -1, ''
            number = len(result) - 1 if level != 1 else len(result)
            headline = iamraw.Headline(
                title=title,
                level=level,
                page=page.page,
                raw=line,
                raw_level=rawlevel,
                container=containerid,
            )
            result[number].append(headline)
    result = dict(result).values()
    return result


def valid_cluster(cluster) -> bool:
    if whitespace_rate(cluster) > 0.15:
        return False
    return True


def whitespace_rate(cluster) -> float:
    charcount = 0
    whitespaces = 0
    for item in cluster:
        charcount += len(item.text)
        whitespaces += item.text.count(' ')
    if not charcount:
        return 0.0
    return whitespaces / charcount
