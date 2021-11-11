# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""There are 2 different types of list:

    * the ordered (1.,2.,3.,...)
    * dotted, plus, minus - list (* Bratwurst, * Currwurst, +, -.)

     - load extracted text
     - filter undefined areas
     - check undefined area that area is list
"""

import iamraw
import serializeraw
import utila

import words.lists.runtime
import words.lookup


@utila.checkdatatype
def work(
    textx: str,
    textpositions: str,
    border: str,
    headliner: str,
    headerfooters: str,
    magic: str = None,
    pages: tuple = None,
) -> str:
    """Combine `extracted_text` and check the `undefined` fields for lists.

    extracted_textx(str): document with `undefined fields` from `text`
                         module of `words`
    """
    ptcns, headlines = create_data(
        textx,
        textpositions,
        border,
        headliner,
        headerfooters,
        magic,
        pages=pages,
    )
    # run extractor
    result = words.lists.runtime.extract_lists(ptcns, headlines)
    # dump result
    dumped = serializeraw.dump_lists(result)
    return dumped


def create_data(
    text: str,
    textpositions: str,
    border: str,
    headlines: str,
    headerfooters: str,
    magic: str = None,
    pages: tuple = None,
):
    ptcns = serializeraw.ptcn_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=border,
        headerfooterpath=headerfooters,
        pages=pages,
    )
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    magic = words.lookup.magics_frompath(
        path=magic,
        pages=pages,
    )
    ptcns = skip_magic(ptcns, magic)
    return ptcns, headlines


LIST_VALID = {
    iamraw.PageContentType.LIST,
    iamraw.PageContentType.TEXT,
}


def skip_magic(ptcns, magics):
    if isinstance(magics, words.lookup.LookupEmpty):
        return ptcns
    for page in ptcns:
        data = [
            item for index, item in enumerate(page) if magics(
                page=page.page,
                line=index,
                default=iamraw.PageContentType.TEXT,
            ) in LIST_VALID
        ]
        page.data = data
    return ptcns
