# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import knlp
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
    collected = collect_quotations(word, lists)

    dumped = textflow.quotation.serialize.dump_quotations(collected)
    return dumped


def collect_quotations(
    word,
    lists: iamraw.PageContentLists = None,
) -> textflow.quotation.data.ExtractedQuotations:
    result = []
    for page, index, sentence, splitted in sentences(word, lists):
        lang = german.lang(splitted).language
        extracted = german.extract_quotes(sentence, lang=lang)
        if not extracted:
            continue
        for item in extracted:
            if item[0] is None or item[1] is None:
                utila.error(f'not fully closed quotation {splitted}')
        extracted = [
            item for item in extracted
            if item[0] is not None and item[1] is not None
        ]
        quote = german.raw_quotation(splitted, extracted)
        for item in quote:
            result.append((page, index, item))
    return result


def sentences(  # pylint:disable=R1260
    word,
    lists: iamraw.PageContentLists = None,
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
                    extracted_list = utila.select_content(lists, page)
                    if extracted_list is None:
                        utila.error(f'could not find list on page: {page}; TODO: split area') # yapf:disable
                        continue
                    try:
                        extracted_list = extracted_list[list_index]
                    except IndexError:
                        utila.error(f'could not access: {list_index} on page: {page}') # yapf:disable
                        continue
                    for _, listitem in extracted_list:
                        # list items must not be a full sentence
                        splitted = knlp.word_tokenize(
                            listitem,
                            # validate_sentences=False,
                        )
                        yield page, sentence_index, listitem, splitted
                        sentence_index = sentence_index + 1
                    continue
                undefined = words.undefined.intindex(sentence)
                if undefined is not None:
                    continue
                splitted = knlp.word_tokenize(sentence)
                if splitted:
                    yield page, sentence_index, sentence, splitted
                sentence_index = sentence_index + 1
