# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests


@pytest.mark.parametrize('command', [
    pytest.param(['--help'], id='help'),
    pytest.param(['--version'], id='version'),
    pytest.param(
        ['-i', power.link(power.DOCU27_PDF), '-o', '.'],
        id='restructured',
    ),
    pytest.param(
        ['-i', power.link(power.DOCU27_PDF), '-o', '.', '--pages', '0:9'],
        id='pages',
    ),
    pytest.param(['-i', power.link(power.MASTER072_PDF)], id='master72'),
    pytest.param(['-i', power.link(power.DOCU09_PDF)], id='pyporting'),
])
@pytest.mark.usefixtures('testdir')
@utilatest.nightly
def test_run_words(command, monkeypatch, capsys):
    """Run help and version command to reach basic test coverage"""
    tests.run(command, monkeypatch=monkeypatch)
    utilatest.write_capsys(capsys)


@utilatest.longrun
def test_feature_words_work_pages0_10(testdir, monkeypatch):
    root = str(testdir)
    cmd = f'-i {root} -o {root} --pages=0:10'

    utila.copy_content(
        source=power.link(power.MASTER072_PDF),
        destination=root,
        pattern='(rawmaker|sections|groupme)__*.yaml',
    )
    tests.run(cmd, monkeypatch=monkeypatch)
