# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import serializeraw
import texmex.sentences
import utila

import words.undefined


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
    lists = load_lists(lists, pages=pages)
    word = prepare_lists(wordo, lists=lists)
    word = undefined_remove(word)
    dumped = serializeraw.dump_text(word)
    return dumped


def load_lists(source: str, pages: tuple = None) -> dict:
    lists = serializeraw.load_lists(source, pages=pages)
    lists = utila.flatten_content(lists)
    result = {item.identifier: item for item in lists}
    return result


def prepare_lists(
    word: iamraw.PageContentTexts,
    lists: dict,
) -> iamraw.PageContentTexts:
    for page in word:
        for textsection in page.content:
            textsection.content, textsection.pages = list_insert(
                textsection,
                lists,
            )
    return word


def undefined_remove(word: iamraw.PageContentTexts) -> iamraw.PageContentTexts:
    for wordpage in word:
        for textsection in wordpage.content:
            contents, pages = [], []
            for item, page in zip(textsection.content, textsection.pages):
                undefined = words.undefined.intindex(item)
                if undefined is not None:
                    continue
                contents.append(item)
                pages.append(page)
            textsection.content, textsection.pages = contents, pages
    return word


def list_insert(textsection, lists) -> tuple:
    contents, pages = [], []
    single = utila.Single()
    for item, page in zip(textsection.content, textsection.pages):
        listindex = words.undefined.listindex(item)
        if listindex is None:
            contents.append(item)
            pages.append(page)
            continue
        if single.contains(listindex):
            continue
        listdata, listpages = prepare_listitem(item, lists, page=page)
        contents.extend(listdata)
        pages.extend(listpages)
    return contents, pages


def prepare_listitem(item, lists, page) -> tuple:
    listnumber, position = words.undefined.listindex(item)
    listitem = lists[listnumber].data[position]
    list_text = listitem[1]
    # TODO: RUN IN --WORD-Step?
    list_text = utila.normalize_text(
        list_text,
        normalize_spaces=True,
    )
    sentences = sentence_split(list_text)
    content, pages = [f'{texmex.sentences.LIST_SEPA}{sentences[0]}'], [page]
    for sentence in sentences[1:]:
        content.append(f'{texmex.sentences.LIST_ITEM}{sentence}')
        pages.append(page)
    return content, pages


def sentence_split(item: str) -> list:
    result = german.sentence_tokenize(item)
    return result
