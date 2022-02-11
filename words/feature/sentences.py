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
import utila

import words.undefined

LIST_SEPA = '#$@LIST_SEPA@$#:'
LIST_ITEM = '#$@LIST_ITEM@$#:'

FORMULA = '#$@FORMULA@$#:'


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
    lists = serializeraw.load_lists(lists, pages=pages)
    word = prepare_lists(wordo, lists=lists)
    word = undefined_remove(word)
    dumped = serializeraw.dump_text(word)
    return dumped


def prepare_lists(
    word: iamraw.PageContentTexts,
    lists: iamraw.PageContentLists,
) -> iamraw.PageContentTexts:
    for page in word:
        for textsection in page.content:
            pagelist = utila.select_content(lists, page=page.page)
            if not pagelist:
                continue
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
        list_onpage = utila.select_content(lists, page=page)
        listdata, listpages = prepare_listitem(item, list_onpage, page=page)
        contents.extend(listdata)
        pages.extend(listpages)
    return contents, pages


def prepare_listitem(item, list_onpage, page) -> tuple:
    listnumber, position = words.undefined.listindex(item)
    listitem = list_onpage[listnumber].data[position]
    list_text = listitem[1]
    # TODO: RUN IN --WORD-Step?
    list_text = utila.normalize_text(
        list_text,
        normalize_spaces=True,
    )
    sentences = sentence_split(list_text)
    content, pages = [f'{LIST_SEPA}{sentences[0]}'], [page]
    for sentence in sentences[1:]:
        content.append(f'{LIST_ITEM}{sentence}')
        pages.append(page)
    return content, pages


def sentence_split(item: str) -> list:
    result = german.sentence_tokenize(item)
    return result


def is_list_separator(item: str) -> bool:
    """\
    >>> is_list_separator('#$@LIST_SEPA@$#:Hände waschen')
    True
    """
    item = item.strip()
    if item.startswith(LIST_SEPA):
        return True
    return False


def is_list_item(item: str) -> bool:
    """\
    >>> is_list_item('#$@LIST_ITEM@$#:Content')
    True
    """
    item = item.strip()
    if item.startswith(LIST_ITEM):
        return True
    return False


def is_formula(item: str) -> bool:
    """\
    >>> is_formula('#$@FORMULA@$#:5')
    True
    """
    item = item.strip()
    if item.startswith(FORMULA):
        return True
    return False


def nosentence(text: str) -> bool:
    if is_list_separator(text):
        return True
    if is_list_item(text):
        return True
    if is_formula(text):
        return True
    return False


def list_split(item: str):
    start = item[0:16]
    if start == LIST_SEPA:
        return item[16:], LIST_SEPA
    if start == LIST_ITEM:
        return item[16:], LIST_ITEM
    return item
