# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import tests.fixtures.master72.seventytwo as fseventytwo
import words.text.chapter
import words.text.sentence as wts


def test_text_seventytwo_extract_texts():
    required = fseventytwo.textrequired(pages=(3))
    extracted = words.text.chapter.extract_texts(required)
    assert extracted

    firstpage = utila.select_page(extracted, 3)
    firstsection = firstpage.content[0]
    sectioncontent = firstsection.content

    assert len(sectioncontent) == 17


@utila.skip_longrun
def test_text_seventytwo_visit_sentences():
    required = fseventytwo.textrequired(pages=(3))
    firstpage = words.text.chapter.split(required)[0]
    required = fseventytwo.textrequired(pages=(4))
    secondpage = words.text.chapter.split(required)[0]

    sentences = list(wts.visit_sentences(firstpage))
    assert len(sentences) == 17

    sentences = list(wts.visit_sentences(secondpage))
    assert len(sentences) == 14

    # second page first sentence
    assert sentences[0][1] == ('Nutzerverhalten vor allem in '
                               'Bezug auf die Privatheitsthematik.')

    # second page second sentence
    assert sentences[1][1] == ('Massenmedien und Literatur sehen die '
                               'Privatsphäre in Gefahr und äußern daher zum '
                               'Teil massive Kritik an der Selbstpräsentation '
                               'der Nutzer.')


def test_text_seventytwo_visit_sentences_merge_page_endstart():
    """Merge the first two content pages to one sentence unit. Important
    is to unite the last sentence of the first page with the first
    sentence of the second page and merge them to one sentence."""
    required = fseventytwo.textrequired(pages=(3, 4))
    pages = words.text.chapter.split(required)

    merged = list(wts.merge_sentences(pages))
    assert len(merged) == 30

    merged_middle_sentence = merged[16][1]
    assert merged_middle_sentence == (
        'Kritisch beurteilt wird das '
        'Nutzerverhalten vor allem in Bezug auf die Privatheitsthematik.')

    # ensure that every sentence has a headline
    assert all([item is not None for item, _ in merged])

    # ensure that every sentence has content
    assert all([item is not None for _, item in merged])


def test_text_seventytwo_visit_sentences_merge_page5_7():
    required = fseventytwo.textrequired(pages=(5, 6, 7))
    pages = words.text.chapter.split(required)
    merged = list(wts.merge_sentences(pages))

    assert merged[10][0].text == (
        '2. Das Social Web und die Privatsphäre – '
        'Selbstdarstellungsverhalten der Nutzer aus Sicht von Massenmedien und '
        'Literatur')
    assert merged[10][1] == (
        'Im Folgenden geht es zunächst um eine definitorische Einführung in '
        'den Bereich der Social Media sowie um die Eigenschaften netzbasierter '
        'Kommunikation, die für das Social Web von Bedeutung sind.')
    lastsentence = ('Es sind Anwendungen entstanden, welche die '
                    'soziale Komponente in den Vordergrund')
    assert merged[-1][1] == lastsentence


@utila.skip_longrun
def test_text_seventytwo_visit_chapters():
    required = fseventytwo.textrequired(pages=tuple(range(0, 14)))
    pages = words.text.chapter.split(required)

    chapters = list(wts.visit_chapters(pages))
    minpage = min([headline.page for headline, _ in chapters])
    assert minpage == 3, minpage
    # '1.  Einleitung'
    # Headline(text=None, level=None, rawlevel=None, page=4, container=-1)
    # '1.1  Fragestellung und Zielsetzung'
    # '1.2  Aufbau der Arbeit'
    # '2.  Das Social Web und die Privatsphre '
    # '2.1  Web  2.0,  Social  Web  und  Social  Media:  Abgrenzungen  und'
    # Headline(text=None, level=None, rawlevel=None, page=7, container=-1)
    # Headline(text=None, level=None, rawlevel=None, page=8, container=-1)
    # Headline(text=None, level=None, rawlevel=None, page=9, container=-1)
    # Headline(text=None, level=None, rawlevel=None, page=10, container=-1)
    # '2.2  Merkmale von Social Network Sites'
    # Headline(text=None, level=None, rawlevel=None, page=11, container=-1)
    # '2.3  Eigenschaften netzbasierter Kommunikation'
    # '2.4  Einfhrung in das Konzept der Privatheit'
    sectionpages = [headline.page for headline, _ in chapters]
    assert sectionpages == [3, 4, 5, 6, 6, 10, 12, 13]


@utila.skip_longrun
def test_text_seventytwo_visit_chapters_page5_6_7():
    required = fseventytwo.textrequired(pages=(5, 6, 7))
    pages = words.text.chapter.split(required)

    chapters = list(wts.visit_chapters(pages))
    assert len(chapters) == 3

    headlines = [headline for headline, _ in chapters]
    assert all([item.text is not None for item in headlines])

    sentences = [sentence for _, sentence in chapters]
    count = [len(item) for item in sentences]
    # check sentence count for different sections
    assert count == [10, 2, 26], str(count)

    lastsentence = chapters[-1][1][-1]
    assert lastsentence == ('Es sind Anwendungen entstanden, welche die '
                            'soziale Komponente in den Vordergrund')


@utila.skip_longrun
def test_text_seventytwo_visit_chapters_complete():
    required = fseventytwo.textrequired()
    pages = words.text.chapter.split(required)

    chapters = list(wts.visit_chapters(pages))

    # user content headlines, Literverzeichnis and Eidesstattliches are
    # excluded cause there are part of appendix.
    master72_headline_count = 30
    assert len(chapters) == master72_headline_count


def test_text_seventytwo_extract_sentences():
    expected = fseventytwo.firstpage_sentences()
    raw = ' '.join(expected)
    splitted = wts.split_sentences(raw)

    assert len(splitted) == len(expected)
    assert splitted == expected


@pytest.mark.xfail(reason='multiple equal fontdistance, think about later')
def test_text_doubleequal_fontdistance():
    required = fseventytwo.textrequired(pages=(0))
    extracted = words.text.chapter.extract_texts(required)
    assert extracted
