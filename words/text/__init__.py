# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import dataclasses


@dataclasses.dataclass
class HeadlineWithContent:
    text: str = None
    content: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class PageTextWithHeadlines:
    page: int = None
    content: list[HeadlineWithContent] = dataclasses.field(default_factory=list)


PageAnalyzeResources = collections.namedtuple(
    'PageAnalyzeResources',
    'number, headlines, pagetextcontentnavigator, fontcontentstore',
)

TextSections = list[TextSection]


@dataclasses.dataclass
class PageContentPageTextDetected:
    page: int = None
    content: list = None


PageContentPageTextDetectedList = list[PageContentPageTextDetected]
