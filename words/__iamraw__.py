# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import texmex
import utila


@dataclasses.dataclass
class MultilineGroup:
    """Group of following text lines with equal properties.

    Public Attributes:
        text: content as a list of following texmex.TextInfo.
        size: font size of common content.
    """
    text: list = dataclasses.field(default_factory=list)
    size: float = None
    firstid: int = None
    bounding: tuple = None

    def append(self, item):
        self.text.append(item)  # pylint:disable=E1101

    def __getitem__(self, index):
        return self.text[index]  # pylint:disable=E1136

    def __len__(self):
        return len(self.text)

    def content_and_index(self):
        assert self.firstid is not None, 'create MultilineGroup with firstid'
        for index, item in enumerate(self, start=self.firstid):
            yield index, item


def group_page_by_size_distance(content: texmex.PageTextNavigator):
    assert isinstance(content, texmex.NavigatorMixin), type(content)
    grouped = texmex.group_linedistances_complex(content)
    result = []
    for group in grouped:
        groupcontent = [content[index] for index in group]
        groupcontent = merge_group(groupcontent)
        # TODO: make container more pythonic
        size = groupcontent[0].style.content[0].size
        firstid = group[0]
        bounding = rectangle_single([item.bounding for item in groupcontent])
        result.append(
            MultilineGroup(
                bounding=bounding,
                firstid=firstid,
                size=size,
                text=groupcontent,
            ))
    return result


def merge_group(items):
    if not items:
        return items
    result = [items[0]]
    for item in items[1:]:
        before = result[-1]
        ynear = utila.near(item.bounding[3], before.bounding[3], diff=5.0)
        xnear = utila.near(item.bounding[0], before.bounding[2], diff=1.0)
        if ynear and xnear:
            # merge before
            before.text = before.text.strip() + item.text
            before.bounding[2] = item.bounding[2]
            before.style.content.extend(item.style.content)
        else:
            result.append(item)
    return result


def rectangle_single(items: list) -> tuple:
    # TODO: REPLACE WITH UTILA CODE
    assert items, 'no rectangles given'
    x0 = utila.mins(item[0] for item in items)
    x1 = utila.maxs(item[2] for item in items)
    y0 = utila.mins(item[1] for item in items)
    y1 = utila.maxs(item[3] for item in items)
    return x0, y0, x1, y1


texmex.MultilineGroup = MultilineGroup
texmex.group_page_by_size_distance = group_page_by_size_distance
