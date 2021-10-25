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
import words.loader

LIST_VALID = {
    iamraw.PageContentType.LIST,
    iamraw.PageContentType.TEXT,
}


@utila.checkdatatype
def work(
    text: str,
    textpositions: str,
    border: str,
    headlines: str,
    headerfooters: str,
    magic: str = None,
    pages: tuple = None,
) -> str:
    """Combine `extracted_text` and check the `undefined` fields for lists.

    extracted_text(str): document with `undefined fields` from `text`
                         module of `words`
    """
    ptcns = serializeraw.ptcn_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=border,
        headerfooterpath=headerfooters,
        pages=pages,
    )
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    if utila.exists(magic):
        magic = serializeraw.load_magic_types(
            magic,
            pages=pages,
        )
        ptcns = skip_magic(ptcns, magic, valid=LIST_VALID)
    else:
        utila.error('list: no magic data')
    # run extractor
    result = words.lists.runtime.extract_lists(ptcns, headlines)
    # dump result
    dumped = serializeraw.dump_lists(result)
    return dumped


def skip_magic(ptcns, magics, valid):
    for page in ptcns:
        magic = utila.select_content(magics, page.page)
        if magic:
            invalid = [item[0] for item in magic if item[1] not in valid]
        else:
            invalid = {}
        data = [item for index, item in enumerate(page) if index not in invalid]
        page.data = data
    return ptcns
