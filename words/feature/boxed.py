# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Words: Boxed Text Extractor
===========================

TODO: Think about this complex data structure. Do we need this realy?
"""
import collections
import functools

import hey
import iamraw
import serializeraw
import utila
import yaml

import words.boxed
import words.loader.input

PageContentBoxed = collections.namedtuple('PageContentBoxed', 'page content')


@utila.checkdatatype
def work(
        extracted_text: str,
        text: str,
        text_position: str,
        headlines: str,
        border: str,
        boxes: str,
        headerfooters: str,
        pages=None,
) -> str:
    """Combine `extracted_text` and check the `undefined` fields for lists

    extracted_text(str): document with `undefined fields` from `text`
                         module of `words`
    """
    extracted, _ = words.loader.input.load_resources(
        extracted_text,
        text,
        text_position,
        border,
        headlines=headlines,
        headerfooters=headerfooters,
        pages=pages,
    )
    boxes = serializeraw.load_boxes(boxes)

    result = process_content(extracted, boxes)

    dumped = dump_boxedcontent(result)
    return dumped


def process_content(extracted, boxes: words.boxed.BoxedChecker):
    boxes = words.boxed.BoxedChecker(boxes)
    worker = functools.partial(extract_boxed_content, boxed=boxes)

    result = words.loader.input.process_input(extracted, worker)
    return result


def extract_boxed_content(contentblock, boxed: words.boxed.BoxedChecker):  # pylint:disable=R0914
    result = collections.defaultdict(list)
    for (page, headlinenumber, headlinecontent) in contentblock:

        zipped = zip(headlinecontent[0], headlinecontent[1])
        for _, ((headlineblockid, blocks), uindexs) in enumerate(zipped):
            collected = []
            current = collections.defaultdict(list)
            for block, uindex in zip(blocks, uindexs):
                bounding, line = block.bounding, block.text
                boxid = boxed.boxid(page, bounding)
                if boxid == words.boxed.NO_BOX:
                    # splitted by non-box-element
                    if not current:
                        continue
                    collected.append([(
                        boxed.boundingbox(page, boxid_),
                        (boxid_, uindex, content),
                    ) for boxid_, content in current.items()])
                    current = collections.defaultdict(list)
                # add line to box, defined by `boxid`
                current[boxid].append((bounding, uindex, line))
            # item ends with box
            if current:
                collected.append([(
                    boxed.boundingbox(page, item),
                    (item, content),
                ) for item, content in current.items()])

            if collected:
                result[page].append((
                    headlinenumber,
                    headlineblockid,
                    collected,
                ))
    if not result:
        return None
    assert len(result) == 1, len(result)
    for key, value in result.items():
        return (key, value)


def dump_boxedcontent(boxed) -> str:  # pylint:disable=R0914

    # headlinenumber,
    # headlineblocknumber,
    # collected,

    # BoundingBox
    # boxid, content
    raw = []
    for (page, pagecontent) in boxed:
        pageresult = []
        for (headlinenumber, headlineblocknumber, collected) in pagecontent:
            # for (bounding, blockcontent) in collected:
            # more than one box in a box-container:
            # content, box, box, content, box, content
            single_collector = []  # crazy naming!
            for multiboxed in collected:
                items = []
                for index, item in enumerate(multiboxed):
                    try:
                        bounding, (boxid, _content) = item
                    except ValueError:
                        # TODO: INVESTIGATE WHAT HAPPENS HERE
                        utila.error(
                            'could not convert, skip boxed: `%s`' % str(item))
                        continue
                    items.append({
                        'boxed_id':
                        '%d %d' % (boxid, index),
                        'bounding':
                        str(bounding),
                        'content': [
                            '%s %d %s' % (str(bounding), uindex, contentitem)
                            for (bounding, uindex, contentitem) in _content
                        ]
                    })
                single_collector.append(items)
            pageresult.append({
                'headlinenumber': headlinenumber,
                'headlineblocknumber': headlineblocknumber,
                'content': single_collector,
            })

        raw.append({
            'page': page,
            'content': pageresult,
        })
    dumped = yaml.dump(raw)
    return dumped


@functools.lru_cache(hey.CACHE_SMALL)
def load_boxedcontent(content: str, pages=None):  # pylint:disable=R0914

    def _parse_box_content(line: str) -> tuple:
        """bounding(BoundingBox) undefined_index(int) content(str)"""
        splitted = line.split(maxsplit=5)
        bounding = iamraw.BoundingBox.from_str(' '.join(splitted[0:4]))
        return (bounding, int(splitted[4]), splitted[5])

    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)

    pagedict = collections.defaultdict(list)
    for line in loaded:
        pagenumber = int(line['page'])
        if utila.should_skip(pagenumber, pages):
            continue
        for item in line['content']:
            multiboxed = []
            headlinenumber = item['headlinenumber']
            headlineblocknumber = item['headlineblocknumber']
            for single_collector in item['content']:
                boxed = []
                for multibox in single_collector:
                    m_bounding = iamraw.BoundingBox.from_str(
                        multibox['bounding'])
                    m_content = multibox['content']
                    boxid, _ = [  # boxid, index
                        int(item) for item in multibox['boxed_id'].split()
                    ]
                    m_content = [_parse_box_content(item) for item in m_content]
                    boxed.append((m_bounding, (boxid, m_content)))
                multiboxed.append(boxed)
            pagedict[pagenumber].append((
                headlinenumber,
                headlineblocknumber,
                multiboxed,
            ))
    result = []
    for page, value in pagedict.items():
        result.append(PageContentBoxed(page=page, content=value))
    return result
