# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import tests.resources
import tests.textflow_
import textflow.path


@utilatest.longrun
def test_blockquote_master72():
    source = power.link(power.MASTER072_PDF)
    pages = (15,)

    textsize = 12.0  # TODO: NOT VALIDATED
    ptcn = serializeraw.create_pagetextcontentnavigators_frompath(
        source,
        pages=pages,
    )
    extracted = textflow.features.blockquote.analyze_page(
        ptcn[0],
        textsize=textsize,
    )
    assert len(extracted.content) == 2


@utilatest.longrun
def test_blockquote_validate_master72(testdir, monkeypatch):
    tests.textflow_.run(
        f'-i {power.link(power.MASTER072_PDF)} --blockquote --pages=0:65',
        monkeypatch=monkeypatch,
    )

    path = textflow.path.blockquote(testdir.tmpdir)
    loaded = serializeraw.load_blockquotes(path)

    current = [(item.page, len(item.content)) for item in loaded]
    expected = [(14, 1), (15, 2), (17, 1), (24, 1), (25, 1), (26, 1), (38, 1)]
    assert current == expected


@utilatest.longrun
def test_blockquote_validate_bachelor76_page8_11_13_15_16(testdir, monkeypatch):
    tests.textflow_.run(
        f'-i {power.link(power.BACHELOR076_PDF)} --blockquote --pages=8:17',
        monkeypatch=monkeypatch,
    )
    path = textflow.path.blockquote(testdir.tmpdir)
    loaded = serializeraw.load_blockquotes(path)

    expected = [(8, 1), (11, 1), (13, 1), (15, 1), (16, 2)]
    current = [(item.page, len(item.content)) for item in loaded]
    assert current == expected


@utilatest.longrun
def test_blockquote_validate_master98(testdir, monkeypatch):
    tests.textflow_.run(
        f'-i {power.link(power.MASTER098_PDF)} --blockquote --pages=0:17',
        monkeypatch=monkeypatch,
    )
    path = textflow.path.blockquote(testdir.tmpdir)
    loaded = serializeraw.load_blockquotes(path)

    expected = [(2, 1), (3, 1), (7, 2), (8, 1), (11, 1), (12, 1), (13, 1),
                (15, 1)]
    current = [(item.page, len(item.content)) for item in loaded]
    assert current == expected
