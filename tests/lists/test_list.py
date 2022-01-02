# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utilatest

import tests
import words.lists.runtime
import words.lists.strategies.bestpage
import words.lists.strategies.regex
import words.lists.strategies.vertical

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


def test_list_numbered_regex_last_item():
    parsed = words.lists.strategies.regex.parse_numbered_list(NUMBERED_LIST)
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
    parsed = words.lists.strategies.regex.parse_numbered_list(raw)
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
    'Horizontal rules\nmore than one line\nfuther more lines',
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


def test_list_dotted_simple():
    parsed = words.lists.strategies.regex.parse_dotted_list(DOTTED_LIST)
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
    parsed = words.lists.strategies.regex.parse_dotted_list(DOTTED_EXAMPLE)
    assert parsed == DOTTED_EXAMPLE_EXPECTED


DOTTED_EXAMPLE_CONTENT_ONLY = """ • Index Page
    • Support
• Changelog"""


def test_list_dotted_with_content_only():
    parsed = words.lists.strategies.regex.parse_dotted_list(
        DOTTED_EXAMPLE_CONTENT_ONLY)
    assert parsed == ['Index Page', 'Support', 'Changelog']


@utilatest.longrun
def test_list_master72page39_one_list(testdir):
    pages = (39,)
    source = power.link(power.MASTER072_PDF)
    ptcn = serializeraw.ptcn_frompath(
        source,
        pages=pages,
    )
    listinstance = words.lists.strategies.vertical.analyze_page(ptcn[0], [])
    assert len(listinstance) == 1
    assert len(listinstance[0]) == 2


OVERLAPPING = [
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
             )),
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
             )),
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
             )),
        ], 13
    ],
]


def test_merge_overlapping_lists():
    merged = words.lists.strategies.bestpage.merge_overlapping_lists(
        OVERLAPPING)
    assert len(merged) == 2
    assert len(merged[0][1]) == 1
    assert len(merged[1][1]) == 2


TWO_PAGES = [
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
                  12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
              ],
          ))],
        28,
    ],
    [
        10,
        [(0, 0,
          iamraw.PageList(
              data=[(None, 'Virtual  Social  Worlds  ('),
                    (None, 'Chats und Diskussionsforen')],
              area=[0, 1, 2, 3, 4],
          ))],
        27,
    ],
]


def test_merge_overlapping_lists_two_pages():
    merged = words.lists.strategies.bestpage.merge_overlapping_lists(TWO_PAGES)
    single = merged[0][1][0][2]
    marker = [item[0] for item in single]
    # ensure that list separator is None
    assert not any(marker), str(marker)


def test_list_area_tuple_master110pages67(testdir, monkeypatch):
    """Ensure that area-attribute is splitted by list content.

    Example: 0l_0, 0l_0; 0l_1; 0l_2
    """
    source = power.link(power.MASTER110_PDF)
    cmd = f'--list --page=67 -i {source} -o {testdir.tmpdir}'
    tests.run(cmd, monkeypatch=monkeypatch)
    lists = serializeraw.load_lists(testdir.tmpdir, pages=67)[0].content[0]
    expected = [2, 1, 2, 1, 1, 2]
    area_length = lists.area_length
    assert area_length == expected
