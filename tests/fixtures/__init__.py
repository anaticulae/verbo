# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import iamraw.sections
import power
import serializeraw
import texmex
import utila


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


def create_pagetextnavigators(path, pages=None):
    text = iamraw.path.text(path)
    text = serializeraw.load_document(
        text,
        pages=pages,
    )
    assert text

    text_positions = iamraw.path.textposition(path)
    text_positions = serializeraw.load_textpositions(
        text_positions,
        pages=pages,
    )
    assert text_positions

    navigators = texmex.create_pagetextnavigators(
        text=text,
        text_positions=text_positions,
    )
    return navigators


def setup_testresources(source, dest, accept=None):
    # TODO: REPLACE WITH UTILA CODE
    # this step is required, cause the test generator already
    # generates this required items.
    sources = [
        item.name
        for item in os.scandir(power.link(power.DOCU27_PDF))
        if accept is None or
        any([item.name.startswith(pattern) for pattern in accept])
    ]
    for item in sources:
        utila.copy_content(os.path.join(source, item), dest)
