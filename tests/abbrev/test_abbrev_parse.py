# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila

import tests
import words.path


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


BACHELOR37 = utila.splititems("""AG ANOVA BP BPM CD CX EKG EN ENBP FMRI IAPS \
IL MA MD MATLAB MDHF PASW PET PFC RS SAM SD SEM SPSS HF US USA al. bzw. ca. \
etc. s. \u2212md
""")


@pytest.mark.xfail(reason='???')
def test_bachelor37abbr(testdir, monkeypatch):
    extracted = abbr(power.BACHELOR037_PDF, '5:33', testdir, monkeypatch, True)
    extracted = sorted(utila.lower(*extracted))
    expected = sorted(BACHELOR37)
    assert extracted == expected
