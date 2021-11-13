# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import functools
import os
import typing

import configo
import iamraw
import iamraw.path
import magic.path
import serializeraw
import texmex
import utila

import words.boxed
import words.feature.headlines
import words.feature.word
import words.headlines
import words.lookup
import words.path


@dataclasses.dataclass
class TextRequiredResources:
    border: iamraw.Border
    boxes: words.boxed.BoxedChecker
    lists: 'ListLookUp'
    fontstore: iamraw.FontStore
    headlines: iamraw.PagesHeadlineList
    textnavigators: texmex.PageTextContentNavigators
    magics: words.lookup.PageLineLookup = None
    formulas: iamraw.PageContentRawFormulas = None


@functools.lru_cache(configo.CACHE_SMALL)
def load_resources(  # pylint:disable=R0914,R0913
    text: str,
    textposition: str,
    fontheader: str,
    fontcontent: str,
    headlines: str,
    pagesizes: str,
    boxes: str,
    lists: str,
    headerfooters: str,
    magics: str = None,
    formulas: str = None,
    pages=None,
) -> TextRequiredResources:
    """Load content from path and create required object"""

    # TODO: CHECK REALY REQUIRED RESOURCES AND REMOVE NON REQUIRED
    ptcns = serializeraw.ptcn_fromfile(
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
    boxed = words.boxed.BoxedChecker(boxes)

    if os.path.exists(lists):
        lists = serializeraw.load_lists(lists, pages=pages)
    else:
        utila.log(f'skip loading lists: {lists}')
        lists = []
    if utila.exists(formulas):
        formulas = serializeraw.load_rawformulas(formulas, pages=pages)
    else:
        utila.log(f'skip loading formulas: {formulas}')
        formulas = []
    lists = words.feature.word.ListLookUp(lists)  # pylint:disable=R0204
    magics = words.lookup.magics_frompath(
        path=magics,
        pages=pages,
    )
    fontstore = serializeraw.create_fontstore(fontheader, fontcontent)
    border = {navigator.page: navigator.content for navigator in ptcns}
    result = TextRequiredResources(
        border=border,
        boxes=boxed,
        lists=lists,
        fontstore=fontstore,
        headlines=headlines,
        textnavigators=ptcns,
        magics=magics,
        formulas=formulas,
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
    # oneline_text = iamraw.path.text(path, prefix='oneline')
    # oneline_textposition = iamraw.path.textposition(path, prefix='oneline')
    # oneline_fontheader = iamraw.path.fontheader(path, prefix='oneline')
    # oneline_fontcontent = iamraw.path.fontcontent(path, prefix='oneline')
    # section = sections.path.sections_(path)
    sizeandborder = iamraw.path.sizeandborder(path)
    boxes = iamraw.path.boxed(path)
    headerfooters = iamraw.path.headerfooters(path)
    lists = words.path.lists(path)
    headlines = words.path.headlines(path)
    magics = magic.path.content_oneline(path)

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
        magics=magics,
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
