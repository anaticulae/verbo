# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import tests.fixtures.master72.seventytwo as fseventytwo
import words.text.sentence


def test_merge_sentences_merge_divis():
    required = fseventytwo.textrequired(pages=(13, 14))
    pages = words.text.chapter.split(required)
    assert pages

    notmerged = words.text.sentence.merge_sentences(pages, merge_divis=False)
    text = utila.NEWLINE.join([item.sentence for item in notmerged])
    assert 'Kontrollmöglichkeiten' not in text

    merged = words.text.sentence.merge_sentences(pages)
    sentences = [item.sentence for item in merged]
    text = utila.NEWLINE.join(sentences)
    # ensure that divis is replaced correctly
    assert 'Kontrollmöglichkeiten' in text
