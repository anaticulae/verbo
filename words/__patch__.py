# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import dataclasses
import functools
import os

import configo
import groupme.toc.group
import iamraw
import serializeraw
import utila
import yaml


@dataclasses.dataclass
class Headline:
    title: str
    level: int = dataclasses.field(default=0)
    raw: str = dataclasses.field(default=None)
    raw_level: str = dataclasses.field(default=None, compare=False)
    page: int = dataclasses.field(default=-1)
    container: int = dataclasses.field(default=None)
    decoration: tuple = dataclasses.field(default=None)

    @property
    def start(self):
        with contextlib.suppress(TypeError):
            return self.container[0]  # pylint:disable=E1136
        return self.container

    @property
    def end(self):
        with contextlib.suppress(TypeError):
            return self.container[1]  # pylint:disable=E1136
        return self.container


iamraw.Headline = Headline


def dump_headlines(headlines: iamraw.PagesHeadlineList) -> str:
    raw = []
    for index, page in enumerate(headlines):
        content = []
        for item in page:
            container = item.container
            if isinstance(container, tuple):
                container = utila.from_tuple(container)
            content.append({
                'container': container,
                'level': item.level,
                'page': item.page,
                'raw': item.raw,
                'raw_level': item.raw_level,
                'title': item.title,
                'decoration': item.decoration,
            })
        if not content:
            # do not write empty pages
            continue
        raw.append({
            'chapter?': index,  # TODO: How to deal with empty chapter?
            'headlines': content,
        })
    dumped = yaml.safe_dump(raw)
    return dumped


serializeraw.dump_headlines = dump_headlines


@functools.lru_cache(configo.CACHE_SMALL)
def load_headlines(content: str, pages=None) -> iamraw.PagesHeadlineList:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.safe_load(content)
    result = []
    for step in loaded:
        loadedstep = []
        for headline in step['headlines']:
            pagenumber = int(headline['page'])
            if utila.should_skip(pagenumber, pages):
                continue
            try:
                container = int(headline['container'])
            except ValueError:
                # support ranged container id
                container = utila.parse_tuple(  # pylint:disable=R0204
                    headline['container'],
                    length=2,
                    typ=int,
                )
            level = headline['level']
            if level is not None:
                level = int(level)
            else:
                utila.error(f'headline level is None: {headline["title"]}')
            item = iamraw.Headline(
                container=container,
                level=level,
                page=pagenumber,
                raw=headline['raw'],
                raw_level=headline['raw_level'],
                title=headline['title'],
                decoration=headline.get('decoration', None),
            )
            loadedstep.append(item)
        if loadedstep:
            result.append(loadedstep)
    return result


serializeraw.load_headlines = load_headlines


def numbered_level(raw: str) -> int:
    """Convert number to raw level.

    >>> numbered_level('5 Geology')
    1
    >>> numbered_level('2. Zentrum')
    1
    >>> numbered_level('2.1.3. Abschluss')
    3
    >>> numbered_level('2.1 Anhang')
    2
    >>> numbered_level('2..1... Fehlerfrei') # ignore typos
    2
    >>> numbered_level('2020 This is not a headline level')
    False
    >>> numbered_level('04.03.2016. No Headline')
    False
    """
    # TODO: SUPPORT LEVEL WITHOUT SPACE
    # TODO: MOVE TESTS?
    raw = raw.strip()
    if not raw:
        return None
    raw = raw.split()[0]
    try:
        splitted = [int(item) for item in raw.split('.') if item]
        if max(splitted) > 20:
            return False
    except ValueError:
        return None
    return len(splitted)


groupme.toc.group.numbered_level = numbered_level


def exists(path: str) -> bool:
    """Wrapper for os.path.exists with checking None and convert path to
    str if required.

    >>> exists(__file__)
    True
    >>> exists(None)
    False
    >>> exists(1234)
    False
    """
    if path is None:
        return False
    path = str(path)
    return os.path.exists(path)


utila.exists = exists
