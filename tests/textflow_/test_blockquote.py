# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import tests.resources
import tests.textflow_
import textflow.features.blockquote
import textflow.path


def test_blockquote_master72():
    source = tests.resources.MASTER72
    pages = (15,)

    ptcn = serializeraw.create_pagetextcontentnavigators_frompath(
        source,
        pages=pages,
    )
    extracted = textflow.features.blockquote.analyze_page(ptcn[0])
    assert len(extracted.content) == 2


def test_blockquote_validate_master72(testdir, monkeypatch):
    tests.textflow_.run(
        f'-i {tests.resources.MASTER72} --blockquote --pages=0:65',
        monkeypatch=monkeypatch,
    )

    path = textflow.path.blockquote(testdir.tmpdir)
    loaded = textflow.features.blockquote.load_blockquotes(path)

    current = [(item.page, len(item.content)) for item in loaded]
    expected = [(14, 1), (15, 2), (17, 1), (24, 1), (25, 1), (26, 1), (38, 1)]

    assert current == expected
