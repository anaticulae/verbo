# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utilatest

import tests.textflow_
import textflow.features.lineending
import textflow.path


@utilatest.longrun
def test_textflow_lineendings(testdir, monkeypatch):
    tests.textflow_.run(
        f'-i {power.link(power.MASTER072_PDF)} --pages=0:10 --lineending',
        monkeypatch=monkeypatch,
    )
    source = textflow.path.lineending(testdir.tmpdir)

    endings = textflow.features.lineending.load_lineendings(source)
    assert len(endings) == 10
