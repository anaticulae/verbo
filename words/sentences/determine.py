# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import words.sentences.lists
import words.sentences.quote
import words.undefined


def determine(word, lists):
    word = words.sentences.lists.prepare_lists(
        word,
        lists=lists,
    )
    word = words.sentences.quote.mark_quotes(word)
    word = undefined_remove(word)
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
