# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw

import tests


@pytest.mark.xfail(reason='improve oneline/normal indexing')
def test_word_master110pages67(testdir, monkeypatch):
    """Ensure that area-attribute is splitted by list content.

    Example: 0l_0, 0l_0; 0l_1; 0l_2
    """
    source = power.link(power.MASTER110_PDF)
    cmd = f'--word --page=67 -i {source} -o {testdir.tmpdir}'
    tests.run(cmd, monkeypatch=monkeypatch)
    loaded = serializeraw.load_text('words__word_result.yaml', pages=67)
    content = loaded[0].content[0].content
    expected = 'beschreibt die erforderlichen Schritte, um die von einem Objekt'
    error = 'sentence seems to mixed in lists/undefined parsing'
    assert expected in str(content), error
    assert all(item in content for item in '0l0 0l1 0l2 0l3 0l4 0l5'.split())
