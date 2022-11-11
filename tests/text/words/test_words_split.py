# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utilatest

import tests
import tests.fixtures.master72.seventytwo as fseventytwo
import words.text.chapter
import words.text.sentence

MASTER72_EXPECTED = {
    30: 18,
    31: 6 + 12,
    32: 20,
    33: 9 + 5,
    34: 18,
}


@utilatest.nightly
def test_validate_words_split_master72():
    pages = tuple(MASTER72_EXPECTED.keys())
    required = fseventytwo.textrequired(pages=pages)
    extracted_pages = words.text.chapter.split(required)
    for page in extracted_pages:
        expected = MASTER72_EXPECTED[page.page]
        sentences = utila.flat(
            [item[1] for item in words.text.sentence.find_sentences(page)])
        tests.assert_length(sentences, expected, msg=f'page: {page.page}')
