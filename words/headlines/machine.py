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

import words.headlines.strategies.multiline
import words.headlines.strategies.nolevel
import words.headlines.strategies.standard
import words.headlines.utils

STRATEGIES = [
    words.headlines.strategies.multiline,
    words.headlines.strategies.nolevel,
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
    # prepare data
    textsize = texmex.document_textsize(navigators=ptcns)
    textdistance = words.headlines.utils.document_textdistance(
        navigators=ptcns,
        digits=0,
    )
    data = Data(ptcns, sectionlist, chapters, textsize, textdistance)
    # run strategies
    results = [
        run(
            strategy=strategy,
            data=data,
            pages=pages,
        ) for strategy in STRATEGIES
    ]
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
        results[chapter] = extract_chapter(
            strategy,
            data,
            chapter_ranges[chapter],
        )

    # filter result
    with contextlib.suppress(AttributeError):
        results = strategy.filter_headlines(results)

    grouped = words.headlines.utils.groupby_headlinelevel(results)
    return grouped


def extract_chapter(strategy, data, chapter_range):
    result = []
    start, end = chapter_range
    for page in range(int(start), int(end + 1)):
        navigator = utila.select_page(data.ptcns, page)
        if not navigator or not navigator.content:  # TODO: CHECK .content
            # empty page
            continue
        try:
            # use module extractor
            pageheadlines = strategy.extract_page(data, page)
        except AttributeError:
            # use default extractor
            pageheadlines = extract_page(strategy, data, page)
        result.extend(pageheadlines)
    return result


def extract_page(strategy, data, page):
    pagecontent = utila.select_page(data.ptcns, page)
    result = []
    bounds = texmex.textbounds(pagecontent, pagecontent.content)
    without_content = [item.bounds for item in bounds]
    # PageContentNavigator, the header and footer is ignored
    textdistances = texmex.fontdistance_textbounds(without_content)

    textfeeds = [item.bounds.leftdist for item in bounds]

    for containerid, item in enumerate(pagecontent):
        splitted = item.text.splitlines()
        if len(splitted) > 1:
            # TODO: REMOVE?
            continue
        headline = strategy.extract_headline(
            textinfo=item,
            textdistances=textdistances,
            textfeeds=textfeeds,
            textsize=data.textsize,
            textdistance=data.textdistance,
            ptcn=pagecontent,
            containerid=containerid,
        )
        if not headline:
            continue
        result.append(headline)
    return result
