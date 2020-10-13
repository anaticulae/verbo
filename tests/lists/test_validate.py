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
import utilatest

import tests
import words.path


def extract_lists(source, pages: tuple, testdir, monkeypatch):
    pages = utila.from_tuple(pages, separator=',')
    # run words
    tests.run(
        # TODO: replace with --list*
        f'-i {source} --list --pages {pages}',
        monkeypatch=monkeypatch,
    )
    path = words.path.lists(testdir.tmpdir)
    lists = serializeraw.load_lists(path)
    return lists


@utilatest.skip_longrun
def test_list_bachelor76_page4(testdir, monkeypatch):
    pages = (4,)
    source = power.link(power.BACHELOR076_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch)
    # 1 pages with list content
    assert len(lists) == 1


@utilatest.skip_longrun
def test_list_bachelor76_page5_10(testdir, monkeypatch):
    pages = (5, 6, 7, 8, 9, 10)
    source = power.link(power.BACHELOR076_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch)
    # 1 pages with list content
    assert len(lists) == 1


@utilatest.skip_longrun
def test_list_master72_page9_10(testdir, monkeypatch):
    pages = (9, 10)
    source = power.link(power.MASTER072_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch=monkeypatch)
    assert len(lists) == 1
    assert len(utila.select_page(lists, 9).content[0].data) == 7


@utilatest.skip_longrun
def test_list_master72_page39_40_41(testdir, monkeypatch):
    pages = (39, 40, 41, 42)
    source = power.link(power.MASTER072_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch=monkeypatch)
    assert len(lists) == 1

    page39 = utila.select_page(lists, page=39).content
    assert len(page39) == 1
    first_list = page39[0]
    assert len(first_list) == 4
