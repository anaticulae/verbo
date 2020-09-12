# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import doctextstyle.parser
import iamraw
import texmex
import utila


@dataclasses.dataclass(unsafe_hash=True)
class TextProperty:
    length: int = None
    hashed: str = None
    size: float = None
    font: int = None
    before: float = None
    after: float = None
    top: float = None
    bottom: float = None
    left: float = None
    right: float = None
    page: int = None


@dataclasses.dataclass(unsafe_hash=True)
class PageTextProperties:
    length: int = None
    hashed: int = None
    sizes: float = None
    fonts: int = None
    distances: float = None
    ypos: float = None
    left: float = None
    right: float = None
    page: int = None


iamraw.TextProperty = TextProperty
iamraw.PageTextProperties = PageTextProperties


def textfonts(navi: texmex.NavigatorMixin) -> utila.Ints:
    # TODO: REMOVE AFTER PATCHING HEY
    assert issubclass(navi.__class__, texmex.NavigatorMixin), type(navi)
    collected = []
    for line in navi:
        # TODO: REPLACE WITH char.width
        # determine most common font family
        family = [[char.font] * (char.end - char.start) for char in line.style]
        family = utila.flatten(family)
        collected.append(utila.mode(family))
    return collected


doctextstyle.parser.textfonts = textfonts
