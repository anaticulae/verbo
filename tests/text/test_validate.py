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

ARCHIVE = utila.join(words.ROOT, 'tests/text/expected', exist=True)

param = pytest.param


@pytest.mark.parametrize('source, pages, expected', [
    param(power.BACHELOR028_PDF, '2:23', 'bachelor028', id='bachelor028'),
    param(power.BACHELOR051_PDF, '3:42', 'bachelor051', id='bachelor051'),
    param(power.BACHELOR063_PDF, '4:43', 'bachelor063', id='bachelor063'),
    param(power.BACHELOR067_PDF, '8:55', 'bachelor067', id='bachelor067'),
    param(power.BACHELOR090_PDF, '11:76', 'bachelor090', id='bachelor090'),
    param(power.BACHELOR128_PDF, '6:96', 'bachelor128', id='bachelor128'),
    param(power.DISS143_PDF, '19:131', 'diss143', id='diss143'),
    param(power.DISS172_PDF, '17:152', 'diss172', id='diss172'),
    param(power.DISS205_PDF, '16:18', 'diss205p1617', id='diss205p1617'),
    param(power.DISS205_PDF, None, 'diss205', id='diss205all'),
    param(power.DISS218_PDF, '9:184', 'diss218', id='diss218'),
    param(power.DISS266_PDF, '7:213', 'diss266', id='diss266'),
    param(power.MASTER072_PDF, '30', 'master072p30', id='master072p30'),
    param(power.MASTER072_PDF, '3:64', 'master072', id='master072'),
    param(power.MASTER075_PDF, '5:69', 'master075', id='master075'),
    param(power.MASTER098_PDF, '1:88', 'master098', id='master098'),
    param(power.MASTER110_PDF, '19:104', 'master110', id='master110'),
    param(power.MASTER116_PDF, '7:88', 'master116', id='master116'),
    param(power.MASTER155_PDF, '8:77', 'master155', id='master155'),
])
@utilatest.nightly
def test_validate_text(source, pages, expected, td, mp):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=pages,
        expected=expected,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()
    # TODO: USE SECTIONS TO SELECT PAGES


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.run,
                mp=mp,
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
