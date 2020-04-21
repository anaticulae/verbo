# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw

import words.feature.word
from tests.fixtures.restruct import restructured_boxed
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_list_work
from tests.fixtures.restruct import restructured_textexample


def restructured_words():
    text = serializeraw.dump_text(restructured_textexample())
    headlines = restructured_headlines()
    boxed = serializeraw.dump_boxedcontent(restructured_boxed())
    lists = serializeraw.dump_lists(restructured_list_work())
    # dumped data as input
    for item in [
            boxed,
            headlines,
            lists,
            text,
    ]:
        assert isinstance(item, str), str(item)

    # compare text, headlines, lists and boxes to one output
    text, listlookup, boxlookup = words.feature.word.load_resources(
        boxed=boxed,
        headlines=headlines,
        lists=lists,
        text=text,
    )

    result = words.feature.word.process_words(text, listlookup, boxlookup)
    assert result
    return result


@pytest.mark.xfail(reason='unable to merge undefined sections correctly')
def test_dump_and_load_words_result():
    word_ = restructured_words()
    headlines = restructured_headlines()
    dumped = serializeraw.dump_text(word_)
    headlines = serializeraw.load_headlines(headlines)
    loaded = serializeraw.load_text(dumped, headlines)
    assert loaded == word_
