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
import utila
import utilatest

import tests
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


def abbr(source, pages, testdir, monkeypatch, flat: bool = False):
    source = power.link(source)
    cmd = f'-i {source} -o {testdir.tmpdir} --abbreviation --pages={pages}'
    tests.run(cmd, monkeypatch=monkeypatch)
    abbrpath = words.path.abbr(testdir.tmpdir)
    result = serializeraw.load_text_abbreviations(abbrpath)
    if flat:
        result = [[item.short for item in page.content] for page in result]
        result = utila.flatten(result)
        result = utila.make_unique(result)
    return result


BACHELOR37 = ('PFC al. IAPS US FMRI s. bzw. ENBP EN BP SAM SD= I) II III RS CX '
              'EKG etc. PASW SPSS IL USA ANOVA SA SEM AG CD MATLAB MA BPM ca. '
              'F( T( MB PM SD M= MDHF \u2212MD HF Z= PET')


def test_bachelor37abbr(testdir, monkeypatch):
    extracted = abbr(power.BACHELOR037_PDF, '5:33', testdir, monkeypatch, True)
    raw = ' '.join(extracted)
    assert raw == BACHELOR37


def test_abbreviation_dump_load_parsed_abbreviation():
    expected = bachelor37()
    loaded = serializeraw.load_text_abbreviations(expected)
    dumped = serializeraw.dump_text_abbreviations(loaded)
    assert dumped == expected, dumped
