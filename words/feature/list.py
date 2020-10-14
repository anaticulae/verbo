# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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

import serializeraw
import utila

import words.lists.runtime
import words.loader


@utila.checkdatatype
def work(  # pylint:disable=R0914
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
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=border,
        headerfooterpath=headerfooters,
        pages=pages,
    )
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    magic = serializeraw.load_types(
        magic,
        pages=pages,
    ) if utila.exists(magic) else None  # pylint:disable=E1101
    if magic is None:
        utila.error('list: no magic data')
    result = words.lists.runtime.extract_lists(ptcns, headlines)
    dumped = serializeraw.dump_lists(result)
    return dumped
