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

import tests
import words.path


@utilatest.requires(power.MASTER075_PDF)
def test_links_master75(testdir, monkeypatch):
    # TODO: MASTER75 TEXT SECTION EXTRACTION IS BROKEN
    loaded = hyperlinks(power.MASTER075_PDF, testdir, monkeypatch)
    assert len(loaded) == 22


@utilatest.requires(power.MASTER075_PDF)
def test_links_master75_pages15(testdir, monkeypatch):
    loaded = hyperlinks(power.MASTER075_PDF, testdir, monkeypatch, 15)
    assert len(loaded) == 1
    hyperlink = loaded[0].href
    assert hyperlink.startswith('https')
    assert hyperlink.endswith('index.html')
    assert loaded[0].visited


def hyperlinks(source, testdir, monkeypatch, pages=':'):
    cmd = f'-i {power.link(source)} --links --pages={pages}'
    tests.run(cmd, monkeypatch=monkeypatch)
    loaded = serializeraw.load_hyperlinks(words.path.links(testdir.tmpdir))  # pylint:disable=e1101
    return loaded
