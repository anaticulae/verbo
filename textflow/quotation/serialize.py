# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila
import yaml

import textflow.quotation.data


def dump_quotations(quotations) -> str:
    result = []
    for page, index, sentence in quotations:
        result.append(f'{page} {index} {sentence}')
    dumped = yaml.dump(result)
    return dumped


def load_quotations(
    content: str,
    pages: tuple = None,
) -> textflow.quotation.data.ExtractedQuotations:
    loaded = utila.yaml_from_raw_or_path(content, safe=False)
    result = []
    for item in loaded:
        page, index, sentence = item.split(maxsplit=2)
        page = int(page)
        if utila.should_skip(page, pages):
            continue
        index = int(index)
        result.append(
            textflow.quotation.data.ExtractedQuotation(page, index, sentence))
    return result


# TODO: REPLACE WITH SERIALZIERAW?
def load_text(
    content: str,
    headlines: iamraw.PagesHeadlineList = None,
    pages=None,
) -> iamraw.ChapterTextList:
    """Load text and replace headline reference with current headline

    Args:
        content(str): path to dumped text
        headlines(PagesHeadlineList): list of page with list of headlines
        pages(tuple): load all if None or load selected one.
    Returns:
        loaded text with replaced headlines
    """
    loaded = utila.yaml_from_raw_or_path(content, safe=False)
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
                    title=None,
                    level=None,
                    raw_level=None,
                    page=page,
                    container=section['fc'],
                )
            pagecontent.append((headline, section_content))
        result.append((page, pagecontent))
    return result
