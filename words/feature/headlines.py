# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

"""

import typing

import iamraw
import serializeraw
import utila

import words.headlines.run


@utila.checkdatatype
def work(  # pylint:disable=R0913,R0914
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
    normal, oneline = words.headlines.run.run(
        sectionlist,
        textx,
        text_position,
        font_header,
        font_content,
        oneline_text,
        oneline_text_position,
        oneline_font_header,
        oneline_font_content,
        sizeandborder,
        boxes,
        headerfooters,
        magics,
        pages=pages,
    )
    # dump
    normal: str = serializeraw.dump_headlines(normal)
    oneline: str = serializeraw.dump_headlines(oneline)
    return normal, oneline


def headlines_frompath(path: str, prefix: str = '', pages: tuple = None):
    sections_ = iamraw.path.sections_(path, prefix=prefix)
    text = iamraw.path.text(path, prefix=prefix)
    textposition = iamraw.path.textposition(path, prefix=prefix)
    fontheader = iamraw.path.fontheader(path, prefix=prefix)
    fontcontent = iamraw.path.fontcontent(path, prefix=prefix)
    sizeandborder = iamraw.path.sizeandborder(path, prefix=prefix)
    headerfooters = iamraw.path.headerfooters(path, prefix=prefix)
    # run extraction
    extracted = words.headlines.run.extract_headlines(
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
