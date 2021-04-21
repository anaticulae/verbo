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

import tests
import words.path


def test_links_master75(testdir, monkeypatch):
    # TODO: MASTER75 TEXT SECTION EXTRACTION IS BROKEN
    loaded = hyperlinks(power.MASTER075_PDF, testdir, monkeypatch)
    assert len(loaded) == 22


def hyperlinks(source, testdir, monkeypatch, pages=':'):
    cmd = f'-i {power.link(source)} --links --pages={pages}'
    tests.run(cmd, monkeypatch=monkeypatch)
    loaded = serializeraw.load_hyperlinks(words.path.links(testdir.tmpdir))  # pylint:disable=e1101
    return loaded
