# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import groupme.abbreviation
import iamraw
import serializeraw
import utila
import yaml

# TODO: MOVE TO IAMRAW

PageContentText = collections.namedtuple('PageContentText', 'page, content')
PageContentTexts = typing.List[PageContentText]


def load_text(
        content: str,
        headlines: iamraw.PagesHeadlineList,
        pages=None,
) -> PageContentTexts:
    loaded = serializeraw.load_text(content, headlines, pages)
    result = []
    for pagenumber, pagecontent in loaded:
        result.append(PageContentText(page=pagenumber, content=pagecontent))
    return result


def dump_text(text: PageContentTexts) -> str:
    converted = [(page.text, page.content) for page in text]
    dumped = serializeraw.dump_text(converted)
    return dumped


ExtractedTextAbbreviation = collections.namedtuple(
    'ExtractedTextAbbreviation',
    'page, content',
)
ExtractedTextAbbreviations = typing.List[ExtractedTextAbbreviation]


def dump_text_abbreviations(items) -> str:
    result = []
    for page in items:
        content = []
        for item in page.content:
            raw = groupme.abbreviation._dump_abbreviation(item)  # pylint:disable=W0212
            content.append(raw)
        if not content:
            continue
        result.append({'page': page.page, 'content': content})
    dumped = yaml.dump(result)
    return dumped


def load_text_abbreviations(
        content: str,
        pages: tuple = None,
) -> ExtractedTextAbbreviations:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)
    result = []
    for page in loaded:
        pagenumber = int(page['page'])
        if utila.should_skip(pagenumber, pages):
            continue
        current = [
            groupme.abbreviation._load_abbreviation(item)  # pylint:disable=W0212
            for item in page['content']
        ]
        result.append(
            ExtractedTextAbbreviation(page=pagenumber, content=current))
    return result
