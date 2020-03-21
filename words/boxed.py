# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from iamraw import BoundingBox

NO_BOX = -1


class BoxedChecker:
    # TODO: VERY SLOW, REPLACE WITH GOOD ONE, FOR THE FIRST TIME, TIME IS NOT
    # IMPORTANT.
    def __init__(self, boxes):
        assert isinstance(boxes, list), type(boxes)
        self.data = {}
        for page in boxes:
            content = []
            for box in page.content:
                bounding = box.box
                content.append(bounding)
            self.data[page.page] = content

    def contains(self, page, bounds) -> int:
        return self.boxid(page, bounds) >= 0

    def boxid(self, page, bounds) -> int:
        x0, y0, x1, y1 = bounds
        try:
            pagedata = self.data[page]
        except KeyError:
            return NO_BOX
        else:  # TODO: DO WE NEED ELSE?
            for index, bound in enumerate(pagedata):
                _x0, _y0, _x1, _y1 = bound
                if _y0 <= y0 <= y1 <= _y1 and _x0 <= x0 <= x1 <= _x1:
                    return index
        return NO_BOX

    def boundingbox(self, page, boxid: int) -> BoundingBox:
        """Return a copy of `BoundingBox` defined by `boxid`"""
        current = self.data[page][boxid]
        # copy BoundingBox
        copybox = BoundingBox.from_str(str(current))
        return copybox
