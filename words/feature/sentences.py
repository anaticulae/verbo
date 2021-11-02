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

PREFIX_LIST = '#$@LIST@$#:'
SENTENCE_SEPARATOR = '#$@STOP@$#'


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
        listdata = prepare_listitem(item, list_onpage)
        result.append(listdata)
        pages.append(page)
        done.add(listindex)
    return result, pages


def prepare_listitem(item, list_onpage) -> str:
    listnumber, position = words.undefined.listindex(item)
    listitem = list_onpage[listnumber].data[position]
    sentences = sentence_split(listitem[1])
    raw = SENTENCE_SEPARATOR.join(sentences)
    result = f'{PREFIX_LIST}{raw}'
    return result


def sentence_split(item: str) -> list:
    result = german.sentence_tokenize(item)
    return result


def islistitem(item: str) -> bool:
    """\
    >>> islistitem('#$@LIST@$#:Hände waschen')
    True
    """
    item = item.strip()
    if item.startswith(PREFIX_LIST):
        return True
    return False
