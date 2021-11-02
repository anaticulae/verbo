# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila

import words.undefined

PREFIX_LIST = '#$@LIST@$#:'


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
            textsection.content = list_insert(
                textsection,
                lists,
            )
    return word


def list_insert(textsection, lists):
    content, pages = textsection.content, textsection.pages
    done = set()
    result = []
    for item, page in zip(content, pages):
        listindex = words.undefined.listindex(item)
        if listindex is None:
            result.append(item)
            continue
        if listindex in done:
            continue
        list_onpage = utila.select_content(lists, page=page)
        listnumber, position = words.undefined.listindex(item)
        listitem = list_onpage[listnumber].data[position]
        listdata = f'{PREFIX_LIST}{listitem[1]}'
        result.append(listdata)
        done.add(listindex)
    return result
