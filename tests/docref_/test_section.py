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

import docref.path
import tests.docref_


def test_section_master75_pages25_50(testdir, monkeypatch):
    source = power.link(power.MASTER075_PDF)
    cmd = f'-i {source} --section --pages=25:50'
    tests.docref_.run(cmd, monkeypatch=monkeypatch)

    path = docref.path.docref_section(testdir.tmpdir)
    loaded = serializeraw.load_docref(path)
    assert len(loaded) == 9  # TODO: VALIDATE LATER
