# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# NOTE: STORE EXPERIMENTAL CODE HERE


def sentences(texts, numbers: bool = False):
    number, current = 0, None
    for chunk in texts:
        for section in chunk.content:
            for page, sentence in zip(section.pages, section.content):
                if not numbers:
                    yield page, sentence
                else:
                    if current != page:
                        number = 0
                        current = page
                    else:
                        number += 1
                    yield page, number, sentence
