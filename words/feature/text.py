# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
    """Extract textual structure out of document. A text is structured
    in chapter, sections, paragraphs, sentences and words.

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
        dumped paragraphs
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

    extracted = words.text.chapter.extract_texts(resources)

    dumped = serializeraw.dump_text(extracted)
    return dumped
