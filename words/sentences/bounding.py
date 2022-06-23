# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import german
import iamraw
import konrad
import utila


def boundings(sentences, ptcns) -> iamraw.PageContent:
    result = collections.defaultdict(list)
    for chapter in sentences:
        for part in chapter.content:
            for line, page in zip(part.content, part.pages):
                bounding = find_bounding(
                    line,
                    utila.select_page(ptcns, page=page),
                )
                if not bounding:
                    utila.error(f'missing bounding on page: {page}; {line}')
                    bounding: tuple = tuple()
                result[page].append(bounding)
    # convert to result data type
    result: list = [
        iamraw.PageContent(page=page, content=content)
        for page, content in result.items()
    ]
    return result


def find_bounding(sentence: str, content) -> tuple:
    """Try to locate sentence on a page.

    1. Create lookup for every word on a page
    2. Split sentence into token
    3. Find largest pattern
    4. Optimize count of rectangles
    """
    lookup = lookup_create(content)
    page_content = [item[0] for item in lookup]
    pattern = [
        konrad.mark2str(item)
        for item in german.word_tokenize(sentence, validate_sentences=False)
    ]
    done = german.search(
        pattern=pattern,
        sentence=page_content,
        compare_content=True,
    )
    if not done:
        return None
    if len(done) > 1:
        utila.error(f'more than one matching sentence detected: {done}')
    rectangles = []
    for start, end in done:
        for index in utila.rlist(start, end):
            rectangles.append(lookup[index][1])
    result = optimize_bounding(rectangles)
    return result


def optimize_bounding(rectangles: list) -> list:
    """Merges bounding of token from sentence into fewer rectangles.

                    ||||||||||||
    ||||||||||||||||||||||||||||
    ||||||||||
    """
    # TODO: ADD A MORE COMPLEX MERGE STRATEGY
    result = utila.rect_max(rectangles)
    return result


@utila.cacheme
def lookup_create(content) -> list:
    """Split lines into token and there single word bounding."""
    result = []
    for line in content:
        bbox = line.bounding
        current = line.text
        tokens = [
            konrad.mark2str(item)
            for item in german.word_tokenize(current, validate_sentences=False)
        ]
        for token in tokens:
            cur_x = utila.findindex(current, token)
            if not cur_x:
                utila.debug(f'could not find token: {token} in {current}')
                continue
            cur_x = cur_x[0]
            text = current[cur_x:cur_x + len(token)]
            current = utila.ghost_replace(current, token)
            bounding = iamraw.split_x(
                bbox,
                part=cur_x,
                parts=len(current),
                width=len(text),
            )
            result.append((text, tuple(bounding)))
    return result
