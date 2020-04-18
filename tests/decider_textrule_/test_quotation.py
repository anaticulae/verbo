# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import words.text.sentence
import words.text.word

STANDARD = """„Protest“, so schreibt Sigrid Baringhorst, „ist
kommunikatives Handeln“ (1998: 327). Will man das Phänomen ‚Protest‘
angemessen erfassen, so gilt es zu untersuchen, wie er kommuniziert
wird."""

MIXED = """‚Soziale Bewegung‘ – dieser Begriff beschreibt ein Gebilde,
das analytisch schwer zu fassen ist. Van de Donk u.a. (2004b: 3)
beschreiben soziale Bewegungen als „fuzzy and fluid phenomena often
without clear boundaries“, und fügen hinzu: „In sum, a social movement
is a ‚moving target’, difficult to observe.” Dennoch soll im Folgenden
der Versuch einer Definition vorgenommen werden."""


def test_split_paragraph_with_quotation():
    splitted = words.text.sentence.split_sentences(STANDARD)
    assert len(splitted) == 2


def test_split_paragraph_with_quotation_mixed():
    splitted = words.text.sentence.split_sentences(MIXED)
    assert len(splitted) == 4
    last = ('Dennoch soll im Folgenden der Versuch einer '
            'Definition vorgenommen werden.')
    assert splitted[-1] == last, splitted


def test_split_words_with_quotation():
    first = words.text.sentence.split_sentences(STANDARD)[0]
    word = words.text.word.split_words(first)
    print(word)
    assert 0
