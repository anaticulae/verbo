# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import tests.textflow_


def test_textflow_cli(monkeypatch):
    tests.textflow_.run('--help', monkeypatch=monkeypatch)


def test_textflow_alignments_restruct(testdir, monkeypatch):
    """Ensure that document with empty page is parsed correctly."""
    tests.textflow_.run(
        f'-i {tests.resources.RESTRUCT}',
        monkeypatch=monkeypatch,
    )


@pytest.mark.parametrize('source', [
    pytest.param(tests.resources.MASTER72, id='master72'),
    pytest.param(tests.resources.PYPORTING, id='pyporting'),
])
def test_textflow_alignments(source, testdir, monkeypatch):
    """Ensure that document with empty page is parsed correctly."""
    tests.textflow_.run(f'-i {source}', monkeypatch=monkeypatch)
