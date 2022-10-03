# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import tests


@pytest.mark.xfail(reason='software integration')
@utilatest.requires(power.BACHELOR067_PDF)
def test_sentences_bachelor067pages51(td, mp):
    source = power.link(power.BACHELOR067_PDF)
    cmd = f'--sentences --page=50,51 -i {source} -o {td.tmpdir}'
    tests.run(cmd, mp=mp)
    sentences = serializeraw.load_text('words__sentences_sentences.yaml')
    sentences = utila.flatten_content(utila.flatten_content(sentences))
    assert len(sentences) == 11  # VALIDATED
