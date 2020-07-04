# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import configo
import power
import utila

import words
import words.feature

SEVENTYTWO_FIRSTPAGE = os.path.join(
    words.ROOT,
    'tests/fixtures/master72/seventytwo_firstpage.txt',
)


@functools.lru_cache(configo.CACHE_SMALL)
def textrequired(pages=None):
    return words.feature.load_resources_frompath(
        power.link(power.MASTER072_PDF),
        pages=pages,
    )


def firstpage_sentences():
    assert os.path.exists(SEVENTYTWO_FIRSTPAGE), SEVENTYTWO_FIRSTPAGE

    content = utila.file_read(SEVENTYTWO_FIRSTPAGE)
    splitted = content.split(utila.NEWLINE * 2)

    sentences = [item.replace(utila.NEWLINE, ' ').strip() for item in splitted]
    return sentences
