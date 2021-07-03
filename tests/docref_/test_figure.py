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

import docref.path
import tests.docref_


@utilatest.requires(power.MASTER075_PDF)
def test_figure_master75_pages6(testdir, monkeypatch):
    source = power.link(power.MASTER075_PDF)
    cmd = f'-i {source} --figure --pages=7:21'
    tests.docref_.run(cmd, monkeypatch=monkeypatch)

    path = docref.path.docref_figure(testdir.tmpdir)
    loaded = serializeraw.load_docref(path)
    assert len(loaded) == 5
