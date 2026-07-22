# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import germania
import iamraw
import serializeraw
import texmex.sentences
import utilo


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


def list_insert(textsection, lists) -> tuple:
    contents, pages = [], []
    single = utilo.Single()
    for item, page in zip(textsection.content, textsection.pages):
        listindexx = listindex(item)
        if listindexx is None:
            contents.append(item)
            pages.append(page)
            continue
        if single.contains(listindexx):
            continue
        listdata, listpages = prepare_listitem(item, lists, page=page)
        contents.extend(listdata)
        pages.extend(listpages)
    return contents, pages


def prepare_listitem(item, lists, page) -> tuple:
    listnumber, position = listindex(item)
    listitem = lists[listnumber].data[position]
    list_text = listitem[1]
    # TODO: RUN IN --WORD-Step?
    list_text = utilo.normalize_text(
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
    result = germania.sentence_tokenize(item)
    return result


def listindex(index: str) -> int:
    """Convert list index `'10l'` to int index `10.

    >>> listindex('10l')
    10
    >>> listindex('5l17')
    (5, 17)
    """
    with contextlib.suppress(ValueError, IndexError):
        splitted = index.split('l')
        if not splitted[1]:
            return int(splitted[0])
        return int(splitted[0]), int(splitted[1])
    return None


def load_lists(source: str, pages: tuple = None) -> dict:
    if not utilo.exists(source):
        utilo.error(f'list does not exists: {source}')
        return []
    lists = serializeraw.load_lists(source, pages=pages)
    lists = utilo.flatten_content(lists)
    result = {item.identifier: item for item in lists}
    return result
