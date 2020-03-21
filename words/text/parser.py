# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import words.text.sentence
import words.text.word


def text_to_words(text: str) -> list:
    result = []
    for sentence_ in words.text.sentence.split_sentences(text):
        for word_ in words.text.word.split_words(
                sentence_,
                validate_sentences=False,
        ):
            result.append(word_)
    return result
