# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import power
import pytest
import serializeraw
import utila
import utilatest

import tests
import words

ARCHIVE = os.path.join(words.ROOT, 'tests/text/expected')
utila.exists_assert(ARCHIVE)


# yapf:disable
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR051_PDF, '3:42', 'bachelor051', id='bachelor051', marks=pytest.mark.xfail(reason='not ready yet')),
    pytest.param(power.MASTER072_PDF, '3:64', 'master072', id='master072', marks=pytest.mark.xfail(reason='requires little changes')),
    pytest.param(power.DISS205_PDF, '16:18', 'diss205p1617', id='diss205p1617'),
    pytest.param(power.DISS205_PDF, None, 'diss205', id='diss205all'),
    # pytest.param(power.DISS266_PDF, utila.ranged_tuple(7, 213), 'diss266', id='diss266', marks=pytest.mark.xfail(reason='not ready yet')),
])
# yapf:enable
@utilatest.nightly
def test_text_validate(source, pages, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=pages,
        expected=expected,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.run,
                monkeypatch=monkeypatch,
            ),
            step='text',
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
            index=expected,
        )
        self.headlines = power.link(source)

    def frompath(self, path):  # pylint:disable=R0201
        headlines = serializeraw.load_headlines(self.headlines)
        text = serializeraw.load_text(path, headlines=headlines)
        return text

    def raw(self, value) -> str:
        value = utila.flatten_content(value)
        collected = []
        headline = None
        for item in value:
            if item.headline != headline:
                if item.headline.title:
                    collected.append(f'\n\n:::: {item.headline.title} ::::\n\n')
                headline = item.headline
            if item.content:
                # skip None-Sentence between two headlines without content
                collected.extend(item.content)
        result = utila.NEWLINE.join(collected)
        return result
