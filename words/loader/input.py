# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import pprint
import typing

import configo
import iamraw
import serializeraw
import utila

import words.headlines
import words.undefined


@functools.lru_cache(configo.CACHE_SMALL)
def load_resources(
        extracted_text,
        text,
        text_position,
        border,
        headlines,
        headerfooters,
        pages=None,
) -> typing.Tuple[typing.List, iamraw.Border]:
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    extracted_text = serializeraw.load_text(
        extracted_text,
        headlines,
        pages=pages,
    )
    border = serializeraw.load_pageborders(border, pages=pages)
    headerfooters = serializeraw.load_headerfooter(
        headerfooters,
        pages=pages,
    )
    contentborder = words.headlines.contentborder(
        border,
        headerfooters,
    )
    text = serializeraw.load_document(
        text,
        pages=pages,
    )
    text_position = serializeraw.load_textpositions(
        text_position,
        pages=pages,
    )
    undefined = words.undefined.extract_undefined(
        extracted_text,
        text,
        text_position,
        contentborder=contentborder,
    )
    return undefined, contentborder


def process_input(extracted, worker):
    result = []
    for pagecontent in extracted:
        extracted = worker(pagecontent)
        if not extracted and pagecontent:
            # TODO: REMOVE LATER
            page = pagecontent[0][0]
            utila.info('skip on page: %d' % (page))
            utila.info(pprint.pformat(pagecontent))
            continue
        result.append(extracted)
    return result
