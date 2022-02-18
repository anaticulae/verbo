# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import words.sentences.determine


def work(
    wordo: str,
    lists: str,
    headliner: str,
    pages: tuple = None,
) -> str:
    headlines = serializeraw.load_headlines(headliner, pages=pages)
    wordo = serializeraw.load_text(
        wordo,
        headlines=headlines,
        pages=pages,
    )
    wordo = words.sentences.determine.determine(wordo, lists=lists, pages=pages)
    dumped = serializeraw.dump_text(wordo)
    return dumped
