# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import docref.path
import docref.serialize
import tests.docref_


def test_docref_help(monkeypatch):
    tests.docref_.run('--help', monkeypatch=monkeypatch)


def test_docref_bachelor37(testdir, monkeypatch):
    source = power.link(power.BACHELOR037_PDF)
    tests.docref_.run(f'-i {source}', monkeypatch=monkeypatch)
    path = testdir.tmpdir

    figures = docref.serialize.load_docref(docref.path.docref_figure(path))
    assert len(figures) == 11  # may changes later

    tables = docref.serialize.load_docref(docref.path.docref_table(path))
    assert len(tables) == 3
