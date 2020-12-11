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


def extract_label(source, testdir, monkeypatch):
    source = power.link(source)
    tests.docref_.run(
        f'-i {source} --bibliography',
        monkeypatch=monkeypatch,
    )
    bibliography = docref.path.docref_bibliography(testdir.tmpdir)
    bibliography = serializeraw.load_docref(bibliography)
    return bibliography


@utilatest.longrun
def test_docref_bibliography_master116(testdir, monkeypatch):
    # TODO: Changes after support more tech label
    bibliography = extract_label(power.MASTER116_PDF, testdir, monkeypatch)
    assert len(bibliography) == 86  # NOT VALIDATED YET


@utilatest.longrun
def test_docref_bibliography_master98(testdir, monkeypatch):
    bibliography = extract_label(power.MASTER098_PDF, testdir, monkeypatch)
    assert len(bibliography) == 257  # NOT VALIDATED YET
