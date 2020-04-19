# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider_textrule.features.quotation_mark
import decider_textrule.quotation_mark as dq
import tests.fixtures.master72.seventytwo as fseventytwo
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
    first = words.text.word.split_words(
        words.text.sentence.split_sentences(STANDARD)[0])

    assert dq.valid_double_marks_count(first)
    assert dq.valid_single_marks_count(first)


def test_chapter_split_words():
    required = fseventytwo.textrequired(pages=(13, 14))
    pages = words.text.chapter.split(required)

    result = decider_textrule.features.quotation_mark.validate_sentences(pages)
    assert len(result[0]) == 1, str(result)
    assert not result[1], str(result)


REQUIRE_SINGLE_INSIDE = """\
Bevor die Konzepte der Privatheit und Öffentlichkeit
systemtheoretisch näher betrachtet werden, soll vorab kurz umrissen
werden, was darunter verstanden wird. Rössler beschreibt etwas
Privates folgendermaßen: „‚privat‘ nennen wir einerseits Handlungs-
und Verhaltensweisen, zum Zweiten ein bestimmtes Wissen und drittens
Räume“ und weiter: „als privat gilt etwas dann, wenn man selbst
den Zugang zu diesem „etwas“ kontrollieren kann“. Privatheit
beinhaltet also den Aspekt der Zugangskontrolle seitens des
Individuums.
"""


def test_validate_count_of_double_quotation():
    splitted = words.text.sentence.split_sentences(REQUIRE_SINGLE_INSIDE)
    assert len(splitted) == 5

    third = words.text.word.split_words(splitted[2])
    assert dq.valid_double_marks_count(third)

    fourth = words.text.word.split_words(splitted[3])
    double_inside_double = dq.valid_double_marks_count(fourth)
    assert double_inside_double is False


def test_valid_english_quotation_marks():
    required = fseventytwo.textrequired(pages=(17))
    pages = words.text.chapter.split(required)

    result = decider_textrule.features.quotation_mark.validate_sentences(pages)
    expected = [(17, 6), (17, 12)]
    assert result.double == expected, str(result)
