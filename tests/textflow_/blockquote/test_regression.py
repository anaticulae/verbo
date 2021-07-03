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
import utilatest

import tests.textflow_
import textflow.path


def test_noblockquote_bachelor51page21(testdir, monkeypatch):
    detected = run_blockquote(
        power.BACHELOR051_PDF,
        testdir,
        monkeypatch,
        pages='21',
    )
    assert not detected


def run_blockquote(source, testdir, monkeypatch, pages=':'):
    utilatest.fixture_requires(source)
    source = power.link(source)
    tests.textflow_.run(
        f'-i {source} --blockquote --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = textflow.path.blockquote(testdir.tmpdir)
    loaded = serializeraw.load_blockquotes(path)
    return loaded
