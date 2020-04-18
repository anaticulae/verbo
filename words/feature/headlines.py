# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Headlines
=========

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

import iamraw.path
import sections.path
import serializeraw
import utila

import words.headlines
import words.headlines.multiline
import words.headlines.nolevel
import words.headlines.standard

PageContentBoxed = collections.namedtuple('PageContentBoxed', 'page content')


@utila.checkdatatype
def work(
        sectionlist: str,
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        sizeandborder: str,
        boxes: str,  # pylint:disable=W0613
        headerfooters: str,
        pages: tuple = None,
) -> str:
    """Extract headlines out of data."""
    results = extract_headlines(
        sectionlist,
        text,
        text_position,
        font_header,
        font_content,
        sizeandborder,
        headerfooters,
        pages=pages,
    )
    extracted = judge_result(results)
    # dump
    dumped = serializeraw.dump_headlines(extracted)
    return dumped


def extract_headlines(
        sections_,
        text,
        textposition,
        fontheader,
        fontcontent,
        sizeandborder,
        headerfooters,
        pages: tuple = None,
):
    loaded = words.loader.basic.load_basic(
        text,
        textposition,
        fontheader,
        fontcontent,
        sizeandborder,
        headerfooters,
        pages=pages,
    )
    sectionlist = serializeraw.load_sections(sections_, pages=pages)

    strategies = [
        words.headlines.multiline.MultiLine,
        words.headlines.nolevel.NoLevelHeadlineExtractor,
        words.headlines.standard.StandardHeadlineExtractor,
    ]
    results = [
        strategy(
            basic=loaded,
            sectionlist=sectionlist,
            chapters=None,
        ).result(pages=pages) for strategy in strategies
    ]
    return results


def judge_result(results):
    # TODO: add judeging unit
    extracted = results[1]
    if any([len(item) for item in results[0]]):
        extracted = results[0]
    return extracted


def headlines_frompath(path: str, prefix: str = '', pages: tuple = None):
    sections_ = sections.path.sections_(path, prefix=prefix)
    text = iamraw.path.text(path, prefix=prefix)
    textposition = iamraw.path.textposition(path, prefix=prefix)
    fontheader = iamraw.path.fontheader(path, prefix=prefix)
    fontcontent = iamraw.path.fontcontent(path, prefix=prefix)
    sizeandborder = iamraw.path.sizeandborder(path, prefix=prefix)
    headerfooters = iamraw.path.headerfooters(path, prefix=prefix)

    extracted = extract_headlines(
        sections_,
        text,
        textposition,
        fontheader,
        fontcontent,
        sizeandborder,
        headerfooters,
        pages=pages,
    )
    result = judge_result(extracted)
    return result
