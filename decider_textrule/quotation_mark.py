# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import words.text.word

DOUBLE_OPEN = words.text.word.Mark.QUOTATION_MARK_DOUBLE_OPEN
DOUBLE_CLOSE = words.text.word.Mark.QUOTATION_MARK_DOUBLE_CLOSE
SINGLE_OPEN = words.text.word.Mark.QUOTATION_MARK_SINGLE_OPEN
SINGLE_CLOSE = words.text.word.Mark.QUOTATION_MARK_SINGLE_CLOSE


def valid_double_marks_count(sentence: str) -> bool:
    words_ = words.text.word.split_words(sentence)

    double_open = [item for item in words_ if item == DOUBLE_OPEN]
    double_close = [item for item in words_ if item == DOUBLE_CLOSE]

    valid = len(double_open) == len(double_close)
    return valid


def valid_single_marks_count(sentence: str) -> bool:
    words_ = words.text.word.split_words(sentence)

    single_open = [item for item in words_ if item == SINGLE_OPEN]
    single_close = [item for item in words_ if item == SINGLE_CLOSE]

    valid = len(single_open) == len(single_close)
    return valid
