# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BlockQuotes

.. todo:: think about block quotes without quotation marks


"""

import collections
import typing

import german
import serializeraw
import texmex
import utila
import yaml

MIN_BLOCK_QUOTE_DIST = 5.0  # TODO: HOLY VALUE

PageContentBlockQuotes = collections.namedtuple(
    'PageContentBlockQuotes',
    'content, page',
)
PageContentBlockQuotesList = typing.List[PageContentBlockQuotes]


def work(
        text: str,
        textpositions: str,
        sizeandborderpath: str,
        headerfooterpath: str,
        pages: tuple,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborderpath,
        headerfooterpath,
        pages=pages,
    )
    result = [analyze_page(page) for page in ptcns]

    # remove empty pages
    result = [item for item in result if item.content]
    dumped = dump_blockquotes(result)
    return dumped


def analyze_page(ptcn: texmex.PageTextContentNavigator) -> PageContentBlockQuotes: # yapf:disable
    grouped = texmex.group_linedistances_complex(ptcn)

    bounds = texmex.textbounds(ptcn, contentborder=ptcn.content)
    boundsgroups = group_todata(grouped, bounds)
    datagroups = group_todata(grouped, ptcn)

    result = []
    for index, (group, bounds) in enumerate(zip(datagroups, boundsgroups)):
        if not iscitation_group(bounds):
            continue
        result.append((grouped[index], [item.text.strip() for item in group]))
    return PageContentBlockQuotes(page=ptcn.page, content=result)


def group_todata(index, navigator):
    if not index:
        return []
    result = []
    for group in index:
        collected = [navigator[index] for index in group]
        result.append(collected)
    return result


def iscitation_group(bounds) -> bool:
    """Check that group is indentend and contains some quotation
    marks."""
    left, right = group_distance(bounds)

    if left < MIN_BLOCK_QUOTE_DIST:
        return False
    if right < MIN_BLOCK_QUOTE_DIST:
        return False

    lines = [
        german.split_words(item.text, validate_sentences=False)
        for item in bounds
    ]
    marks = [word for word in lines if german.contain_quotation_marks(word)]
    marks = utila.flatten(marks)
    contains_quotation = any(marks)
    return contains_quotation


def group_distance(group):
    if not group:
        return None

    left = [item.bounds.leftdist for item in group]
    right = [item.bounds.rightdist for item in group]

    left = utila.roundme(left, digits=0, convert=False)
    right = utila.roundme(right, digits=0, convert=False)

    left, right = utila.mode(left), utila.mode(right)
    return left, right


# TODO: MOVE TO SERIALIZERAW
def dump_blockquotes(blockquotes: PageContentBlockQuotesList) -> str:
    converted = [(page.page, page.content) for page in blockquotes]
    dumped = yaml.safe_dump(converted, width=200)
    return dumped


def load_blockquotes(
        content: str,
        pages: tuple = None,
) -> PageContentBlockQuotesList:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.safe_load(content)
    result = []
    for page, pagecontent in loaded:
        if utila.should_skip(page, pages):
            continue
        result.append(PageContentBlockQuotes(page=page, content=pagecontent))
    return result
