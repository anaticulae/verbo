# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import utila


def parse_single(content: str):
    r"""\
    last plus sign is an empty entree
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


# ''
QUARDO = chr(61607)
PLUS = '+'
MINUS = '-'
# 61623: dot
DOTTED = {'•', '\x88', '\x99', chr(61623)}
NUMBER = utila.compiles(r'^[0-9]{1,2}\.(?!\d)')


def parse_quardo_list(content: str) -> utila.Strings:
    return parse_general_list(content, QUARDO)


def parse_dotted_list(content: str) -> utila.Strings:
    return parse_general_list(content, DOTTED)


def parse_plus_list(content: str) -> utila.Strings:
    return parse_general_list(content, PLUS)


def parse_minus_list(content: str) -> utila.Strings:
    r"""\
    >>> parse_minus_list(('- Bezugsbetreuung im Wohn- und Lebensumfeld\n'
    ... '- bei Wohnungslosigkeit Möglichkeit Trägerbestand\n\n'))
    ['Bezugsbetreuung im Wohn- und Lebensumfeld', 'bei Wohnungslosigkeit Möglichkeit Trägerbestand']
    """
    return parse_general_list(content, MINUS)


def parse_numbered_list(content: str) -> list:
    """Parse 1.2.3. list

    Returns:
        list with (text, level) of list items
        None if nothing no list is parsed
    """
    return parse_general_list(content, NUMBER, selector_skip=False)


def parse_general_list(
    content: str,
    selector: str,
    selector_skip: bool = True,
) -> utila.Strings:
    r"""\
    >>> parse_general_list('\x88 Humus\n\x88 Bread', ['•', '\x88'])
    ['Humus', 'Bread']
    >>> parse_general_list('- no well detected + wuhu', selector='*')
    []
    """
    if not isinstance(selector, re.Pattern):
        selector = utila.compiles(f'^{regex_prepare(selector)}')
    assert isinstance(content, str), type(content)
    data = [item.strip() for item in content.splitlines()]
    starts = [index for index, item in enumerate(data) if selector.match(item)]
    if not starts:
        # could not detect any list
        return []
    result = [
        '\n'.join(data[current:after])
        for current, after in zip(starts[:-1], starts[1:])
    ]
    # find first empty item to merge last item
    end = [
        index for index, item in enumerate(data[starts[-1]:], start=starts[-1])
        if not item
    ]
    if end:
        end = end[0]
    elif len(starts) == 1:
        # only one startpoint and no ending, therefore collect from start
        # till end of content.
        end = len(data)
    else:
        # last item is a content item
        end = starts[-1]
    result.append('\n'.join(data[starts[-1]:end + 1]))
    # strip selector
    if selector_skip:
        result = [selector.sub('', item).strip() for item in result]
    else:
        result = [(selector.sub('', item).strip(), (selector.match(item)[0]))
                  for item in result]
    return result


def regex_prepare(items):
    if isinstance(items, str):
        items = re.escape(items)
    if utila.iterable(items):
        items = [re.escape(item) for item in items]
        items = f"({'|'.join(items)})"
    return items
