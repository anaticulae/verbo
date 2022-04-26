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

import utila

# TODO: REMOVE LATER


@utila.checkdatatype
def work(result: str) -> typing.Tuple[str, str]:
    """Extract headlines out of data."""
    result: str = utila.file_read(result)
    # dump
    normal: str = result
    oneline: str = result
    return normal, oneline
