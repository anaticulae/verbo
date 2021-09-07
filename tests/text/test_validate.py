# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import utila
import utilatest

import words
import words.feature
import words.text.sentence


def load_expected(name) -> str:
    source = os.path.join(words.ROOT, f'tests/text/expected/{name}')
    content = utila.file_read(source)
    return content


@pytest.mark.xfail(reason='require some little changes')
@utilatest.longrun
def test_validate_master072_text():
    source = power.MASTER072_PDF
    pages = utila.ranged_tuple(3, 64)

    raw = load_current(source, pages)
    expected = load_expected('master072')

    assert raw == expected


# yapf:disable
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR051_PDF, utila.ranged_tuple(3, 42), 'bachelor051', id='bachelor051',
    marks=pytest.mark.xfail(reason='not ready yet')),
    pytest.param(power.DISS266_PDF, utila.ranged_tuple(7, 213), 'diss266', id='diss266',
    marks=pytest.mark.xfail(reason='not ready yet')),
    pytest.param(power.DISS205_PDF, utila.ranged_tuple(16, 18), 'diss205p1617', id='diss205p1617'),
])
# yapf:enable
@utilatest.nightly
def test_text_validate(source, pages, expected, testdir):
    raw = load_current(source, pages)
    expected = load_expected(expected)
    if raw != expected:
        utila.log(raw)
        utila.file_create(os.path.join(testdir.tmpdir, 'baseline'), raw)
    assert raw == expected


def load_current(source, pages) -> str:
    resources = words.feature.load_resources_frompath(
        power.link(source),
        pages=pages,
    )
    splitted = words.text.chapter.split(resources)
    merged = words.text.sentence.merge_sentences(splitted)
    collected = []
    headline = None
    for item in merged:
        if item.headline != headline:
            collected.append(f'\n\n:::: {item.headline.title} ::::\n\n')
            headline = item.headline
        if item.sentence:
            # skip None-Sentence between two headlines without content
            collected.append(item.sentence)
    result = utila.NEWLINE.join(collected) + utila.NEWLINE
    return result
