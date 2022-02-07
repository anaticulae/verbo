# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
TODO: DO NOT MIX STRATEGYS

TODO: New concept:

Collect all title, cluster them by size and font distance and derivate the
headline level out of these information. Use further text information out of
headline.
"""

import typing

import serializeraw
import utila

import words.headlines
import words.headlines.improve.levelfour
import words.headlines.judge
import words.headlines.machine
import words.lookup


def run(  # pylint:disable=R0913,R0914
    sectionlist: str,
    textx: str,
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
    magics: str = None,
    pages: tuple = None,
) -> typing.Tuple[str, str]:
    """Extract headlines out of data."""
    normal = headlines_step(
        sectionlist,
        textx,
        text_position,
        font_header,
        font_content,
        sizeandborder,
        headerfooters,
        magics,
        pages=pages,
    )
    oneline = headlines_step(
        sectionlist,
        oneline_text,
        oneline_text_position,
        oneline_font_header,
        oneline_font_content,
        sizeandborder,
        headerfooters,
        magics,
        pages=pages,
    )
    return normal, oneline


def headlines_step(
    sectionslist,
    text,
    textpositions,
    fontheader,
    fontcontent,
    sizeandborder,
    headersfooters,
    magics,
    pages,
):
    result = extract_headlines(
        sectionslist,
        text,
        textpositions,
        fontheader,
        fontcontent,
        sizeandborder,
        headersfooters,
        magics,
        pages=pages,
    )
    result = words.headlines.judge.run(result)
    if not has_levelfour(result):
        textnavigators = serializeraw.ptcn_fromfile(
            text=text,
            textpositions=textpositions,
            sizeandborderpath=sizeandborder,
            headerfooterpath=headersfooters,
            fontheader=fontheader,
            fontcontent=fontcontent,
            pages=pages,
        )
        # only extract level four headlines if result does not contain any
        # 4.1.2.3 levels.
        levelfour = words.headlines.improve.levelfour.headlines(textnavigators)
        valid = words.headlines.improve.levelfour.valid_levelfour(
            result, levelfour)
        if levelfour and valid:
            result = merge_levelfour(result, levelfour)
    return result


def extract_headlines(
    sections_,
    text,
    textposition,
    fontheader,
    fontcontent,
    sizeandborder,
    headerfooters,
    magics=None,
    pages: tuple = None,
):
    ptcns = serializeraw.ptcn_fromfile(
        text,
        textposition,
        sizeandborder,
        headerfooters,
        fontheader,
        fontcontent,
        pages=pages,
    )
    sectionlist = serializeraw.load_sections(sections_, pages=pages)
    fontstore = serializeraw.create_fontstore(
        fontheader,
        fontcontent,
        pages=pages,
    )
    magics = words.lookup.magics_frompath(
        path=magics,
        pages=pages,
    )
    result = words.headlines.machine.headlines(
        ptcns,
        sectionlist,
        fontstore=fontstore,
        chapters=None,
        magics=magics,
        pages=pages,
    )
    return result


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
    utila.debug('merge_levelfour')
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
