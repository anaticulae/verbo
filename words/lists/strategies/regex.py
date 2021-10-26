# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
import typing

import configo
import iamraw
import texmex
import utila


def parse_single(content: str):
    r"""\
    # last plus sign is an empty entree
    >>> parse_single('+ list item\n+ next item\n+\n')
    ['list item', 'next item', '']
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

# ''
QUARDO = chr(61607)


def parse_quardo_list(content: str) -> utila.Strings:
    return parse_general_list(content, QUARDO)


# 61623: dot
DOTTED = {'•', '\x88', '\x99', chr(61623)}


def parse_dotted_list(content: str) -> utila.Strings:
    # TODO: ADD SPECIAL CHAR CONVERTER TO RAWMAKER
    return parse_general_list(content, DOTTED)


PLUS = '+'


def parse_plus_list(content: str) -> utila.Strings:
    return parse_general_list(content, PLUS)


def parse_minus_list(content: str) -> utila.Strings:
    r"""Hidden token is required that regex parser works with hidden
    listing list sign in list content.

    >>> parse_minus_list(('- Bezugsbetreuung im Wohn- und Lebensumfeld\n'
    ... '- bei Wohnungslosigkeit Möglichkeit Trägerbestand\n\n'))
    ['Bezugsbetreuung im Wohn- und Lebensumfeld', 'bei Wohnungslosigkeit Möglichkeit Trägerbestand']
    """
    # TODO: THINK ABOUT A BETTER PLAN
    # HACK Y
    # wrap token inside hidden pattern
    hidden_token = [
        (r'-\n', '-\n', '$_$_$_$_$_$_$_$_$_$_$'),
        (r'\b\-', '-', '$*$*$*$*$*$*$*$*$'),
    ]
    for pattern, _, hidden in hidden_token:
        content = re.sub(pattern, hidden, content)

    parsed = parse_general_list(content, '-')

    for index, item in enumerate(parsed):
        # remove hidden token
        for _, origin, hidden in hidden_token:
            item = item.replace(hidden, origin)
        parsed[index] = item
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
    >>> parse_general_list('- no well detected + wuhu', selector='*')
    []
    """
    assert isinstance(content, str), type(content)
    data = [item.strip() for item in content.splitlines()]
    starts = [
        index for index, item in enumerate(data) if item and item[0] in selector
    ]
    if not starts:
        # could not detect any list
        return []
    result = [
        '\n'.join(data[current:after])
        for current, after in zip(starts[:-1], starts[1:])
    ]
    # find first empty item to merge last item
    end = [
        index for index, item in enumerate(data, start=starts[-1]) if not item
    ]
    if end:
        end = end[0]
    else:
        # last item is a content item
        end = starts[-1]
    result.append('\n'.join(data[starts[-1]:end + 1]))
    # strip selector
    result = [item[1:].strip() for item in result]
    return result


LISTS_MERGE_Y_MAX = configo.HV_FLOAT_PLUS(default=15.0)


def extract_lists(  # pylint:disable=R0914
    page: texmex.PageTextNavigator,
    pagesize: iamraw.Border,  # pylint:disable=W0613
    uindex=None,
) -> typing.List[iamraw.PageList]:
    """Extract lists out of document page. There are different types of Lists.

    Numbered... 1.2.3, I. II. III., + + +, - - -, * * *.
    """
    # TODO: MAX_Y_MERGE IS VERY INSTABLE

    page, merged = texmex.merge_content(
        page,
        max_y_merge=LISTS_MERGE_Y_MAX,
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
