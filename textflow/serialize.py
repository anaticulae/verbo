# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import iamraw
import serializeraw
import utila
import yaml

PageContent = collections.namedtuple('PageContent', 'content, page')


def dumpme(func):
    # TODO: MOVE TO IAMRAW

    def dumper(items) -> str:
        result = []
        for page in items:
            rawpage = []
            for line in page.content:
                raw = func(line)
                rawpage.append(raw)
            result.append({'page': page.page, 'content': rawpage})
        dumped = yaml.dump(result)
        return dumped

    return dumper


def loadme(func=None, ctor=PageContent):

    def decorating_function(user_function):

        def loader(raw: str, pages: tuple = None):
            loaded = utila.yaml_from_raw_or_path(raw, safe=False)
            result = []
            for page in loaded:
                pagenumber = int(page['page'])
                if utila.should_skip(pagenumber, pages):
                    continue
                content = []
                for line in page['content']:
                    parsed = user_function(line)
                    content.append(parsed)
                result.append(ctor(page=pagenumber, content=content))
            return result

        return loader

    if func is None:
        return decorating_function
    return decorating_function(func)


def dump_wordspaces(items) -> str:

    def dumper(lines) -> list:
        result = []
        for number, content in lines:
            content = utila.from_tuple(utila.flatten(content))
            line = f'{number} {content}'
            result.append(line)
        return result

    dumped = serializeraw.dump_pagecontent(items, pagedumper=dumper)
    return dumped


def load_wordspaces(content: str, pages: tuple = None) -> iamraw.PageContents:

    def loader(page) -> iamraw.PageContent:
        result = []
        for line in page:
            number, content = line.split(maxsplit=1)
            # TODO: IMPROVE THIS METHOD
            content = content.split()
            content = [
                utila.parse_tuple(' '.join(chunk))
                for chunk in utila.chunks(content, size=4)
            ]
            result.append((int(number), content))
        return result

    loaded = serializeraw.load_pagecontent(
        content,
        pages=pages,
        pageloader=loader,
        fname='textflow__wordspace_wordspace',
    )
    return loaded
