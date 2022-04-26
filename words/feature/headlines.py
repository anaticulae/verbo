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
import utila

import words.headlines.run


@utila.checkdatatype
def work(result: str) -> typing.Tuple[str, str]:
    """Extract headlines out of data."""
    result: str = utila.file_read(result)
    # dump
    normal: str = result
    oneline: str = result
    return normal, oneline


def headlines_frompath(path: str, prefix: str = '', pages: tuple = None):
    sections_ = iamraw.path.sections_(path, prefix=prefix)
    text = iamraw.path.text(path, prefix=prefix)
    textposition = iamraw.path.textposition(path, prefix=prefix)
    fontheader = iamraw.path.fontheader(path, prefix=prefix)
    fontcontent = iamraw.path.fontcontent(path, prefix=prefix)
    sizeandborder = iamraw.path.sizeandborder(path, prefix=prefix)
    headerfooters = iamraw.path.headerfooters(path, prefix=prefix)
    magics = iamraw.path.magic_content(path, prefix=prefix)
    # run extraction
    result = words.headlines.run.extract_headlines(
        sections_,
        text,
        textposition,
        fontheader,
        fontcontent,
        sizeandborder,
        headerfooters,
        magics,
        pages=pages,
    )
    return result
