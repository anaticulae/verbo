# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import docref.path
import tests.docref_


@utilatest.longrun
def test_docref_master116_bibliography(testdir, monkeypatch):
    source = power.link(power.MASTER116_PDF)
    tests.docref_.run(
        f'-i {source} --bibliography',
        monkeypatch=monkeypatch,
    )
    bibliography = docref.path.docref_bibliography(testdir.tmpdir)
    bibliography = serializeraw.load_docref(bibliography)
    assert len(bibliography) == 87  # NOT VALIDATED YET
