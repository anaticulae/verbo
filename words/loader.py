# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pprint

import configos
import iamraw
import serializeraw
import utilo

import words.undefined


@configos.cache_small
def load_resources(
    extracted_text,
    text,
    textpositions,
    border,
    headlines,
    headerfooters,
    pages=None,
) -> tuple[list, iamraw.Border]:
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    extracted_text = serializeraw.load_text(
        extracted_text,
        headlines,
        pages=pages,
    )
    ptcns = serializeraw.ptcn_fromfile(
        text,
        textpositions,
        border,
        headerfooters,
        pages=pages,
    )
    contentborder = serializeraw.load_pageborders(border)  # TODO: REMOVE LATER
    undefined = words.undefined.extract_undefined(
        pages=extracted_text,
        ptcns=ptcns,
    )
    return undefined, contentborder


def process_input(extracted, worker):
    result = []
    for pagecontent in extracted:
        extracted = worker(pagecontent)
        if not extracted and pagecontent:
            # TODO: REMOVE LATER
            page = pagecontent[0][0]
            utilo.info(f'skip on page: {page}')
            utilo.info(pprint.pformat(pagecontent))
            continue
        result.append(extracted)
    return result
