# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import tests


@utilotest.nightly
@utilotest.requires(hoverpower.DISS143_PDF)
def test_word_diss143page27(td, mp):
    source = hoverpower.link(hoverpower.DISS143_PDF)
    cmd = f'--text --page=26,27 -i {source} -o {td.tmpdir}'
    tests.run(cmd, mp=mp)
    loaded = serializeraw.load_text(td.tmpdir)
    assert loaded, 'missing headline?'
    assert '#$@FORMULA@$#:0' in str(loaded)
    assert '#$@FORMULA@$#:1' in str(loaded)


@pytest.mark.xfail(reason='software integration')
@utilotest.longrun
@utilotest.requires(hoverpower.HOME050_PDF)
def test_word_home50page31(td, mp):
    """Regression test that line before '4.1 Auswahl des
    Shuntwiderstands ' does not generate any formula.
    """
    source = hoverpower.link(hoverpower.HOME050_PDF)
    cmd = f'--text -i {source} -o {td.tmpdir} --pages=31'
    tests.run(cmd, mp=mp)
    loaded = utilo.flatten_content(serializeraw.load_text(td.tmpdir))
    raw = utilo.NEWLINE.join(utilo.flatten_content(loaded))
    assert raw.count('#$@FORMULA@$#:0') == 1
