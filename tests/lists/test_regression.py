# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila

import tests
import words.path


def test_nolist_bachelor241_page81(testdir, monkeypatch):
    """This test was designed cause on this page table content was
    parsed as lists."""
    source = power.link(power.BACHELOR241_PDF)
    tests.run(f'-i {source} --pages=81 --list', monkeypatch=monkeypatch)

    loaded = serializeraw.load_lists(words.path.lists(testdir.tmpdir))
    assert not loaded


def test_list_docu_restructured_page4(testdir, monkeypatch):
    """This test was designed cause on this page table content was
    parsed as lists."""
    source = power.link(power.DOCU27_PDF)
    tests.run(f'-i {source} --pages=4 --list', monkeypatch=monkeypatch)

    loaded = serializeraw.load_lists(words.path.lists(testdir.tmpdir))
    assert len(loaded) == 1
    area = utila.select_content(loaded, page=4)[0].area
    assert area == [5, 6, 7, 8]  # remove 8 after fixing parser
