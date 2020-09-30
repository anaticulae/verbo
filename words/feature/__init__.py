# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import functools
import os
import typing

import configo
import groupme.path
import iamraw
import iamraw.path
import sections.path
import serializeraw
import texmex
import utila

import words.boxed
import words.feature.headlines
import words.feature.word
import words.headlines
import words.path


@dataclasses.dataclass
class TextRequiredResources:
    border: iamraw.Border
    boxes: words.boxed.BoxedChecker
    lists: 'ListLookUp'
    fontstore: iamraw.FontStore
    headlines: iamraw.PagesHeadlineList
    textnavigators: texmex.PageTextContentNavigators


@functools.lru_cache(configo.CACHE_SMALL)
def load_resources(  # pylint:disable=R0914
        text: str,
        textposition: str,
        fontheader: str,
        fontcontent: str,
        headlines: str,
        pagesizes: str,
        boxes: str,
        lists: str,
        headerfooters: str,
        pages=None,
) -> TextRequiredResources:
    """Load content from path and create required object"""

    # TODO: CHECK REALY REQUIRED RESOURCES AND REMOVE NON REQUIRED
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=text,
        textpositions=textposition,
        sizeandborderpath=pagesizes,
        headerfooterpath=headerfooters,
        fontheader=fontheader,
        fontcontent=fontcontent,
        pages=pages,
    )
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    boxes = serializeraw.load_boxes(boxes, pages=pages)

    if os.path.exists(lists):
        lists = serializeraw.load_lists(lists, pages=pages)
    else:
        utila.log(f'skip loading lists: {lists}')
        lists = []
    lists = words.feature.word.ListLookUp(lists)  # pylint:disable=R0204

    fontstore = serializeraw.create_fontstore(fontheader, fontcontent)

    border = {navigator.page: navigator.content for navigator in ptcns}

    boxed = words.boxed.BoxedChecker(boxes)
    result = TextRequiredResources(
        border=border,
        boxes=boxed,
        lists=lists,
        fontstore=fontstore,
        headlines=headlines,
        textnavigators=ptcns,
    )
    return result


@functools.lru_cache(configo.CACHE_SMALL)
def load_resources_frompath(  # pylint:disable=R0914
        path: str,
        pages: tuple = None,
) -> TextRequiredResources:
    text = iamraw.path.text(path)
    textposition = iamraw.path.textposition(path)
    fontheader = iamraw.path.fontheader(path)
    fontcontent = iamraw.path.fontcontent(path)
    oneline_text = iamraw.path.text(path, prefix='oneline')
    oneline_textposition = iamraw.path.textposition(path, prefix='oneline')
    oneline_fontheader = iamraw.path.fontheader(path, prefix='oneline')
    oneline_fontcontent = iamraw.path.fontcontent(path, prefix='oneline')
    section = sections.path.sections_(path)
    sizeandborder = iamraw.path.sizeandborder(path)
    boxes = iamraw.path.boxed(path)
    headerfooters = groupme.path.headerfooters(path)
    lists = words.path.lists(path)

    headlines, _ = words.feature.headlines.work(
        sectionlist=section,
        text=text,
        text_position=textposition,
        font_header=fontheader,
        font_content=fontcontent,
        oneline_text=oneline_text,
        oneline_text_position=oneline_textposition,
        oneline_font_header=oneline_fontheader,
        oneline_font_content=oneline_fontcontent,
        sizeandborder=sizeandborder,
        boxes=boxes,
        headerfooters=headerfooters,
        pages=pages,
    )

    loaded = load_resources(
        text=text,
        textposition=textposition,
        fontheader=fontheader,
        fontcontent=fontcontent,
        headlines=headlines,
        pagesizes=sizeandborder,
        boxes=boxes,
        headerfooters=headerfooters,
        lists=lists,
        pages=pages,
    )
    return loaded


@functools.lru_cache(configo.CACHE_SMALL)
def load_extracted(
        extracted_text,
        headlines,
        pages=None,
) -> typing.Tuple[typing.List, iamraw.Border]:
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    extracted_text = serializeraw.load_text(
        extracted_text,
        headlines,
        pages=pages,
    )
    return extracted_text, headlines
