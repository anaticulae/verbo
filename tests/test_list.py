# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw
import utila

import tests.fixtures.restruct
import tests.resources
import words.lists.regex
import words.lists.vertical
import words.path

NUMBERED_LIST_SAMPLE_SIZE = 9
NUMBERED_LIST = """
6. Use caniusepython3 to find out which of your dependencies are blocking your use of Python 3 (pip
install caniusepython3)

To make your project be single-source Python 2/3 compatible, the basic steps are:

1. Only worry about supporting Python 2.7
2. Make sure you have good test coverage (coverage.py can help; pip install coverage)
3. Learn the differences between Python 2 & 3
4. Use Futurize (or Modernize) to update your code (e.g. pip install future)
5. Use Pylint to help make sure you don’t regress on your Python 3 support (pip install pylint)
6. Use caniusepython3 to find out which of your dependencies are blocking your use of Python 3 (pip
install caniusepython3)

7. Once your dependencies are no longer blocking you, use continuous integration to make sure you stay
compatible with Python 2 & 3 (tox can help test against multiple versions of Python; pip install
tox)

8. Consider using optional static type checking to make sure your type usage works in both Python 2 &
3 (e.g. use mypy to check your typing under both Python 2 & Python 3).

Text
"""


def test_list_numbered_regex():
    parsed = words.lists.regex.parse_numbered_list(NUMBERED_LIST)

    assert len(parsed) == NUMBERED_LIST_SAMPLE_SIZE, parsed

    # Final example is very important!
    last_content, last_title = parsed[-1]
    assert last_title == '8.'
    assert last_content == (
        "Consider using optional static type checking to"
        " make sure your type usage works in both Python 2 &\n3 (e.g. use mypy "
        "to check your typing under both Python 2 & Python 3).")


def test_list_numbered_regex_single_item():
    raw = (
        "8. Consider using optional static type checking to make sure your "
        "type usage works in both Python 2 &\n3 (e.g. use mypy to check your "
        "typing under both Python 2 & Python 3).")

    parsed = words.lists.regex.parse_numbered_list(raw)
    assert len(parsed) == 1
    level = parsed[0][1]
    assert level == "8."


DOTTED_LIST = """
Basics
Improving upon the pattern established at:
• Code: Block
• Code: Inline
• Emphasis: Italics
• Emphasis: Strong
• Headers
• Horizontal rules
  more than one line
  futher more lines
• Images: Inline
• Line Return
• Links: Inline
• Links: Inline with title
• Links: Reference
• Lists: Simple
• Lists: Nested
• Paragraphs
• Images: Reference
Futher text
"""

DOTTED_LIST_EXPECTED = [
    'Code: Block',
    'Code: Inline',
    'Emphasis: Italics',
    'Emphasis: Strong',
    'Headers',
    'Horizontal rules\n  more than one line\n  futher more lines',
    'Images: Inline',
    'Line Return',
    'Links: Inline',
    'Links: Inline with title',
    'Links: Reference',
    'Lists: Simple',
    'Lists: Nested',
    'Paragraphs',
    'Images: Reference',
]


@pytest.mark.xfail(reason='broken regex')
def test_list_dotted():
    parsed = words.lists.regex.parse_dotted_list(DOTTED_LIST)
    assert parsed == DOTTED_LIST_EXPECTED


DOTTED_EXAMPLE = """
For this project, we’ll have the following pages:
  • Index Page
    • Support
      • Installation
  • Cookbook/Examples
• Command Line Options
• Changelog
Let’s start with the Support page.
"""

DOTTED_EXAMPLE_EXPECTED = [
    'Index Page',
    'Support',
    'Installation',
    'Cookbook/Examples',
    'Command Line Options',
    'Changelog',
]


@pytest.mark.xfail(reason='broken regex')
def test_list_dotted_with_start_and_end():
    parsed = words.lists.regex.parse_dotted_list(DOTTED_EXAMPLE)
    assert parsed == DOTTED_EXAMPLE_EXPECTED


DOTTED_EXAMPLE_CONTENT_ONLY = """ • Index Page
    • Support
• Changelog"""


@pytest.mark.xfail(reason='broken regex')
def test_list_dotted_with_content_only():
    parsed = words.lists.regex.parse_dotted_list(DOTTED_EXAMPLE_CONTENT_ONLY)
    assert parsed == ['Index Page', 'Support', 'Changelog']


def test_list_work():  # pylint:disable=W0621
    extracted = tests.fixtures.restruct.restructured_list_work()
    dumped_list = serializeraw.dump_lists(extracted)
    assert len(dumped_list) > 400, str(dumped_list)

    result = serializeraw.load_lists(dumped_list)
    assert len(result) == 3, str(result)

    first_items = [item for (_, item) in result[0][1][0][2].data]
    second_items = [item for (_, item) in result[1][1][0][2].data]
    last_items = [item for (_, item) in result[2][1][0][2].data]

    assert len(first_items) == 15, str(first_items)
    assert first_items == [
        'Code: Block', 'Code: Inline', 'Emphasis: Italics', 'Emphasis: Strong',
        'Headers', 'Horizontal rules', 'Images: Inline', 'Line Return',
        'Links: Inline', 'Links: Inline with title', 'Links: Reference',
        'Lists: Simple', 'Lists: Nested', 'Paragraphs', 'Images: Reference'
    ]
    assert len(second_items) == 6, str(second_items)
    assert second_items == [
        'Index Page', 'Support', 'Installation', 'Cookbook/Examples',
        'Command Line Options', 'Changelog'
    ]
    assert len(last_items) == 3, str(last_items)
    assert last_items == ['genindex', 'modindex', 'search']


def test_list_dump_and_load_lists():  # pylint:disable=W0621
    result = tests.fixtures.restruct.restructured_list_work()
    dumped_list = serializeraw.dump_lists(result)
    loaded = serializeraw.load_lists(dumped_list)
    assert loaded == result


def extract_lists(source, pages: tuple, testdir, monkeypatch):
    # TODO: REPLACE WITH UTILA
    pages = ','.join([str(item) for item in pages])
    # run words
    tests.run(
        # TODO: replace with --list*
        f'-i {source} --headlines  --text --list --pages {pages}',
        monkeypatch=monkeypatch,
    )
    path = words.path.lists(testdir.tmpdir)
    lists = serializeraw.load_lists(path)
    return lists


def test_list_bachelor76_page4_5(testdir, monkeypatch):
    pages = (4, 5, 6, 7, 8)
    source = tests.resources.BACHELOR76

    lists = extract_lists(source, pages, testdir, monkeypatch)

    flat = utila.flatten([item[1] for item in lists])
    lists = [item[2] for item in flat]
    assert len(lists) == 2

    # TODO: EXTEND DOTTED PARSER TO SUPPORT MULTILINES


def test_list_master72_page9_10(testdir, monkeypatch):
    pages = (9, 10)
    source = tests.resources.MASTER72

    lists = extract_lists(source, pages, testdir, monkeypatch=monkeypatch)
    assert len(lists) == 1

    first = lists[0][1][0][2]
    assert len(first) == 7


def test_list_master72_page39_one_list(testdir):
    pages = (39,)
    source = tests.resources.MASTER72

    ptcn = serializeraw.create_pagetextcontentnavigators_frompath(
        source,
        pages=pages,
    )

    listinstance = words.lists.vertical.analyze_page(ptcn[0])
    assert len(listinstance) == 1
    assert len(listinstance[0]) == 2
