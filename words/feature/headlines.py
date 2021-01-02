# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
import typing

import iamraw.path
import sections.path
import serializeraw
import utila

import words.headlines
import words.headlines.judge
import words.headlines.levelfour
import words.headlines.machine

PageContentBoxed = collections.namedtuple('PageContentBoxed', 'page content')


@utila.checkdatatype
def work(  # pylint:disable=R0913,R0914
        sectionlist: str,
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        oneline_text: str,
        oneline_text_position: str,
        oneline_font_header: str,
        oneline_font_content: str,
        sizeandborder: str,
        boxes: str,  # pylint:disable=W0613
        headerfooters: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
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
    extracted = words.headlines.judge.run(results)

    oneline_results = extract_headlines(
        sectionlist,
        oneline_text,
        oneline_text_position,
        oneline_font_header,
        oneline_font_content,
        sizeandborder,
        headerfooters,
        pages=pages,
    )
    oneline_extracted = words.headlines.judge.run(oneline_results)

    textnavigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=text,
        textpositions=text_position,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooters,
        fontheader=font_header,
        fontcontent=font_content,
        pages=pages,
    )

    if not has_levelfour(extracted):
        # only extract level four headlines if result does not contain any
        # 4.1.2.3 levels.
        levelfour_ = words.headlines.levelfour.headlines(textnavigators)
        valid = words.headlines.levelfour.valid_levelfour(extracted, levelfour_)
        if levelfour_ and valid:
            extracted = merge_levelfour(extracted, levelfour_)
    # dump
    dumped = serializeraw.dump_headlines(extracted)
    oneline_dumped = serializeraw.dump_headlines(oneline_extracted)
    return dumped, oneline_dumped


def has_levelfour(headlines):
    flat = utila.flatten(headlines)
    maxlevel = max(
        [item.level for item in flat if item.level is not None],
        default=0,
    )
    if maxlevel >= 4:
        return True
    # TODO: USE SMARTER DECIDER, MAY COLLECT HEADLINE DUPLICATON
    # THIS STEP IS REQUIRED WHEN STRATEGY ALREADY PARSE LEVEL FOUR
    # HEADLINES.
    counted = 0
    for headline in flat:
        # Headline(title='A) Einführungsphase', level=3, raw='A)
        # Einführungsphase', raw_level='', page=52, container=21,
        # decoration=None)
        if headline.level == 3 and not headline.raw_level:
            counted += 1
    if counted >= 3:
        return True
    return False


def merge_levelfour(extracted, levelfour):
    result = [item[:] for item in extracted]
    levelfour = levelfour[:]

    def insert(current, result):
        for chapter in result:
            for index, item in enumerate(chapter):
                start = item.container
                if isinstance(start, tuple):
                    start = start[0]
                if current.page > item.page:
                    continue
                if current.page == item.page and current.container > start:
                    continue
                chapter.insert(index, current)
                return

    while levelfour:
        current = levelfour.pop()
        insert(current, result)
    return result


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
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textposition,
        sizeandborder,
        headerfooters,
        fontheader,
        fontcontent,
        pages=pages,
    )
    sectionlist = serializeraw.load_sections(sections_, pages=pages)

    result = words.headlines.machine.headlines(
        ptcns,
        sectionlist,
        chapters=None,
        pages=pages,
    )
    return result


def score_headlines(items):
    score = 0
    for item in utila.flatten(items):
        score += len(item.title)
        if item.level is not None:
            # prefer headline with extracted level over headlines without
            # level
            score += len(item.title)
    return score


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
    result = words.headlines.judge.run(extracted)
    return result
