# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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


@utilatest.longrun
def test_list_bachelor76_page4(testdir, monkeypatch):
    pages = (4,)
    source = power.link(power.BACHELOR076_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch)
    # 1 pages with list content
    assert len(lists) == 1


@utilatest.longrun
def test_list_bachelor76_page5_10(testdir, monkeypatch):
    pages = (5, 6, 7, 8, 9, 10)
    source = power.link(power.BACHELOR076_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch)
    # 1 pages with list content
    assert len(lists) == 1


@utilatest.longrun
def test_list_master72_page9_10(testdir, monkeypatch):
    pages = (9, 10)
    source = power.link(power.MASTER072_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch=monkeypatch)
    assert len(lists) == 1
    assert len(utila.select_page(lists, 9).content[0].data) == 7


@utilatest.longrun
def test_list_master72_page39_40_41(testdir, monkeypatch):
    pages = (39, 40, 41, 42)
    source = power.link(power.MASTER072_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch=monkeypatch)
    assert len(lists) == 1

    page39 = utila.select_page(lists, page=39).content
    assert len(page39) == 1
    first_list = page39[0]
    assert len(first_list) == 4


@pytest.mark.parametrize('pages', [
    pytest.param((36, 37, 38, 39, 40, 41, 42), id='with_offset'),
    pytest.param(utila.ranged_tuple(0, 42), id='no_offset'),
    pytest.param(':', id='all'),
])
def test_list_bachelor128_page36_42(pages, testdir, monkeypatch):
    """Use pages to ensure that extracting works when extraction uses
    more than one chunk."""
    source = power.link(power.BACHELOR128_PDF)
    extracted = extract_lists(source, pages, testdir, monkeypatch=monkeypatch)
    # assert len(extracted) == 1
    selected = utila.select_content(extracted, page=37)
    assert len(selected) == 1
    data = selected[0].data
    assert len(data) == 8
    area = selected[0].area

    expected = [
        (17, 18, 19, 20, 21),  # page 37
        utila.ranged_tuple(0, 30),  # page 38
        utila.ranged_tuple(0, 11),  # page 39
    ]
    assert area == expected


def validate_master99(extracted):
    # single list with six items on page 9
    page9 = utila.select_content(extracted, page=9)
    assert len(page9) == 1
    # TODO: ADD TEST FOR LAST ITEM WHICH IN TOO LONG YET
    assert len(page9[0]) == 6

    page46 = utila.select_content(extracted, page=46)
    assert len(page46) == 1
    assert len(page46[0]) == 9

    # regression check to avoid parsing table as list
    assert not utila.select_content(extracted, page=48)

    page49 = utila.select_content(extracted, page=49)
    assert len(page49) == 1
    assert len(page49[0]) == 3

    page79 = utila.select_content(extracted, page=79)
    # assert len(page79[0]) == 3 # TODO: Activate later
    assert len(page79[0]) == 2

    page80 = utila.select_content(extracted, page=80)
    # assert len(page80[0]) == 9 # TODO: Activate later
    assert len(page80[0]) == 3


@pytest.mark.parametrize('source, validator', [
    pytest.param(power.MASTER099_PDF, validate_master99, id='master99'),
])
def test_list_validate(source, validator, testdir, monkeypatch):
    source = power.link(source)
    # run extraction
    extracted = extract_lists(source, ':', testdir, monkeypatch=monkeypatch)
    # run validator
    validator(extracted)
