# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This module provides an easy access the textual structure of an
document. The access is described below:

.. code-block:: python

    for chapter in content:
        p(chapter.title)
        for paragraph in chapter:
            p(paragraph.title)
            p(paragraph.number)
            for sentence in paragraph:
                p('word cout: %d' % len(sentence))
                for word in sentence:
                    p(word)

word

word.font
word.font.color
word.font.size
word.style = [i, b, u, strong? etc?]
"""

import serializeraw

import words.boxed
import words.feature
import words.headlines
import words.text.chapter


def work(  # pylint:disable=R0913
    textx: str,
    textposition: str,
    fontheader: str,
    fontcontent: str,
    headliner: str,
    pagesizes: str,
    headerfooters: str,
    boxes: str,
    lists: str,
    magics: str = None,
    pages: tuple = None,
) -> str:
    """Extract textual structure out of document. A text is structured
    in chapter, sections, paragraphs, sentences and words.

    Args:
        textx(str): path to text extraction from rawmaker
        textposition(str): path to textposition matching with text-extraction
        fontheader(str): table with all fonts in document
        fontcontent(str): font definition for every word
        headliner(str): path to extracted headlines from words
        pagesizes(str): path to size and border
        boxes(str): definition of boxed rectangles
        lists(str): definition of lists path
        headerfooters(str): path to extracted footer and header
        magics(str): path to optional magic file
        pages: list of page numbers to process
    Returns:
        dumped paragraphs
    """
    resources = words.feature.load_resources(
        boxes=boxes,
        lists=lists,
        fontcontent=fontcontent,
        fontheader=fontheader,
        headerfooters=headerfooters,
        headlines=headliner,
        pagesizes=pagesizes,
        text=textx,
        textposition=textposition,
        magics=magics,
        pages=pages,
    )

    extracted = words.text.chapter.extract_texts(resources)

    dumped = serializeraw.dump_text(extracted)
    return dumped
