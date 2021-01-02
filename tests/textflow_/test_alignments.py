# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests.textflow_
import textflow.features.alignment
import textflow.path
import textflow.serialize


@utilatest.longrun
def test_textflow_alignment_expected(testdir, monkeypatch):
    tests.textflow_.run(
        f'-i {power.link(power.MASTER072_PDF)} --pages=10:20 --alignment',
        monkeypatch=monkeypatch,
    )
    source = textflow.path.alignment(testdir.tmpdir)
    current = textflow.features.alignment.load_alignment(source)

    assert current
    assert len(current) == 10, str(current)


@pytest.mark.xfail(reason='unsupported block_end')
@utilatest.longrun
def test_alignment_master98_page2(testdir, monkeypatch):
    tests.textflow_.run(
        f'-i {power.link(power.MASTER098_PDF)} --pages=2 --alignment',
        monkeypatch=monkeypatch,
    )
    source = textflow.path.alignment(testdir.tmpdir)
    current = textflow.features.alignment.load_alignment(source)

    content = utila.select_content(current, 2)

    assert content[4] == textflow.alignment.style.TextAlignment.BLOCK_END
