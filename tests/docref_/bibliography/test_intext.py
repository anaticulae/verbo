# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import docref.bibliography.strategies.intext

RAW = """\
(Halbwachs 1985:71)
(ebd .:20)
(Nora 1990:12-13)
(Hahn ; Traba 2015:13)
(Koreik 2010:1482)
(Seydoux de Clausonne 1968:20)
(vgl. Darilek 2014)
"""

TODO = """\
(vgl. Defrance ; Pfeil 2014 ; vgl. Frank 2005)
"""


def test_parse_label():
    parsed = docref.bibliography.strategies.intext.parse(RAW)
    expected = len(RAW.splitlines())
    assert len(parsed) == expected


@pytest.mark.xfail(reason='improve collector')
def test_parse_not_working_yet():
    parsed = docref.bibliography.strategies.intext.parse(TODO)
    expected = len(TODO.splitlines())
    assert len(parsed) == expected
