# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import utila
import yaml

import words.undefined


def work(word: str, pages: tuple = None) -> str:
    word = load_text(word, headlines=None, pages=pages)
    for page, pagecontent in word:
        sentence_index = 0
        for headline, content in pagecontent:
            for sentence in content:
                undefined = words.undefined.intindex(sentence)
                if undefined is not None:
                    continue
                sentence_index = sentence_index + 1
    # assert 0
    return ''


def load_text(
        content: str,
        headlines: iamraw.PagesHeadlineList = None,
        pages=None,
) -> typing.List[iamraw.ChapterText]:
    """Load text and replace headline reference with current headline

    Args:
        content(str): path to dumped text
        headlines(PagesHeadlineList): list of page with list of headlines
        pages(tuple): load all if None or load selected one.
    Returns:
        loaded text with replaced headlines
    """
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)

    # convert page index to global index
    headlines = utila.flatten(headlines) if headlines else None

    result = []
    for line in loaded:
        page, content = int(line['page']), line['content']
        if utila.should_skip(page, pages):
            continue
        pagecontent = []
        for section in content:
            section_content, headline = section['content'], section['headline']
            headline = headlines[headline] if headlines is not None else None
            if headline is None:
                headline = iamraw.Headline(
                    text=None,
                    level=None,
                    rawlevel=None,
                    page=page,
                    container=section['fc'])
            pagecontent.append((headline, section_content))

        result.append((page, pagecontent))
    return result
