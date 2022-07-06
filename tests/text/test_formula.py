# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import tests


@utilatest.nightly
def test_word_diss143page27(testdir, monkeypatch):
    source = power.link(power.DISS143_PDF)
    cmd = f'--text --page=26,27 -i {source} -o {testdir.tmpdir}'
    tests.run(cmd, monkeypatch=monkeypatch)
    loaded = serializeraw.load_text(testdir.tmpdir)
    assert loaded, 'missing headline?'
    assert '#$@FORMULA@$#:0' in str(loaded)
    assert '#$@FORMULA@$#:1' in str(loaded)


@utilatest.longrun
def test_word_home50page31(testdir, monkeypatch):
    """Regression test that line before '4.1 Auswahl des
    Shuntwiderstands ' does not generate any formula.
    """
    source = power.link(power.HOME050_PDF)
    cmd = f'--text -i {source} -o {testdir.tmpdir} --pages=31'
    tests.run(cmd, monkeypatch=monkeypatch)
    loaded = utila.flatten_content(serializeraw.load_text(testdir.tmpdir))
    raw = utila.NEWLINE.join(utila.flatten_content(loaded))
    assert raw.count('#$@FORMULA@$#:0') == 1
