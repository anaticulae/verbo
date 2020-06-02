# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Word
====

.. code-block::

    <document>
    <h1>Chapter 1</h1>
    <p>
    Hallo <b>bold</b>,

    wie geht es ihnen?

    <i>Danke</i> sehr <u>gut</u>
    </p>
    <h1>Chapter 2</h1>

    <h1>Chapter 3</h1>
    </document>

"""
import contextlib
import functools
import re

import configo
import serializeraw
import utila

import words.undefined

PATTERN = re.compile(r'^[0-9]+u$')


@utila.checkdatatype
def work(
        text: str,
        headlines: str,
        lists: str,
        boxed: str,
        pages: tuple = None,
) -> str:

    text, listlookup, boxlookup = load_resources(
        headlines,
        text,
        boxed,
        lists,
        pages=pages,
    )

    text = process_words(text, listlookup, boxlookup)

    dumped = serializeraw.dump_text(text)
    return dumped


def process_words(text, listlookup, boxlookup):
    # TODO: Copy before replacing, to avoid side effects
    for (page, pagecontent) in text:
        # headline,
        for (headline, headlinecontent) in pagecontent:
            for index, line in enumerate(headlinecontent):
                if not PATTERN.match(line):
                    continue
                undefined = words.undefined.intindex(line)
                searched = listlookup.search(
                    page,
                    headline.container,
                    undefined,
                )
                if searched is not None:
                    headlinecontent[index] = f'{searched}l'
                    continue
                searched = boxlookup.search(page, undefined)
                if searched is not None:
                    headlinecontent[index] = f'{searched}b'
                    continue
    return text


class ListLookUp:
    # TODO: UNITE WITH BOXEDCHECKER!
    def __init__(self, lists):
        self.data = {}
        self.load(lists)

    def load(self, lists):
        index = 0
        for page, content in lists:
            for item in content:
                try:
                    self.data[page].append((item, index))
                except KeyError:
                    self.data[page] = [(item, index)]
                index += 1

    def search(self, page, headline, undefined):  # pylint:disable=W0613
        with contextlib.suppress(KeyError):
            current = self.data[page]
            for ((_, _, content), index) in current:
                if undefined in content.area:
                    return index
        return None


class BoxLookUp:

    def __init__(self, boxes):
        self.data = {}
        self.load(boxes)

    def load(self, boxes):  # pylint:disable=R0914
        for line in boxes:
            page, content = line
            for item in content:
                __, _, items = item
                chained = utila.flatten(items)  # support verschachtelte boxes
                for real in chained:
                    _, (bindex, bcontent) = real
                    uindexs = [uindex for (_, uindex, _) in bcontent]
                    self.append(page, bindex, uindexs)

    def append(self, page, boxid, uindex):
        if page not in self.data:
            self.data[page] = {}
        for item in uindex:
            self.data[page][item] = boxid

    def search(self, page, uindex):
        with contextlib.suppress(KeyError):
            return self.data[page][uindex]
        return None


@functools.lru_cache(configo.CACHE_SMALL)
def load_resources(
        headlines: str,
        text: str,
        boxed: str,
        lists: str,
        pages=None,
):
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    text = serializeraw.load_text(text, headlines=headlines, pages=pages)
    boxed = serializeraw.load_boxedcontent(boxed, pages=pages)
    lists = serializeraw.load_lists(lists, pages=pages)
    listlookup = ListLookUp(lists)
    boxlookup = BoxLookUp(boxed)
    return text, listlookup, boxlookup
