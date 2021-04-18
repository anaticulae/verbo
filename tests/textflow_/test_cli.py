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
import utilatest

import tests
import tests.textflow_
import textflow.serialize


def test_textflow_cli(monkeypatch):
    tests.textflow_.run('--help', monkeypatch=monkeypatch)


@utilatest.longrun
def test_textflow_alignments_restruct(testdir, monkeypatch):
    """Ensure that document with empty page is parsed correctly."""
    source = power.link(power.DOCU27_PDF)
    tests.run(f'-i {source}', monkeypatch=monkeypatch)
    tests.textflow_.run(f'-i {source}', monkeypatch=monkeypatch)


@pytest.mark.parametrize('source', [
    pytest.param(power.link(power.MASTER072_PDF), id='master72'),
    pytest.param(power.link(power.DOCU09_PDF), id='pyporting'),
])
@utilatest.nightly
def test_textflow_alignments(source, testdir, monkeypatch):
    """Ensure that document with empty page is parsed correctly."""
    tests.run(f'-i {source}', monkeypatch=monkeypatch)
    tests.textflow_.run(f'-i {source}', monkeypatch=monkeypatch)


@utilatest.longrun
def test_textflow_wordspace_bachelor56page4(testdir, monkeypatch):
    source = power.link(power.BACHELOR056_PDF)
    tests.textflow_.run(
        f'-i {source} --wordspace --pages=4',
        monkeypatch=monkeypatch,
    )
    loaded = textflow.serialize.load_wordspaces(testdir.tmpdir)
    dumped = textflow.serialize.dump_wordspaces(loaded)
    again = textflow.serialize.load_wordspaces(dumped)
    assert again == loaded
