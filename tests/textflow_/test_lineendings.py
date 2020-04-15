# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests.resources
import tests.textflow_


def test_textflow_lineendings(testdir, monkeypatch):
    tests.textflow_.run(
        f'-i {tests.resources.MASTER72} --pages=0:10',
        monkeypatch=monkeypatch,
    )
