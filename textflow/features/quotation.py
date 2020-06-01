# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import german.word

import textflow.quotation.data
import textflow.quotation.serialize
import words.undefined


def work(word: str, pages: tuple = None) -> str:
    word = textflow.quotation.serialize.load_text(
        word,
        headlines=None,
        pages=pages,
    )

    collected = collect_quotations(word)

    dumped = textflow.quotation.serialize.dump_quotations(collected)
    return dumped


def collect_quotations(word) -> textflow.quotation.data.ExtractedQuotations:
    result = []
    for page, pagecontent in word:
        sentence_index = 0
        for _, content in pagecontent:
            for sentence in content:
                undefined = words.undefined.intindex(sentence)
                if undefined is not None:
                    continue
                splitted = german.split_words(sentence)
                if splitted:
                    if german.word.contain_quotation_marks(splitted):
                        result.append((page, sentence_index, sentence))
                sentence_index = sentence_index + 1
    return result
