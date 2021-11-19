# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elements
import iamraw

import words.headlines.strategies.multiline


def pagewise(ptcns):
    headlines = []
    for page in ptcns:
        parsed = parse_page(page)
        if not parsed:
            continue
        headlines.extend(parsed)
    return headlines


def parse_page(ptcn) -> iamraw.Headlines:
    if len(ptcn) > 4:
        return None
    result = []
    for container, line in enumerate(ptcn):
        if line.bounding_mean < 18.0:
            continue
        if not elements.isheadline(line.text):
            continue
        parsed = words.headlines.strategies.multiline.parse_headline(line.text)
        if parsed:
            title, level, rawlevel = parsed
        else:
            title, level, rawlevel = line, 1, ''
        result.append(
            iamraw.Headline(
                title=title.strip(),
                container=container,
                level=level,
                raw=line.text,
                raw_level=rawlevel,
                page=ptcn.page,
            ))
    return result
