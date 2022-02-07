# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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


def file_read(name: str) -> str:
    expected = os.path.join(words.ROOT, 'tests/headlines/expected')
    path = os.path.join(expected, name)
    if not utila.exists(path):
        return '', path
    return utila.file_read(path).strip(), path


# TODO: 5.2 Die ´Demenzkampagne Ostfildern „Wir sind Nachbarn!“`: Oktober 2007 – Juni 2008
# 5.2 Die  ´Demenzkampagne  Ostfildern  „Wir  sind  Nachbarn!“`:
# 4. Zivilgesellschaftliche Perspektive und Bürgerschaftliches
# Anhang 1: Prävalenz von Demenzen in Abhängigkeit vom Al-
# Anhang 3: Freiwillig Engagierte und „nur“ gemeinschaftlich
# Anhang 4: Freiwillig Engagierte nach Altersgruppen
# Anhang 5: Freiwilliges Engagement und Bereitschaft zum
# Anhang 7: Leitfragebogen
# Anhang 8: Thesenpapier"""


# yapf:disable
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR037_PDF, None, 'bachelor037', id='bachelor37'),
    pytest.param(power.BACHELOR051_PDF, '0:48', 'bachelor051', id='bachelor51'),
    pytest.param(power.BACHELOR063_PDF, None, 'bachelor063', id='bachelor63'),
    pytest.param(power.BACHELOR067_PDF,  None, 'bachelor067', id='bachelor067'),
    pytest.param(power.BACHELOR076_PDF, None, 'bachelor076', id='bachelor076'),
    pytest.param(power.BACHELOR090_PDF, None, 'bachelor090', id='bachelor90'),
    pytest.param(power.BACHELOR128_PDF, None, 'bachelor128', id='bachelor128'),
    pytest.param(power.BOOK173_PDF, None, 'book173', id='book173'),
    pytest.param(power.DISS172_PDF, None, 'diss172', id='diss172'),
    pytest.param(power.DISS205_PDF,  None, 'diss205', id='diss205'),
    pytest.param(power.DISS218_PDF,  None, 'diss218', id='diss218'),
    pytest.param(power.DISS266_PDF, '7:215', 'diss266', id='diss266'),
    pytest.param(power.DISS178_PDF,  None, 'diss178', id='diss178'),
    pytest.param(power.MASTER072_PDF, None, 'master072', id='master072'),
    pytest.param(power.MASTER075_PDF, None, 'master075', id='master075'),
    pytest.param(power.MASTER098_PDF, None, 'master098', id='master98'),
    pytest.param(power.MASTER099_PDF, None, 'master099', id='master099'),
    pytest.param(power.MASTER110_PDF, None, 'master110', id='master110'),
    pytest.param(power.MASTER116_PDF, None, 'master116', id='master116'),
    pytest.param(power.MASTER155_PDF,  None, 'master155', id='master155'),
    pytest.param(power.DISS264_PDF, None, 'diss264', id='diss264'),
    pytest.param(power.DOCU027_PDF, None, 'docu027', id='docu27',
        marks=pytest.mark.xfail,
    ),
])
# yapf:enable
@utilatest.nightly
def test_headlines_validate(source, pages, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    expected, paths = file_read(expected)
    src, pages = power.link(source), pages if isinstance(pages, str) else ':'
    tests.run(
        f'-i {src} --headlines -VVV --pages={pages}',
        monkeypatch=monkeypatch,
    )
    oneline = serializeraw.load_headlines(words.path.oneline_headlines(testdir.tmpdir))  # yapf:disable
    oneline: str = raw_headlines(oneline)

    normal = serializeraw.load_headlines(words.path.headlines(testdir.tmpdir))
    normal: str = raw_headlines(normal)

    if expected not in (oneline, normal):
        utila.file_create('oneline', oneline)
        utila.file_create('normal', normal)
        utila.log('NORMAL')
        utila.log(normal)
        utila.log('ONELINE')
        utila.log(oneline)
        utila.log('EXPECTED')
        utila.log(expected)
        # ease debugging: if the result is not correct take the assumption
        # that the bigger file may the better file
        if normal or oneline:
            content = normal if len(normal) >= len(oneline) else oneline
            content = content.rstrip() + utila.NEWLINE
            utila.file_replace(
                paths,
                content,
            )
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
