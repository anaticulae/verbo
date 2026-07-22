# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import tests
import words

ARCHIVE = utilo.join(words.ROOT, 'tests/abbrev/expected', exist=True)


@pytest.mark.parametrize(
    'source',
    utilotest.test_resources(tests.conftest.RESOURCES),
)
@utilotest.nightly
def test_validate_abbrev(source, td, mp):
    utilotest.fixture_requires(source)
    Evaluate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.run,
                mp=mp,
            ),
            step='abbreviation',
            pages=hoverpower.ctext(source, default=':'),
            source=hoverpower.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
        )

    def frompath(self, path):  # pylint:disable=R0201
        path = utilo.join(path, 'words__abbreviation_detected.yaml')
        abbrev = serializeraw.load_text_abbreviations(path)
        return abbrev

    def raw(self, value) -> str:
        value = utilo.flatten_content(value)
        collected = []
        for item in value:
            line = str(item.position.page).zfill(3) + ' '
            line += str(item.position.sentence).zfill(2) + ' '
            line += item.short
            if item.description:
                line += ' ' + item.description
            collected.append(line)
        result = utilo.NEWLINE.join(collected)
        return result
