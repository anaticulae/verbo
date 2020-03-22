# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# TODO: IMPROVE NAMING

import dataclasses
import functools

import configo
import groupme.path
import iamraw
import iamraw.path
import serializeraw
import texmex


@dataclasses.dataclass
class BasicRequiredResources:
    sizeandborder: iamraw.PageSizeBorderList
    fontstore: iamraw.FontStore
    textnavigators: texmex.PageTextNavigators
    # TODO: fix iamraw
    headerfooters: iamraw.PageContentFooterHeaders


@functools.lru_cache(configo.CACHE_SMALL)
def load_basic(
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        pagesizes: str,
        headerfooters: str,
        pages=None,
) -> BasicRequiredResources:
    text = serializeraw.load_document(text, pages=pages)
    text_position = serializeraw.load_textpositions(text_position, pages=pages)
    textnavigators = texmex.create_pagetextnavigators(
        text=text,
        text_positions=text_position,
    )

    fontstore = serializeraw.create_fontstore(font_header, font_content)
    sizeandborder = serializeraw.load_pageborders(pagesizes, pages=pages)

    headerfooters = serializeraw.load_headerfooter(
        headerfooters,
        pages=pages,
    )

    result = BasicRequiredResources(
        sizeandborder=sizeandborder,
        fontstore=fontstore,
        textnavigators=textnavigators,
        headerfooters=headerfooters,
    )
    return result


@functools.lru_cache(configo.CACHE_SMALL)
def load_basic_frompath(path: str, pages: tuple = None):
    text = iamraw.path.text(path)
    textposition = iamraw.path.textposition(path)
    fontheader = iamraw.path.fontheader(path)
    fontcontent = iamraw.path.fontcontent(path)
    pagesizes = iamraw.path.sizeandborder(path)
    headerfooters = groupme.path.headerfooters(path)

    loaded = load_basic(
        text=text,
        text_position=textposition,
        font_header=fontheader,
        font_content=fontcontent,
        pagesizes=pagesizes,
        headerfooters=headerfooters,
        pages=pages,
    )
    return loaded
