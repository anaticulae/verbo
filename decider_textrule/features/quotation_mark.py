# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import words.text.word


def work(text: str) -> typing.Tuple[str, str]:
    return '', ''


DOUBLE_OPEN = words.text.word.Mark.QUOTATION_MARK_DOUBLE_OPEN
DOUBLE_CLOSE = words.text.word.Mark.QUOTATION_MARK_DOUBLE_CLOSE


def validate_double_marks(sentence: str):
    marks = []
    word = words.text.word.split_words(sentence)

    double_open = [item for item in word if item == DOUBLE_OPEN]
    double_close = [item for item in word if item == DOUBLE_CLOSE]
