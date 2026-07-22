# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilotest

import tests.fixtures.master72.seventytwo as fseventytwo
import words.text.sentence


@utilotest.longrun
def test_chapter_word_tokenize():
    required = fseventytwo.textrequired(pages=(13, 14))
    pages = words.text.chapter.split(required)
    assert pages
