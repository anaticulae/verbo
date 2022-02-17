# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import texmex.sentences
import utila

import tests


def test_sentences_master110pages67(testdir, monkeypatch):
    source = power.link(power.MASTER110_PDF)
    cmd = f'--sentences --page=67 -i {source} -o {testdir.tmpdir}'
    tests.run(cmd, monkeypatch=monkeypatch)
    output = utila.file_read('words__sentences_sentences.yaml')
    counted = output.count(texmex.sentences.LIST_SEPA)
    # 6 list items in generated sentences
    assert counted == 6
