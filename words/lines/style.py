# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Line Style
==========

Feed
----

* left
* right

Style
-----

* left
* right
* block
* center
* block-center
"""

import dataclasses
import enum
import math
import typing

import texmex
import utila


class TextAlignment(enum.Enum):
    LEFT = enum.auto()
    CENTER = enum.auto()
    RIGHT = enum.auto()
    BLOCK = enum.auto()
    BLOCK_CENTER = enum.auto()
    UNDEFINED = enum.auto()


TextAlignments = typing.List[TextAlignment]


@dataclasses.dataclass
class LineStyleInfo:
    feed_left: float = None
    feed_right: float = None
    alignment: TextAlignment = None


BLOCK_TEXT_DIFF = 10.0  # TODO: HOLY VALUE


def document_alignment(navigators: texmex.PageTextNavigators) -> TextAlignment:
    result = []
    left, right = document_textfeed(navigators)
    for page in navigators:
        # left, right = page.content.left, page.content.right
        style = page_textalignment(page, left, right)
        result.append(style)
    return utila.modes(result)


def document_textfeed(navigators):
    left = texmex.document_textfeed(navigators)
    right = texmex.document_textfeed(navigators, left=False)
    return left, right


TEXT_BORDER_NOISE = 15  # TODO HOLY VALUE


def page_textalignment(navigator, left, right) -> TextAlignment:
    left, right = leftright(navigator, left, right)
    leftzero = zero(left)
    rightzero = zero(right)
    if leftzero >= 0.9 and rightzero >= 0.75:
        return TextAlignment.BLOCK
    if leftzero <= 0.75 and rightzero >= 0.9:
        return TextAlignment.RIGHT
    if leftzero >= 0.75:
        return TextAlignment.LEFT
    return TextAlignment.UNDEFINED


def page_linealignments(
        navigator,
        left_alignment,
        right_alignment,
) -> TextAlignments:
    result = []
    left, right = leftright(navigator, left_alignment, right_alignment)
    for first, second in zip(left, right):
        # TODO: HOLY VALUES
        print(first, second)
        if second == 0.0:
            if first > 100:
                result.append(TextAlignment.RIGHT)
            elif first <= 50:
                result.append(TextAlignment.BLOCK)
        elif second >= 20:
            if first >= 20:
                # left and right textfeed is equal
                if math.fabs(second - first) <= 5.0:
                    result.append(TextAlignment.BLOCK_CENTER)
                else:
                    result.append(TextAlignment.CENTER)
            else:
                result.append(TextAlignment.LEFT)
        else:
            if first <= 50:
                result.append(TextAlignment.LEFT)
            else:
                # ?
                result.append(TextAlignment.BLOCK)
    return result


def leftright(navigator, left, right):
    left = feed_left(navigator, left)
    left = [threshold(item, diff=TEXT_BORDER_NOISE) for item in left]
    right = feed_right(navigator, right)
    right = [threshold(item, diff=TEXT_BORDER_NOISE) for item in right]
    return left, right


def feed_left(navigator, left):
    diff = [item.bounding[0] - left for item in navigator]
    diff = utila.roundme(diff)
    with utila.refactor(major=1, minor=21, description='use convert flag'):
        if isinstance(diff, float):
            diff = [diff]  # pylint:disable=R0204
    return diff


def feed_right(navigator, right):
    diff = [right - item.bounding[2] for item in navigator]
    diff = utila.roundme(diff)
    with utila.refactor(major=1, minor=21, description='use convert flag'):
        if isinstance(diff, float):
            diff = [diff]  # pylint:disable=R0204
    return diff


def threshold(item, diff: float, center: float = 0.0) -> float:
    # TODO: MOVE TO UTILA
    if math.fabs(center - item) <= diff:
        return center
    return item


def zero(items) -> float:
    if not items:
        return None
    counted = 0
    for item in items:
        if not item:
            counted += 1
    return utila.roundme(counted / len(items))
