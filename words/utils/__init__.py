# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# NOTE: STORE EXPERIMENTAL CODE HERE


def sentences(texts):
    for chunk in texts:
        for section in chunk.content:
            for page, sentence in zip(section.pages, section.content):
                yield page, sentence
