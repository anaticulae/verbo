# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import contextlib
import typing

import iamraw
import texmex
import utila

import words.headlines.strategies.standard
import words.headlines.utils

STRATEGIES = [
    words.headlines.strategies.standard,
    words.headlines.strategies.standard,
    words.headlines.strategies.standard,
]

Data = collections.namedtuple(
    'Data',
    'ptcns sectionlist chapters textsize textdistance',
)


def headlines(
        ptcns: texmex.PageTextContentNavigators,
        sectionlist: typing.List[iamraw.Sections],
        chapters: 'ChapterRanges' = None,
        pages: tuple = None,
) -> iamraw.Headlines:
    textsize = texmex.document_textsize(navigators=ptcns)
    textdistance = words.headlines.utils.document_textdistance(
        navigators=ptcns,
        digits=0,
    )
    data = Data(ptcns, sectionlist, chapters, textsize, textdistance)

    results = strategies(
        data=data,
        pages=pages,
    )

    return results


def strategies(data: Data = None, pages: tuple = None):
    results = []
    for strategy in STRATEGIES:
        result = run(
            strategy=strategy,
            data=data,
            pages=pages,
        )
        results.append(result)
    return results


def run(strategy, data: Data, pages: tuple = None):
    chapter_numbers, chapter_ranges = words.headlines.utils.prepare_chapter_and_content(
        data.sectionlist,
        data.chapters,
    )

    results = {}
    # run extraction
    for chapter in chapter_numbers:
        # HACK: REMOVE LAST PAGE TO PASS SHOULD_SKIP THERE IS A
        # PROBLEM WITH THE LAST AREA, CAUSE THE INDEX OF AN AREA IS
        # EXPANDED + 1 OVER THE AREA. AT THE LAST AREA THIS EXPANDS
        # OUTSIDE OF THE DOCUMENT. HACKING PAGE SKIP CHECK SEEMS NOT
        # SO PROBLEMATIC HERE, BUT MUST BE FIXED.
        chapter_pages = list(chapter_ranges[chapter])
        chapter_pages = tuple(chapter_pages[:-1])  # pylint:disable=R0204
        if utila.should_skip(chapter_pages, pages):
            continue
        results[chapter] = words.headlines.utils.extract_chapter(
            strategy,
            data,
            chapter_ranges[chapter],
        )

    # filter result
    with contextlib.suppress(AttributeError):
        results = strategy.filter_headlines(results)

    grouped = words.headlines.utils.groupby_headlinelevel(results)
    return grouped


def best(results):
    return results[0]
