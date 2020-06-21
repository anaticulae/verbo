# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilatest

import tests
import tests.fixtures
import tests.resources


@pytest.mark.parametrize('command', [
    pytest.param(['--help'], id='help'),
    pytest.param(['--version'], id='version'),
    pytest.param(
        ['-i', tests.resources.RESTRUCT, '-o', '.'],
        id='restructured',
    ),
    pytest.param(
        ['-i', tests.resources.RESTRUCT, '-o', '.', '--pages', '0:9'],
        id='pages',
    ),
    pytest.param(['-i', tests.resources.MASTER72], id='master72'),
    pytest.param(['-i', tests.resources.PYPORTING], id='pyporting'),
])
@pytest.mark.usefixtures('testdir')
def test_run(command, monkeypatch, capsys):
    """Run help and version command to reach basic test coverage"""
    tests.run(command, monkeypatch=monkeypatch)
    tests.write_capsys(capsys)


@utilatest.skip_longrun
def test_feature_words_work_pages0_10(testdir, monkeypatch):
    root = str(testdir)
    cmd = f'-i {root} -o {root} --pages=0:10'

    tests.fixtures.setup_testresources(
        source=tests.resources.MASTER72,
        dest=root,
        accept=['rawmaker', 'sections', 'groupme'],
    )

    tests.run(cmd, monkeypatch=monkeypatch)
