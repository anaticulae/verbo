# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex
import utila

import words.headlines
import words.headlines.standard as whs


class MultiLine(words.headlines.HeadlineExtractorStrategy):

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

    def smallest_headlinedistance(self):
        return 0

    def smallest_textsize(self):
        return utila.roundme(self.textsize)

    def extract_page(
            self,
            pagecontent: texmex.PageTextNavigator,
    ) -> iamraw.Headlines:
        """Extract headlines on selected page

        Args:
            pagecontent: content of page to extract headlines
        Returns:
            Extracted list of iamraw.Headline.
        """
        result = []
        grouped = texmex.group_page_by_size_distance(pagecontent)
        for items in grouped:
            # TODO: REMOVE LATER
            text = ' '.join([item.text.strip() for item in items])
            # text = ' '.join([item.text for item in items])
            parsed = whs.parse_headline(text)
            if not parsed:
                text = text.strip()
                if text not in words.headlines.WHITELIST:
                    continue
            if issentence(text):
                # ignore extracted lists which are interpreted as headlines
                continue
            text = normalize_whitespaces(text)
            # TODO: REPLACE WITH LEVEL DETERMINER
            try:
                rawlevel = parsed['level'].strip()
            except TypeError:
                rawlevel = text
            level = rawlevel.count('.') + 1
            if rawlevel.endswith('.'):
                level = 1
            if len(items) == 1:
                container = items.firstid
            else:
                container = (items.firstid, items.firstid + len(items) - 1)
            headline = iamraw.Headline(
                container=container,
                level=level,
                page=pagecontent.page,
                rawlevel=rawlevel,
                text=text,
            )
            result.append(headline)
        return result


def normalize_whitespaces(line):
    token = [item for item in line.split(' ') if item]
    return ' '.join(token)


def issentence(line: str):
    # TODO: IMPROVE THIS
    # TODO: USE BIG FIVE FEATURES
    return line.strip().endswith('.')
