# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Words: Boxed Text Extractor
===========================

TODO: Think about this complex data structure. Do we need this realy?
"""

import collections
import functools

import serializeraw
import utilo

import words.boxed
import words.loader


@utilo.checkdatatype
def work(
    extracted_text: str,
    textx: str,
    text_position: str,
    headliner: str,
    border: str,
    boxes: str,
    headerfooters: str,
    pages: tuple = None,
) -> str:
    """Combine `extracted_text` and check the `undefined` fields for lists

    extracted_textx(str): document with `undefined fields` from `text`
                         module of `words`
    """
    extracted, _ = words.loader.load_resources(
        extracted_text,
        textx,
        text_position,
        border,
        headlines=headliner,
        headerfooters=headerfooters,
        pages=pages,
    )
    boxes = serializeraw.load_boxes(boxes)

    result = process_content(extracted, boxes)

    try:
        dumped = serializeraw.dump_boxedcontent(result)
    except (TypeError, ValueError):
        utilo.error('could not dump boxed content')
        dumped = '[]'
    return dumped


def process_content(extracted, boxes: words.boxed.BoxedChecker):
    boxes = words.boxed.BoxedChecker(boxes)
    worker = functools.partial(extract_boxed_content, boxed=boxes)

    result = words.loader.process_input(extracted, worker)
    return result


def extract_boxed_content(contentblock, boxed: words.boxed.BoxedChecker):  # pylint:disable=R0914
    result = collections.defaultdict(list)
    for (page, headlinenumber, headlinecontent) in contentblock:

        zipped = zip(headlinecontent[0], headlinecontent[1])
        for _, ((headlineblockid, blocks), uindexs) in enumerate(zipped):
            collected = []
            current = collections.defaultdict(list)
            for block, uindex in zip(blocks, uindexs):
                bounding, line = block.bounding, block.text
                boxid = boxed.boxid(page, bounding)
                if boxid == words.boxed.NO_BOX:
                    # splitted by non-box-element
                    if not current:
                        continue
                    collected.append([(
                        boxed.boundingbox(page, boxid_),
                        (boxid_, uindex, content),
                    ) for boxid_, content in current.items()])
                    current = collections.defaultdict(list)
                # add line to box, defined by `boxid`
                current[boxid].append((bounding, uindex, line))
            # item ends with box
            if current:
                collected.append([(
                    boxed.boundingbox(page, item),
                    (item, content),
                ) for item, content in current.items()])

            if collected:
                result[page].append((
                    headlinenumber,
                    headlineblockid,
                    collected,
                ))
    if not result:
        return None
    assert len(result) == 1, len(result)
    for key, value in result.items():
        # TODO: CHECK THIS!
        # THIS FOR RUNS ONLY ONCES
        return (key, value)
