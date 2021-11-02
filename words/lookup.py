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


class LookupEmpty:

    @property
    def pages(self):
        # TODO: REMOVE LATER
        return []

    def __call__(self, page, line):  # pylint:disable=W0613
        return None


class PageLineLookup(LookupEmpty):

    def __init__(self):
        self.data = dict()

    def add(self, page, line, value):
        if page not in self.data:
            self.data[page] = dict()
        self.data[page][line] = value

    @property
    def pages(self):
        # TODO: REMOVE LATER
        result = []
        for page, values in self.data.items():
            content = list(values.items())
            insert = iamraw.PageContentContentType(page=page, content=content)
            result.append(insert)
        return result

    def __call__(self, page, line, default=None):
        try:
            return self.data[page][line]
        except KeyError:
            return default


def magics_frompath(path: str, pages: tuple = None) -> PageLineLookup:
    if not utila.exists(path):
        utila.log(f'skip loading magic: {path}')
        return LookupEmpty()
    loaded = serializeraw.load_magic_types(path, pages=pages)
    result = create_magics(loaded)
    return result


def create_magics(magics: iamraw.PageContentContentTypes):
    result = PageLineLookup()
    for page in magics:
        for item in page.content:
            result.add(page.page, line=item[0], value=item[1])
    return result
