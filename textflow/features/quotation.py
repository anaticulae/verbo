# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import german
import german.word
import serializeraw
import utila

import textflow.quotation.data
import textflow.quotation.serialize
import words.undefined


def work(word: str, lists: str, pages: tuple = None) -> str:
    word = textflow.quotation.serialize.load_text(
        word,
        headlines=None,
        pages=pages,
    )
    lists = serializeraw.load_lists(
        lists,
        pages=pages,
    )
    lists = group_bypage(lists)  # pylint:disable=R0204
    collected = collect_quotations(word, lists)

    dumped = textflow.quotation.serialize.dump_quotations(collected)
    return dumped


def group_bypage(lists) -> dict:
    # TODO: MOVE AS OPTION TO LIST LOADER?
    result = collections.defaultdict(list)
    for page, content in lists:
        for _, __, item in content:
            result[page].append(item)
    result = dict(result)  # pylint:disable=R0204
    return result


def collect_quotations(  # pylint:disable=R1260
        word,
        lists: dict = None,
) -> textflow.quotation.data.ExtractedQuotations:
    result = []
    for page, index, splitted in sentences(word, lists):
        if german.word.contain_quotation_marks(splitted):
            result.append((page, index, splitted))
    return result


def sentences(  # pylint:disable=R1260
        word,
        lists: dict = None,
) -> textflow.quotation.data.ExtractedQuotations:
    for page, pagecontent in word:  # pylint:disable=too-many-nested-blocks
        sentence_index = 0
        done = utila.Single()
        for _, content in pagecontent:
            for sentence in content:
                list_index = words.undefined.listindex(sentence)
                if list_index is not None:
                    if done.contains(list_index):
                        continue
                    extracted_list = lists[page][list_index]
                    for _, listitem in extracted_list:
                        # list items must not be a full sentence
                        splitted = german.split_words(
                            listitem,
                            validate_sentences=False,
                        )
                        yield page, sentence_index, splitted
                        sentence_index = sentence_index + 1
                    continue
                undefined = words.undefined.intindex(sentence)
                if undefined is not None:
                    continue
                splitted = german.split_words(sentence)
                if splitted:
                    yield page, sentence_index, splitted
                sentence_index = sentence_index + 1
