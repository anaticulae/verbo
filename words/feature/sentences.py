# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import serializeraw

import words.sentences.bounding
import words.sentences.determine


def work(
    wordo: str,
    lists: str,
    headliner: str,
    xtext: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    pages: tuple = None,
) -> typing.Tuple[str, str]:
    headlines = serializeraw.load_headlines(
        headliner,
        pages=pages,
    )
    wordo = serializeraw.load_text(
        wordo,
        headlines=headlines,
        pages=pages,
    )
    lists = words.sentences.lists.load_lists(
        lists,
        pages=pages,
    )
    sentences = words.sentences.determine.determine(
        wordo,
        lists=lists,
    )
    dumped_sentences = serializeraw.dump_text(sentences)
    ptncs = serializeraw.ptcn_fromfile(
        xtext,
        textpositions,
        sizeandborder,
        headerfooter,
        pages=pages,
    )
    sentence_bounding = words.sentences.bounding.boundings(
        sentences,
        ptncs,
    )
    dumped_bounding = serializeraw.dump_sentence_bounding(sentence_bounding)
    return dumped_sentences, dumped_bounding
