# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import configo
import texmex

SMALLEST_HEADLINE_DISTANCE = 1.05  # TODO: HOLY VALUE
SMALLEST_HEADLINE_TEXTSIZE = 1.0

MAX_HEADLINE_TEXTFEED = 0.0  # TODO: HOLY VALUE

HEADLINE_MIN_LENGTH = configo.HV_INT_PLUS(7).value


def headline_decoration(navigator, containerid: int) -> int:
    if not navigator:
        # HACK
        return None
    before = navigator[containerid - 1] if containerid > 0 else None
    # after = navigator[containerid + 1] if containerid + 1 < len(navigator) else None
    if before and headline_blacklisted(before.text):
        return containerid - 1
    return None


BLACK_CHAPTER = re.compile(r'(Kapitel|Chapter)[ ]{0,5}\d{1,2}', re.IGNORECASE)


def headline_blacklisted(item: str) -> bool:
    """\
    >>> headline_blacklisted('KAPITEL  1 ')
    True
    >>> headline_blacklisted('Chapter 5 ')
    True
    """
    item = item.strip()
    if BLACK_CHAPTER.match(item):
        return True
    return False
