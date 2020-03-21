# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import dataclasses
import typing


@dataclasses.dataclass
class HeadlineWithContent:
    text: str = None
    content: typing.List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class PageTextWithHeadlines:
    page: int = None
    content: typing.List[HeadlineWithContent] = dataclasses.field(default_factory=list) # yapf:disable

PageAnalyzeResources = collections.namedtuple(
    'PageAnalyzeResources',
    'number, headlines, pagetextcontentnavigator, fontcontentstore',
)


@dataclasses.dataclass
class TextSection:
    headline: str = None
    content: typing.List = dataclasses.field(default_factory=list)

    def __getitem__(self, index):
        # TODO: support tuple unpacking, remove later
        if index > 1:
            raise IndexError
        return self.headline if index == 0 else self.content

    def __eq__(self, value):
        # TODO: support tuple unpacking, remove later
        return self[0] == value[0] and self[1] == value[1]


TextSections = typing.List[TextSection]


@dataclasses.dataclass
class PageContentPageTextDetected:
    page: int = None
    content: list = None

    def __getitem__(self, index):
        # TODO: support tuple unpacking, remove later
        if index > 1:
            raise IndexError
        return self.page if index == 0 else self.content

    def __eq__(self, value):
        # TODO: support tuple unpacking, remove later
        return self[0] == value[0] and self[1] == value[1]


PageContentPageTextDetecteds = typing.List[PageContentPageTextDetected]
