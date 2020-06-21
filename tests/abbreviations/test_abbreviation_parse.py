# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw
import utilatest

import tests
import tests.resources
import words.feature.abbreviation
import words.path


@pytest.fixture
def bachelor37(testdir, monkeypatch):
    source = testdir.tmpdir
    tests.run(
        f'-i {tests.resources.BACHELOR37}',
        monkeypatch=monkeypatch,
    )
    text = words.path.text(source)
    headlines = words.path.headlines(source)
    pages = tuple(range(6, 10))
    result = words.feature.abbreviation.work(text, headlines, pages=pages)
    return result


@utilatest.skip_longrun
def test_abbreviation_parse_page(bachelor37):  # pylint:disable=W0621
    result = bachelor37
    assert len(result) > 100, str(result)


@utilatest.skip_longrun
def test_abbreviation_dump_load_parsed_abbreviation(bachelor37):  # pylint:disable=W0621
    expected = bachelor37
    loaded = serializeraw.load_text_abbreviations(expected)
    dumped = serializeraw.dump_text_abbreviations(loaded)
    assert dumped == expected, dumped
