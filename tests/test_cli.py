# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests


@pytest.mark.parametrize('source, pages', [
    pytest.param(power.DOCU027_PDF, '0:9', id='docu27pages'),
    pytest.param(power.MASTER072_PDF, None, id='master72'),
    pytest.param(power.DOCU009_PDF, None, id='pyporting'),
])
@pytest.mark.usefixtures('testdir')
@utilatest.requires(power.DOCU009_PDF)
@utilatest.requires(power.DOCU027_PDF)
@utilatest.requires(power.MASTER072_PDF)
@utilatest.nightly
def test_run_words(source, pages, monkeypatch, capsys):
    """Run help and version command to reach basic test coverage"""
    pages = pages if pages else ':'
    cmd = f'-i {power.link(source)} --pages {pages}'
    tests.run(cmd, monkeypatch=monkeypatch)
    utilatest.write_capsys(capsys)


@pytest.mark.parametrize('command', [
    pytest.param('--help', id='help'),
    pytest.param('--version', id='version'),
])
def test_run_words_basic(command, monkeypatch):
    """Run help and version command to reach basic test coverage"""
    tests.run(command, monkeypatch=monkeypatch)


@utilatest.nightly
@utilatest.requires(power.MASTER072_PDF)
def test_feature_words_work_pages0_10(testdir, monkeypatch):
    cmd = f'-i {testdir.tmpdir} -o {testdir.tmpdir} --pages=0:10'
    utila.copy_content(
        src=power.link(power.MASTER072_PDF),
        dest=testdir.tmpdir,
        pattern='(rawmaker|sections|groupme)__*.yaml',
    )
    tests.run(cmd, monkeypatch=monkeypatch)
