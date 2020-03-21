# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Example:

* high notes: ^1 ^2 ^3

"""

import serializeraw
import texmex

import words.feature
import words.text
import words.text.chapter
import words.text.sentence


def work(
        text: str,
        textposition: str,
        fontheader: str,
        fontcontent: str,
        headlines: str,
        pagesizes: str,
        boxes: str,
        headerfooters: str,
        pages: tuple = None,
) -> str:
    """Extract highnotes out of words.

    Args:
        text(str): path to text extraction from rawmaker
        textposition(str): path to textposition matching with text-extraction
        fontheader(str): table with all fonts in document
        fontcontent(str): font definition for every word
        headlines(str): path to extracted headlines from hey/words
        pagesizes(str): path to size and border
        boxes(str): definition of boxed rectangles
        headerfooters: path to extracted footer and header
        pages: list of page numbers to process
    Returns:
        dumped highnotes
    """
    resources = words.feature.load_resources(
        boxes=boxes,
        fontcontent=fontcontent,
        fontheader=fontheader,
        headerfooters=headerfooters,
        headlines=headlines,
        pagesizes=pagesizes,
        text=text,
        textposition=textposition,
        pages=pages,
    )

    extracted = extract_highnotes(resources)

    dumped = serializeraw.dump_highnotes(extracted)
    return dumped


def extract_highnotes(loaded: words.feature.TextRequiredResources,
                     ) -> words.text.PageContentPageTextDetecteds:
    """Iterate thrue document via headline and process the content
    between the headlines. Extract highnotes to find links to footer.

    Args:
        loaded: resources provided by text module
    Returns:
        list of text pages with textutal content definition
    """
    loaded = words.text.chapter.split(loaded)

    result = []
    for page in loaded:
        parsed = []
        for headline, content in words.text.sentence.visit_sections(page):
            highnotes = texmex.highnotes(content)
            parsed.extend(highnotes)
        if not parsed:
            continue
        result.append(
            texmex.PageContentTextItems(
                page=page.page,
                content=parsed,
            ))
    return result
