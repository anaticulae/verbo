# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import utila

import words.headlines

SMALLEST_HEADLINE_DISTANCE = 1.2  # TODO: HOLY VALUE
SMALLEST_HEADLINE_TEXTSIZE = 1.1


class NoLevelHeadlineExtractor(words.headlines.HeadlineExtractorStrategy):

    def smallest_headlinedistance(self):
        return utila.roundme(self.textdistance * SMALLEST_HEADLINE_DISTANCE)

    def smallest_textsize(self):
        return utila.roundme(self.textsize * SMALLEST_HEADLINE_TEXTSIZE)

    def should_skip(
            self,
            distance_tosmall,
            headline_tosmall,
            textfeed,
            lastitem,
    ):
        if distance_tosmall and headline_tosmall:
            return True
        if headline_tosmall:
            return True
        return False
