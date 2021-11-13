# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import tests


def test_word_diss143page27(testdir, monkeypatch):
    source = power.link(power.DISS143_PDF)
    cmd = f'--text --page=26,27 -i {source} -o {testdir.tmpdir}'
    tests.run(cmd, monkeypatch=monkeypatch)
    loaded = serializeraw.load_text(testdir.tmpdir)
    assert loaded, 'missing headline?'
    assert '#$@FORMULA@$#:0' in str(loaded)
    assert '#$@FORMULA@$#:1' in str(loaded)
