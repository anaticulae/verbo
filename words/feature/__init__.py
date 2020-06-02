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
import typing

import configo
import groupme.path
import iamraw
import iamraw.path
import sections.path
import serializeraw
import texmex

import words.boxed
import words.feature.headlines
import words.headlines


@dataclasses.dataclass
class TextRequiredResources:
    border: iamraw.Border
    boxes: words.boxed.BoxedChecker
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
        headerfooters: str,
        pages=None,
) -> TextRequiredResources:
    """Load content from path and create required object"""

    # TODO: CHECK REALY REQUIRED RESOURCES AND REMOVE NON REQUIRED
    textnavigators = serializeraw.create_pagetextcontentnavigators_fromfile(
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

    fontstore = serializeraw.create_fontstore(fontheader, fontcontent)

    contentborder = serializeraw.load_pageborders(pagesizes, pages=pages)

    headerfooters = serializeraw.load_headerfooter(
        headerfooters,
        pages=pages,
    )

    border = words.headlines.contentborder(
        contentborder,
        headerfooters,
    )

    boxed = words.boxed.BoxedChecker(boxes)

    result = TextRequiredResources(
        border=border,
        boxes=boxed,
        fontstore=fontstore,
        headlines=headlines,
        textnavigators=textnavigators,
    )
    return result


@functools.lru_cache(configo.CACHE_SMALL)
def load_resources_frompath(
        path: str,
        pages: tuple = None,
) -> TextRequiredResources:
    text = iamraw.path.text(path)
    textposition = iamraw.path.textposition(path)
    fontheader = iamraw.path.fontheader(path)
    fontcontent = iamraw.path.fontcontent(path)
    section = sections.path.sections_(path)
    sizeandborder = iamraw.path.sizeandborder(path)
    boxes = iamraw.path.boxed(path)
    headerfooters = groupme.path.headerfooters(path)

    headlines = words.feature.headlines.work(
        sectionlist=section,
        text=text,
        text_position=textposition,
        font_header=fontheader,
        font_content=fontcontent,
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
