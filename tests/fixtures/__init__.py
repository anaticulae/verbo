# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import hoverpower
import iamraw
import iamraw.sections


def count_chapter(items):
    # Support both data types
    chapters = [
        item for item in items if isinstance(item, iamraw.sections.Chapter)
    ]
    return len(chapters)


def count_chapterlikelihood(items):
    chapters_likelihood = [
        item for item in items
        if isinstance(item, iamraw.PageContentLikelihood) and
        item.content.name == 'chapter'
    ]
    return len(chapters_likelihood)


def assert_chapter_count(chapter, expected):
    count = count_chapter(chapter) + count_chapterlikelihood(chapter)
    msg = (f'{count} != {expected}\n'
           'check chapter detector and min feature value')
    assert count == expected, msg + str(chapter)
