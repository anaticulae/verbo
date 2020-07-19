# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utila

import tests.fixtures.restruct
import words.lists.regex
import words.lists.strategy
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


def test_list_dotted_with_start_and_end():
    parsed = words.lists.regex.parse_dotted_list(DOTTED_EXAMPLE)
    assert parsed == DOTTED_EXAMPLE_EXPECTED


DOTTED_EXAMPLE_CONTENT_ONLY = """ • Index Page
    • Support
• Changelog"""


def test_list_dotted_with_content_only():
    parsed = words.lists.regex.parse_dotted_list(DOTTED_EXAMPLE_CONTENT_ONLY)
    assert parsed == ['Index Page', 'Support', 'Changelog']


def test_list_work():  # pylint:disable=W0621
    extracted = tests.fixtures.restruct.restructured_list_work()
    dumped_list = serializeraw.dump_lists(extracted)
    assert len(dumped_list) > 400, str(dumped_list)

    result = serializeraw.load_lists(dumped_list)
    assert len(result) == 3, str(result)

    first_items = [
        item[1] for item in utila.select_page(result, 8).content[0].data
    ]
    second_items = [
        item[1] for item in utila.select_page(result, 14).content[0].data
    ]
    last_items = [
        item[1] for item in utila.select_page(result, 24).content[0].data
    ]

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
    pages = utila.from_tuple(pages, separator=',')
    # run words
    tests.run(
        # TODO: replace with --list*
        f'-i {source} --headlines  --text --list --pages {pages}',
        monkeypatch=monkeypatch,
    )
    path = words.path.lists(testdir.tmpdir)
    lists = serializeraw.load_lists(path)
    return lists


def test_list_bachelor76_page4(testdir, monkeypatch):
    pages = (4,)
    source = power.link(power.BACHELOR076_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch)
    # 1 pages with list content
    assert len(lists) == 1


def test_list_bachelor76_page5_10(testdir, monkeypatch):
    pages = (5, 6, 7, 8, 9, 10)
    source = power.link(power.BACHELOR076_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch)
    # 1 pages with list content
    assert len(lists) == 1


def test_list_master72_page9_10(testdir, monkeypatch):
    pages = (9, 10)
    source = power.link(power.MASTER072_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch=monkeypatch)
    assert len(lists) == 1
    assert len(utila.select_page(lists, 9).content[0].data) == 7


def test_list_master72_page39_one_list(testdir):
    pages = (39,)
    source = power.link(power.MASTER072_PDF)

    ptcn = serializeraw.create_pagetextcontentnavigators_frompath(
        source,
        pages=pages,
    )

    listinstance = words.lists.vertical.analyze_page(ptcn[0])
    assert len(listinstance) == 1
    assert len(listinstance[0]) == 2


def test_list_master72_page39_40_41(testdir, monkeypatch):
    pages = (39, 40, 41, 42)
    source = power.link(power.MASTER072_PDF)

    lists = extract_lists(source, pages, testdir, monkeypatch=monkeypatch)
    assert len(lists) == 1

    page39 = utila.select_page(lists, page=39).content
    assert len(page39) == 1
    first_list = page39[0]
    assert len(first_list) == 4


def test_merge_overlapping_lists():
    pages = [
        [
            36,
            [
                (0, 0,
                 iamraw.PageList(
                     data=[
                         ('1.', 'A'),
                         ('-', 'AA'),
                         ('-', 'AAA'),
                         ('2.', 'B'),
                         ('-', 'BB'),
                         ('3.', 'C'),
                         ('-', 'CC'),
                         ('-', 'CCC'),
                     ],
                     area=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                     paragraph=None,
                     merged=None)),
            ], 17
        ],
        [
            41,
            [
                (0, 0,
                 iamraw.PageList(
                     data=[
                         ('-', 'A'),
                         ('-', 'B'),
                         ('-', 'C'),
                     ],
                     area=[2, 3, 4],
                     paragraph=None,
                     merged=None)),
                (0, 0,
                 iamraw.PageList(
                     data=[
                         ('+', 'www.Freebus.org'),
                         ('+', 'www.eib-home.de'),
                         ('+', 'www.knx.de'),
                         ('+', 'First'),
                         ('+', 'Second'),
                         ('+', 'Third'),
                         ('+', 'Fourth'),
                     ],
                     area=[6, 7, 8, 9, 10, 11, 12],
                     paragraph=None,
                     merged=None)),
            ], 13
        ],
    ]
    merged = words.lists.strategy.merge_overlapping_lists(pages)
    assert len(merged) == 2
    assert len(merged[0][1]) == 1
    assert len(merged[1][1]) == 2


def test_merge_overlapping_lists_two_pages():
    pages = [
        [
            9,
            [(0, 0,
              iamraw.PageList(
                  data=[(None, 'Blogs  gelten  als  die  fr▒heste  '),
                        (None, 'Wikis  sind  Gemeinschaftsproduktio'),
                        (None, 'Social  Network  Sites  widmen  sic'),
                        (None, 'Microblogs  erm▒glichen  das  Versc'),
                        (None, 'Social-Sharing-Plattformen  bzw.  C')],
                  area=[
                      12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                      26, 27
                  ],
                  paragraph=None,
                  merged=None))],
            28,
        ],
        [
            10,
            [(0, 0,
              iamraw.PageList(
                  data=[(None, 'Virtual  Social  Worlds  ('),
                        (None, 'Chats und Diskussionsforen')],
                  area=[0, 1, 2, 3, 4],
                  paragraph=None,
                  merged=None))],
            27,
        ],
    ]
    merged = words.lists.strategy.merge_overlapping_lists(pages)
    single = merged[0][1][0][2]

    print(single)
    marker = [item[0] for item in single]
    # ensure that list separator is None
    assert not any(marker), str(marker)
