# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
import typing

import iamraw
import texmex
import utila


def parse_single(content: str):
    r"""\
    >>> parse_single('+ list item\n+ next item\n+\n') # skip last plus sign
    ['list item', 'next item']
    """
    for method in [
            parse_numbered_list,
            parse_quardo_list,
            parse_dotted_list,
            parse_plus_list,
            parse_minus_list,
    ]:
        extracted = method(content)
        if not extracted:
            continue
        return extracted
    return []


# TODO: Merge both pattern!
NUMBERED_LIST_PATTERN = r"""
    ^(?P<LEVEL>[0-9]+\.[0-9]{0})           # list level e.g. 1. 4. 5.
    \s                                     # whitespace
    (?P<TEXT>(?:.+\s){1,}?)               # list item content
    (?=[0-9]+\.\s?|$)                      # new list start or final newline
    """

# Double Newline must end this list item.
GENERAL = r"""
    ^\s*
    {selector}\s*
    (?P<TEXT>([^{selector}]+\n))      # list item content
"""


def parse_quardo_list(content: str) -> utila.Strings:
    return parse_general_list(content, '')


def parse_dotted_list(content: str) -> utila.Strings:
    return parse_general_list(content, ['•', '\x88'])


def parse_plus_list(content: str) -> utila.Strings:
    return parse_general_list(content, r'\+')


def parse_minus_list(content: str) -> utila.Strings:
    """Black token is required cause regex parser works with black
    listing list sign in list content."""
    # TODO: THINK ABOUT A BETTER PLAN
    black_token = '$$$$$$$$_$$$$$$$$'
    content = content.replace('-\n', black_token)
    parsed = parse_general_list(content, '-')
    parsed = [item.replace(black_token, '-\n') for item in parsed]
    return parsed


def parse_numbered_list(content: str) -> list:
    """Parse 1.2.3. list

    Returns:
        list with (text, level) of list items
        None if nothing no list is parsed
    """
    content = str(content)
    assert content
    # TODO: WORKAROUND: Single line does not parse without NEWLINE
    if not content.endswith(utila.NEWLINE):
        content += utila.NEWLINE

    parsed = re.finditer(
        NUMBERED_LIST_PATTERN,
        content,
        flags=re.MULTILINE | re.VERBOSE,
    )
    if not parsed:
        return []
    result = []
    for item in parsed:
        start, _ = item.span()
        if start > 0:
            before = content[start - 1]
            if before != utila.NEWLINE:
                # item is not located at the start of the text
                continue
        level, text = item[1], item[2]
        result.append((
            text.strip(),
            level,
        ))
    return result


def parse_general_list(content: str, selector: str) -> utila.Strings:
    r"""\
    >>> parse_general_list('\x88 Humus\n\x88 Bread', ['•', '\x88'])
    ['Humus', 'Bread']
    """
    assert isinstance(content, str), type(content)
    if isinstance(selector, list):
        # join multiple selector
        selector = '(' + '|'.join(selector) + ')'
    pattern = GENERAL.format(selector=selector)
    # Workaround: Adding newline to content. The regex does not work, if the
    # content ends with a newline. TODO: Improve regex
    content = content + utila.NEWLINE
    parsed = re.finditer(
        pattern,
        content,
        flags=re.MULTILINE | re.VERBOSE,
    )
    result = []
    for item in parsed:
        # TODO: IMPROVE REGEX
        text = item['TEXT'].split('\n\n')
        text = text[0]
        text = text.strip()
        if not text:
            # newlines where parsed as content. If we ignore newlines in
            # regex, it is not possible to parse multiple lists items.
            # Therefore we strip the result and check if result does
            # contain any content.
            continue
        result.append(text)
    return result


def extract_lists(  # pylint:disable=R0914
        page: texmex.PageTextNavigator,
        pagesize: iamraw.Border,  # pylint:disable=W0613
        uindex=None,
) -> typing.List[iamraw.PageList]:
    """Extract lists out of document page. There are different types of Lists.

    Numbered... 1.2.3, I. II. III., + + +, - - -, * * *.
    """
    # TODO: MAX_Y_MERGE IS VERY INSTABLE
    # assert hey.textnavigator.is_navigator(page), type(page)

    page, merged = texmex.merge_content(
        page,
        max_y_merge=15,  # TODO: HOLY VALUE
        uindex=uindex,
    )
    text_bounds = texmex.merge_content_join(page)

    result = []
    enumerated = enumerate(zip(text_bounds, merged))
    for paraindex, (paragraph, mergearea) in enumerated:  # pylint:disable=W0612
        bounds, text = paragraph.bounds, paragraph.text  # pylint:disable=W0612
        # ptextsize = fontsize_from_textbounds(bounds)
        # if ptextsize != textsize:
        #     # TODO: Hier gibt es noch ein Problem mit der Berechnung der
        #     # Schriftgroesse, da der Zeilenabstand nicht beruecksichtigt wird
        #     # Collect lists only in text, avoid collecting in headlines
        #     continue
        # TODO: FIX FEED
        # feed = paragraph.bounds.xdist
        # if feed <= 0.0:
        #     # TODO: Improve this
        #     # no text feed
        #     continue
        detected = []
        for parser in [
                parse_dotted_list,
                parse_quardo_list,
                parse_minus_list,
                parse_numbered_list,
                parse_plus_list,
        ]:
            detected = parser(text)
            # TODO: parse all and compare
            if detected:
                break
        # parsing was not succesfull
        if not detected:
            continue
        pagelist = iamraw.PageList(area=mergearea)
        # before, after = before_and_after(text, position[0], position[1])
        for index, item in enumerate(detected):
            # remove newline
            if isinstance(item, str):
                pagelist.append(item, index)
            else:
                content, level = item
                pagelist.append(content, level)
        if pagelist:
            result.append(pagelist)
    return result
