# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
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
            if not possible_headline_group(items):
                continue
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
            text = utila.normalize_whitespaces(text)
            # TODO: REPLACE WITH LEVEL DETERMINER
            try:
                rawlevel = parsed['level'].strip()  # TODO: REMOVE STRIP LATER
            except TypeError:
                rawlevel = text
            level = numbered_level(rawlevel)
            if len(items) == 1:  # TODO: CHECK THIS
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


def numbered_level(raw: str) -> int:
    """Convert number to raw level.

    >>> numbered_level('5')
    1
    >>> numbered_level('2.')
    1
    >>> numbered_level('2.1.3.')
    3
    >>> numbered_level('2.1')
    2
    >>> numbered_level('2..1...') # ignore typos
    2
    """
    # TODO: MOVE TESTS?
    raw = raw.strip()
    if not '.' in raw:
        return 1 if raw.isnumeric() else None
    # 2.1.3
    splitted = [item for item in raw.split('.') if item]
    return len(splitted)


def possible_headline_group(items) -> bool:
    text = ' '.join([item.text for item in items])
    words_ = german.split_words(text, validate_sentences=False)
    if len(words_) >= 20:  # TODO: HOLY VALUE
        # maybe a sentence but headlines are not so long
        return False

    number_count = len([item for item in words_ if isnumber(item)])
    if number_count >= 5:  # TODO: HOLY VALUE
        # assume that headlines does not contain many numbers
        return False
    return True


def isnumber(token: str):
    return str(token).isnumeric()


def issentence(line: str):
    # TODO: IMPROVE THIS
    # TODO: USE BIG FIVE FEATURES
    return line.strip().endswith('.')
