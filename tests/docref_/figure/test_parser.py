# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import docref.figure

SENTENCE = """\
Verkehrsanbindung der Stadt Neunkirchen An der schon immer wichtigen
Handelsroute von Wien über den Semmering via Graz nach Triest gelegen
wurde die Stadt von je her von Handel und Verkehr geprägt (siehe Abb.
1).
"""


def test_figure_parser():
    detected = docref.figure.parse_sentence(SENTENCE)
    assert len(detected) == 1
    expected = [(31, 36)]
    assert detected == expected
