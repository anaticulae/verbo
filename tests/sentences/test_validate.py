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
import iamraw
import pytest
import serializeraw
import utilo
import utilotest

import tests
import words

ARCHIVE = utilo.join(words.ROOT, 'tests/sentences/expected', exist=True)

param = pytest.param


@pytest.mark.parametrize('source, pages, expected', [
    param(hoverpower.BOOK173_PDF, '13:30', 'book173', id='book173'),
    param(hoverpower.MASTER072_PDF, '13:18', 'master072', id='master072'),
    param(hoverpower.BACHELOR032A_PDF, '12', 'bachelor032a', id='bachelor032a'),
])
@utilotest.nightly
def test_validate_sentence(source, pages, expected, td, mp):
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
            step='sentence',
            pages=pages,
            source=hoverpower.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
            index=expected,
        )
        self.headlines = hoverpower.link(source)

    def frompath(self, _):  # pylint:disable=W0613
        headlines = serializeraw.load_headlines(self.headlines)
        path = iamraw.path.words_sentences(self.workdir)
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
