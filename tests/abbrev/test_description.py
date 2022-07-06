# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import tests


@utilatest.longrun
def test_description_bachelor028p3(testdir, monkeypatch):
    source = power.link(power.BACHELOR028_PDF)
    cmd = f'-i {source} -o {testdir.tmpdir} --abbreviation --pages=3'
    tests.run(cmd, monkeypatch=monkeypatch)
    abbreviation = utila.flatten_content(
        serializeraw.load_text_abbreviations(testdir.tmpdir))
    expected = {None, 'multinationaler Unternehmen'}
    descriptions = {item.description for item in abbreviation}
    assert descriptions == expected
