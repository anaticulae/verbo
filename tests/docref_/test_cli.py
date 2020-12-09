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


def test_docref_help(monkeypatch):
    tests.docref_.run('--help', monkeypatch=monkeypatch)


@utilatest.longrun
def test_docref_bachelor37(testdir, monkeypatch):
    source = power.link(power.BACHELOR037_PDF)
    tests.docref_.run(f'-i {source}', monkeypatch=monkeypatch)
    path = testdir.tmpdir

    figures = serializeraw.load_docref(docref.path.docref_figure(path))
    assert len(figures) == 14  # may changes later

    tables = serializeraw.load_docref(docref.path.docref_table(path))
    assert len(tables) == 3
