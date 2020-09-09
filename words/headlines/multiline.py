# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import statistics

import configo
import german
import iamraw
import texmex
import utila

import words.headlines
import words.headlines.standard as whs

# longer word chains may be a sentence or something else
MAX_HEADLINE_TOKEN_LENGTH = configo.HV_INT_PLUS(20)
# assume that headlines does not contain many numbers
MAX_NUMBERS_IN_HEADLINE = configo.HV_INT_PLUS(5)


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

    def extract_page(  # pylint:disable=R1260
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
            if wrong_position(items):
                continue
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
            text = utila.normalize_whitespaces(text)
            # TODO: REPLACE WITH LEVEL DETERMINER
            # with contextlib.suppress(TypeError):
            #     text = parsed['text'].strip()  # TODO: REMOVE STRIP LATER
            try:
                raw_level = parsed['level'].strip()  # TODO: REMOVE STRIP LATER
            except TypeError:
                raw_level = text
            level = words.headlines.numbered_level(raw_level)
            if level is False:
                continue
            if noheadline(text):
                continue

            if len(items) == 1:  # TODO: CHECK THIS
                container = items.firstid
            else:
                container = (items.firstid, items.firstid + len(items) - 1)
            headline = iamraw.Headline(
                container=container,
                level=level,
                page=pagecontent.page,
                raw_level=raw_level,
                title=text,
            )
            result.append(headline)
        return result


def noheadline(text: str) -> bool:
    text = text.strip()
    if not text:
        return True
    if issentence(text):
        # ignore extracted lists which are interpreted as headlines
        return True
    if text.count('.') > 5:
        return True
    wordslength = [len(word) for word in text.split()]
    mean_words_length = statistics.mean(wordslength)
    if mean_words_length <= 3.0:
        return True
    return False


HEADLINE_MEDIAN = configo.HolyTable(  # TODO: HOLY VALUE
    left_outranges_none=False,
    right_outranges_none=False,
)
# TODO: REPLACE AFTER UPGRADING CONFIGO
# HEADLINE_MEDIAN.add(10, 55)
# FONTSIZE; MINIMAL MEDIAN CHAR LENGTH
HEADLINE_MEDIAN.add(10, 40)
HEADLINE_MEDIAN.add(12, 35)
HEADLINE_MEDIAN.add(14, 30)
HEADLINE_MEDIAN.add(16, 26)
HEADLINE_MEDIAN.add(22, 16)


def possible_headline_group(items) -> bool:
    text = ' '.join([item.text for item in items])
    words_ = german.split_words(text, validate_sentences=False)
    if len(words_) >= MAX_HEADLINE_TOKEN_LENGTH:
        # maybe a sentence cause headlines are not so long
        return False

    number_count = len([item for item in words_ if utila.isnumber(item)])
    if number_count >= MAX_NUMBERS_IN_HEADLINE:  # TODO: HOLY VALUE
        # assume that headlines does not contain many numbers
        return False

    if len(items) >= 2:  # multiline
        # In general, multiline headlines fill the whole line. If this
        # does not happen, it is other content which is false positive
        # parsed as headline.
        line_length = [len(item.text) for item in items.text]
        median = statistics.median(line_length)
        if median <= HEADLINE_MEDIAN(items.size):
            return False
    return True


def issentence(line: str):
    # TODO: IMPROVE THIS
    # TODO: USE BIG FIVE FEATURES
    return line.strip().endswith('.')


def wrong_position(
        items,
        max_x0: float = 200.0,  # HOLY VALUE
):
    """We assume that headlines start on the left side of the document.
    This should skip false possitive headline extraction.

    TODO: RUN SECOND EXTRACTION WITHOUT LEFTSTARTED AND COMPARE TO
    SUPPORT RIGHT ALIGNED HEADLINES?
    """
    return items.bounding[0] >= max_x0
