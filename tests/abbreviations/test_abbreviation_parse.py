# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import words.feature.abbreviation
import words.path


def bachelor37():
    utilatest.fixture_requires(power.BACHELOR037_PDF)
    source = power.link(power.BACHELOR037_PDF)
    pages = tuple(range(6, 10))
    text = words.path.text(source)
    headlines = words.path.headlines(source)
    result = words.feature.abbreviation.work(text, headlines, pages=pages)
    return result


def test_abbreviation_parse_page():
    result = bachelor37()
    assert len(result) > 100, str(result)


def test_abbreviation_dump_load_parsed_abbreviation():
    expected = bachelor37()
    loaded = serializeraw.load_text_abbreviations(expected)
    dumped = serializeraw.dump_text_abbreviations(loaded)
    assert dumped == expected, dumped
