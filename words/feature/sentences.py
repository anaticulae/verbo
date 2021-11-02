# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
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


def work(word: str, lists: str, pages: tuple = None) -> str:
    word = serializeraw.load_text(word, pages=pages)
    lists = serializeraw.load_lists(lists, pages=pages)
    word = prepare_lists(word, lists=lists)
    dumped = serializeraw.dump_text(word)
    return dumped


def prepare_lists(
    word: iamraw.PageContentTexts,
    lists: iamraw.PageContentLists,
):
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


def list_insert(textsection, lists):
    done = set()
    result, pages = [], []
    for item, page in zip(textsection.content, textsection.pages):
        listindex = words.undefined.listindex(item)
        if listindex is None:
            result.append(item)
            pages.append(page)
            continue
        if listindex in done:
            continue
        list_onpage = utila.select_content(lists, page=page)
        listdata, listpages = prepare_listitem(item, list_onpage, page=page)
        result.extend(listdata)
        pages.extend(listpages)
        done.add(listindex)
    return result, pages


def prepare_listitem(item, list_onpage, page) -> str:
    listnumber, position = words.undefined.listindex(item)
    listitem = list_onpage[listnumber].data[position]
    sentences = sentence_split(listitem[1])
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
