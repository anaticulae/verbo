# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw
import utila
import utilatest

import tests
import words
import words.path

EXPECTED = os.path.join(words.ROOT, 'tests/headlines/expected')


class LazyFile:

    # TODO: MOVE TO UTILA

    def __init__(self, path):
        self.path = path
        self.content = None

    def lazy(self):
        if self.content is not None:
            return self.content
        self.content = utila.file_read(self.path).strip()
        return self.content

    def __eq__(self, value):
        self.lazy()
        return self.content == value

    def __str__(self):
        return self.lazy()


file_read = lambda x: LazyFile(os.path.join(EXPECTED, x))  # pylint:disable=C0103

DOCU027_HEADLINES = file_read('docu027')

BACHELOR037_HEADLINES = file_read('bachelor037')
BACHELOR051_HEADLINES = file_read('bachelor051')
BACHELOR063_HEADLINES = file_read('bachelor063')
BACHELOR090_HEADLINES = file_read('bachelor090')

DISS266_HEADLINES = file_read('diss266')

# TODO: 5.2 Die ´Demenzkampagne Ostfildern „Wir sind Nachbarn!“`: Oktober 2007 – Juni 2008
# 5.2 Die  ´Demenzkampagne  Ostfildern  „Wir  sind  Nachbarn!“`:
# 4. Zivilgesellschaftliche Perspektive und Bürgerschaftliches
BACHELOR128_HEADLINES = file_read('bachelor128')
# Anhang 1: Prävalenz von Demenzen in Abhängigkeit vom Al-
# Anhang 3: Freiwillig Engagierte und „nur“ gemeinschaftlich
# Anhang 4: Freiwillig Engagierte nach Altersgruppen
# Anhang 5: Freiwilliges Engagement und Bereitschaft zum
# Anhang 7: Leitfragebogen
# Anhang 8: Thesenpapier"""

MASTER98_HEADLINES = file_read('master098')
MASTER110_HEADLINES = file_read('master110')
MASTER155_HEADLINES = file_read('master155')

DISS264_HEADLINES = file_read('diss264')


# yapf:disable
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.DOCU27_PDF, None, DOCU027_HEADLINES, id='docu27'),
    pytest.param(power.BACHELOR037_PDF, None, BACHELOR037_HEADLINES, id='bachelor37'),
    pytest.param(power.BACHELOR051_PDF, '0:48', BACHELOR051_HEADLINES, id='bachelor51'),
    pytest.param(power.BACHELOR063_PDF, None, BACHELOR063_HEADLINES, id='bachelor63'),
    pytest.param(power.BACHELOR090_PDF, None, BACHELOR090_HEADLINES, id='bachelor90'),
    pytest.param(power.BACHELOR128_PDF, None, BACHELOR128_HEADLINES, id='bsc128'),
    pytest.param(power.MASTER098_PDF, None, MASTER98_HEADLINES, id='master98'),
    pytest.param(power.MASTER110_PDF, None, MASTER110_HEADLINES, id='master110',
        marks=pytest.mark.xfail(reason='require ffi special char converter'),
    ),
    pytest.param(power.MASTER155_PDF, MASTER155_HEADLINES, None, id='master155',
        marks=pytest.mark.xfail(reason='upgrading utila?'),
    ),
    pytest.param(power.DISS264_PDF, DISS264_HEADLINES, None, id='diss264',
        marks=pytest.mark.xfail,
    ),
    pytest.param(power.DISS266_PDF, '7:215', DISS266_HEADLINES, id='diss266'),
])
# yapf:enable
@utilatest.nightly
def test_headlines_validate(source, pages, expected, testdir, monkeypatch):
    src, pages = power.link(source), pages if isinstance(pages, str) else ':'
    tests.run(
        f'-i {src} --headlines -VVV --pages={pages}',
        monkeypatch=monkeypatch,
    )
    # ensure that lazy file is loaded
    expected = str(expected)

    oneline = serializeraw.load_headlines(words.path.oneline_headlines(testdir.tmpdir))  # yapf:disable
    oneline: str = raw_headlines(oneline)

    normal = serializeraw.load_headlines(words.path.headlines(testdir.tmpdir))
    normal: str = raw_headlines(normal)

    assert expected in (oneline, normal)


def raw_headlines(parsed) -> str:
    collected = []
    for chapter in parsed:
        for headline in chapter:
            if headline.level is None:
                intent = ''
            else:
                intent = (headline.level - 1) * '    '
            if headline.raw_level:
                line = intent + headline.raw_level + ' ' + headline.title
            else:
                line = intent + headline.title
            collected.append(line)
    return utila.NEWLINE.join(collected)
