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

ARCHIVE = utilo.join(words.ROOT, 'tests/text/expected', exist=True)

param = pytest.param


@pytest.mark.parametrize('source, pages, expected', [
    param(hoverpower.BACHELOR028_PDF, '2:23', 'bachelor028', id='bachelor028'),
    param(hoverpower.BACHELOR051_PDF, '3:42', 'bachelor051', id='bachelor051'),
    param(hoverpower.BACHELOR063_PDF, '4:43', 'bachelor063', id='bachelor063'),
    param(hoverpower.BACHELOR067_PDF, '8:55', 'bachelor067', id='bachelor067'),
    param(hoverpower.BACHELOR090_PDF, '11:76', 'bachelor090', id='bachelor090'),
    param(hoverpower.BACHELOR128_PDF, '6:96', 'bachelor128', id='bachelor128'),
    param(hoverpower.DISS143_PDF, '19:131', 'diss143', id='diss143'),
    param(hoverpower.DISS172_PDF, '17:152', 'diss172', id='diss172'),
    param(hoverpower.DISS205_PDF, '16:18', 'diss205p1617', id='diss205p1617'),
    param(hoverpower.DISS205_PDF, None, 'diss205', id='diss205all'),
    param(hoverpower.DISS218_PDF, '9:184', 'diss218', id='diss218'),
    param(hoverpower.DISS266_PDF, '7:213', 'diss266', id='diss266'),
    param(hoverpower.MASTER072_PDF, '30', 'master072p30', id='master072p30'),
    param(hoverpower.MASTER072_PDF, '3:64', 'master072', id='master072'),
    param(hoverpower.MASTER075_PDF, '5:69', 'master075', id='master075'),
    param(hoverpower.MASTER098_PDF, '1:88', 'master098', id='master098'),
    param(hoverpower.MASTER110_PDF, '19:104', 'master110', id='master110'),
    param(hoverpower.MASTER116_PDF, '7:88', 'master116', id='master116'),
    param(hoverpower.MASTER155_PDF, '8:77', 'master155', id='master155'),
])
@utilotest.nightly
def test_validate_text(source, pages, expected, td, mp):
    utilotest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=pages,
        expected=expected,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()
    # TODO: USE SECTIONS TO SELECT PAGES


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.run,
                mp=mp,
            ),
            step='text',
            pages=pages,
            source=hoverpower.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
            index=expected,
        )
        self.headlines = hoverpower.link(source)

    def frompath(self, path):  # pylint:disable=R0201
        headlines = serializeraw.load_headlines(self.headlines)
        text = serializeraw.load_text(path, headlines=headlines)
        return text

    def raw(self, value) -> str:
        value = utilo.flatten_content(value)
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
        result = utilo.NEWLINE.join(collected)
        return result
