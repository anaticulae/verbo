# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import tests
import words

ARCHIVE = utila.join(words.ROOT, 'tests/abbrev/expected', exist=True)


@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR028_PDF, id='bachelor028'),
])
@utilatest.nightly
def test_validate_abbrev(source, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.run,
                monkeypatch=monkeypatch,
            ),
            step='abbreviation',
            pages=':',
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
        )

    def frompath(self, path):  # pylint:disable=R0201
        path = utila.join(path, 'words__abbreviation_detected.yaml')
        abbrev = serializeraw.load_text_abbreviations(path)
        return abbrev

    def raw(self, value) -> str:
        value = utila.flatten_content(value)
        collected = []
        for item in value:
            line = str(item.position.page).zfill(3) + ' '
            line += str(item.position.sentence).zfill(2) + ' '
            line += item.short
            if item.description:
                line += ' ' + item.description
            collected.append(line)
        result = utila.NEWLINE.join(collected)
        return result
