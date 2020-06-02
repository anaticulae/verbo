#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import collections
import os
import statistics

import iamraw
import texmex
import texmex.text
import utila

__version__ = '0.5.12'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS = 'words'
PACKAGE = PROCESS

HEADLINE_STEP = 'headlines'
HEADLINE_STEP_RESULT = 'headlines'
HEADLINES = f'{HEADLINE_STEP}_{HEADLINE_STEP_RESULT}'

WORDS_HEADLINES = f'{PROCESS}__{HEADLINES}.yaml'


@utila.todo(
    version=iamraw.__version__,
    major=1,
    minor=26,
    description='replace with iamraw',
)
def document_textfeed(
        navigators: texmex.PageTextNavigators,
        count: int = 1,
        left: bool = True,
) -> 'utils.Ints':
    assert count >= 1, f'require none negative count, got: {count}'
    counter = collections.Counter()
    for navigator in navigators:
        for item in navigator:
            if not item.text.strip():
                continue
            if left:
                counter[item.bounding[0]] += 1
            else:
                right = utila.roundme(item.bounding[2])
                counter[right] += 1
    result = counter.most_common(count)
    result = [item for item, _ in result]
    if not result:
        return None
    if count == 1:
        return result[0]
    return result[0:count]


texmex.document_textfeed = document_textfeed


def textsize_frompage(navigator: 'texmex.NavigatorMixin or list') -> float:
    collected = []
    for line in navigator:
        fontsizes = texmex.TextStyle.textsizes(
            line.style,
            method=lambda x: x,  # do not filter anything
        )
        collected.extend(fontsizes)
    return utila.mode(collected, minimize=True)


# TODO: REMOVE LATER
texmex.textsize_frompage = textsize_frompage
