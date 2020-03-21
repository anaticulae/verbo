# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Example driven programming:

for chapter in document:
    for headline in chapter:
        p(headline)

Required resources:
    sections
    text
    font?

TODO: DO NOT MIX STRATEGYS

TODO: New concept:

Collect all title, cluster them by size and font distance and derivate the
headline level out of these information. Use further text information out of
headline.
"""

import collections

import serializeraw
import utila

import words.headlines
import words.headlines.multiline
import words.headlines.nolevel
import words.headlines.standard

PageContentBoxed = collections.namedtuple('PageContentBoxed', 'page content')


@utila.checkdatatype
def work(
        sections: str,
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        sizeandborder: str,
        boxes: str,  # pylint:disable=W0613
        headerfooters: str,
        pages=None,
) -> str:
    """Extract headlines out of data."""
    loaded = words.loader.basic.load_basic(
        text,
        text_position,
        font_header,
        font_content,
        sizeandborder,
        headerfooters,
        pages=pages,
    )
    sections = serializeraw.load_sections(sections, pages=pages)

    strategies = [
        words.headlines.multiline.MultiLine,
        words.headlines.nolevel.NoLevelHeadlineExtractor,
        words.headlines.standard.StandardHeadlineExtractor,
    ]
    results = [
        strategy(
            basic=loaded,
            sectionlist=sections,
            chapters=None,
        ).result(pages=pages) for strategy in strategies
    ]
    extracted = judge_result(results)
    # save
    dumped = serializeraw.dump_headlines(extracted)
    return dumped


def judge_result(results):
    # TODO: add judeging unit
    extracted = results[1]
    if any([len(item) for item in results[0]]):
        extracted = results[0]
    return extracted
