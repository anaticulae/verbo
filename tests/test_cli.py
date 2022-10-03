# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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
    pytest.param(power.DOCU009_PDF, None, id='docu009'),
    pytest.param(power.DOCU027_PDF, '0:9', id='docu27pages'),
    pytest.param(power.MASTER072_PDF, None, id='master72'),
])
@pytest.mark.usefixtures('td')
@utilatest.nightly
def test_run_words(source, pages, mp, capsys):
    utilatest.fixture_requires(source)
    pages = pages if pages else ':'
    cmd = f'-i {power.link(source)} --pages {pages}'
    tests.run(cmd, mp=mp)
    utilatest.write_capsys(capsys)


@pytest.mark.parametrize('command', [
    pytest.param('--help', id='help'),
    pytest.param('--version', id='version'),
])
def test_run_words_basic(command, mp):
    """Run help and version command to reach basic test coverage"""
    tests.run(command, mp=mp)


@pytest.mark.xfail(reason='software integration')
@utilatest.nightly
@utilatest.requires(power.MASTER072_PDF)
def test_feature_words_work_pages0_10(td, mp):
    cmd = f'-i {td.tmpdir} -o {td.tmpdir} --pages=0:10'
    utila.copy_content(
        src=power.link(power.MASTER072_PDF),
        dst=td.tmpdir,
        pattern='(rawmaker|sections|groupme|headlines|words)__*.yaml',
        unlock=True,
    )
    tests.run(cmd, mp=mp)
