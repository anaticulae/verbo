# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import utila

import decider_textrule.quotation_mark as dqm
import words.text.word


def work(text: str) -> typing.Tuple[str, str]:
    return '', ''


def validate_sentences(pages):
    invalid_double = []
    invalid_single = []
    for page in pages:
        sentences = words.text.sentence.find_sentences(page)
        sentence_index = 0
        for (_, content) in sentences:
            for sentence in content:
                token = words.text.word.split_words(sentence)
                if not token:
                    utila.error(f'invalid sentence: {sentence}')
                    sentence_index += 1
                    continue

                if not dqm.valid_double_marks_count(token):
                    invalid_double.append((page.page, sentence_index))
                sentence_index += 1
    return invalid_double, invalid_single
