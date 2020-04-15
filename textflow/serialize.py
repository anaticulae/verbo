# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

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
            raw = utila.from_raw_or_path(raw, ftype='yaml')
            loaded = yaml.load(raw, Loader=yaml.FullLoader)
            result = []
            for page in loaded:
                pagenumber = int(page['page'])
                print('hello')
                print(pagenumber)
                print(pages)
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
