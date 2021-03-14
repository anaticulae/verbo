# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utilatest

import tests.fixtures.master72.seventytwo as fseventytwo
import tests.fixtures.text
import words.text.sentence


@utilatest.longrun
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


def master72_text(pages: tuple) -> str:
    required = fseventytwo.textrequired(pages)
    pages = words.text.chapter.split(required)
    assert pages
    # merge sentences
    merged = words.text.sentence.merge_sentences(pages)
    sentences = [item.sentence for item in merged]
    text = utila.NEWLINE.join(sentences)
    return text


def bachelor51_text(pages: tuple = None) -> str:
    required = tests.fixtures.text.bachelor051_textrequired(pages=pages)
    pages = words.text.chapter.split(required)
    # merge sentences
    merged = words.text.sentence.merge_sentences(pages)
    sentences = [item.sentence for item in merged]
    text = utila.NEWLINE.join(sentences)
    return text


@utilatest.longrun
def test_merge_sentences_before_headline_regression():
    text = master72_text((14,))
    assert 'Ausgewählte Positionen hierzu werden im Folgenden dargestellt.' in text
    assert len(text.splitlines()) == 12


def test_merge_sentences_list_detection_regression():
    text = master72_text((9,))
    # no list starter in text
    assert '&#61607;' not in text
    # list start
    assert '12u' in text
    # list end
    assert '27u' in text


def test_merge_sentences_footer_regression():
    text = master72_text((21,))
    # ensure that footer is not parsed as text
    assert 's. Michael Zimmer' not in text
    assert 'www.spiegel.de' not in text


def test_merge_sentences_table_regression():
    text = bachelor51_text((21,))
    assert 'Tab. 2: Untersuchungsplan' in text  # TODO: CHANGE AFTER SUPPORTING CAPTION
    # exclude table content from sentence matcher
    assert 'Probandenstichprobe' not in text


def test_merge_sentences_figure_regression():
    text = bachelor51_text((31,))
    # exclude figure from sentence detection
    assert 'Präwert' not in text
    assert 'Postwert' not in text
    assert 'Abb. 4: Skalawerte' in text  # TODO: CHANGES LATER
