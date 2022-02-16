# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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
import collections
import contextlib
import functools
import re

import configo
import serializeraw
import utila

import words.undefined

PATTERN = re.compile(r'^[0-9]{1,3}u$')


@utila.checkdatatype
def work(
    textx: str,
    headliner: str,
    lists: str,
    boxes: str,
    pages: tuple = None,
) -> str:
    text, listlookup, boxlookup = load_resources(
        headliner,
        textx,
        boxes,
        lists,
        pages=pages,
    )
    text = process_words(text, listlookup, boxlookup)
    dumped = serializeraw.dump_text(text)
    return dumped


def process_words(text, listlookup, boxlookup):
    # TODO: Copy before replacing, to avoid side effects?
    for item in text:
        # headline,
        for (headline, headlinecontent) in item.content:
            for index, line in enumerate(headlinecontent):
                if not PATTERN.match(line):
                    continue
                undefined = words.undefined.intindex(line)
                searched = listlookup.search(
                    item.page,
                    headline.container,
                    undefined,
                )
                if searched is not None:
                    raw = f'{searched[0]}l{searched[1]}'
                    headlinecontent[index] = raw
                    continue
                searched = boxlookup.search(item.page, undefined)
                if searched is not None:
                    headlinecontent[index] = f'{searched}b'
                    continue
    return text


class ListLookUp:
    """ListLookUp

    Uses page wise lookup. The first list on a page starts with the
    number 0.
    """

    # TODO: UNITE WITH BOXEDCHECKER!
    def __init__(self, lists):
        self.data = None
        self.load(lists)

    def load(self, lists):
        # rewrite input data
        constructed = collections.defaultdict(dict)
        for page in lists:
            for listnumber, listinstance in enumerate(page.content):
                for (pagenr, line), value in expand_instance(
                        listinstance,
                        listnumber,
                        page.page,
                ):
                    constructed[pagenr][line] = value
        self.data = dict(constructed)

    def search(self, page, headline, undefined):  # pylint:disable=W0613
        with contextlib.suppress(KeyError):
            return self.data[page][undefined]
        return None


def expand_instance(listinstance, listnumber, pagenr):
    arealist = listinstance.area
    if isinstance(arealist[0], int):
        arealist = [tuple(arealist)]
    area_length = index_split(
        data=listinstance.area_length,
        lengths=[len(item) for item in arealist],
    )
    result = []
    for pageoff, (area, length) in enumerate(zip(arealist, area_length)):
        # pageoff to signal that list overlaps more than one page
        instance_areas = areas(
            area,
            area_length=length,
        )
        for line, pos in zip(area, instance_areas):
            result.append(((pagenr + pageoff, line), (listnumber, pos[0])))
    return result


def index_split(data, lengths):
    """\
    >>> index_split([2, 2, 1, 2, 2, 1],(2, 8))
    ([2], [2, 1, 2, 2, 1])
    """
    result = []
    for count in lengths:
        collected = []
        while count:
            if not data:
                break
            count -= data[0]
            collected.append(data[0])
            data = data[1:]
        result.append(collected)
    result: tuple = tuple(result)
    return result


def areas(area, area_length) -> list:
    """\
    >>> areas((1, 2, 3, 4, 5, 6, 7), (3, 1, 3))
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1), (2, 2)]
    """
    current = 0
    result = []
    for index, length in enumerate(area_length):
        for pos, _ in enumerate(area[current:current + length]):
            result.append((index, pos))
        current = +length
    return result


def flat_lookup(items):
    """\
    >>> flat_lookup([(10, [(12, 13, 14, 15, 16, 17), (0, 1, 2, 3, 4)])])
    [(10, (12, 13, 14, 15, 16, 17)), (11, (0, 1, 2, 3, 4))]
    >>> flat_lookup([(8, [12, 13, 14, 15, 16, 17])])
    [(8, [12, 13, 14, 15, 16, 17])]
    """
    result = []
    for page, content in items:
        islist = isinstance(content, list)
        if islist and not all((isinstance(item, int) for item in content)):
            for number, pagecontent in enumerate(content, start=page):
                result.extend(flat_lookup([(number, pagecontent)]))
        else:
            result.append((page, content))
    return result


class BoxLookUp:

    def __init__(self, boxes):
        self.data = {}
        self.load(boxes)

    def load(self, boxes):  # pylint:disable=R0914
        for line in boxes:
            page, content = line
            for __, _, items in content:
                chained = utila.flatten(items)  # support verschachtelte boxes
                for _, (bindex, bcontent) in chained:
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
