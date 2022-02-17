# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import words.lists.regex

CONTENT = """\
Betreute Einzelwohnen nach $ 53/54 SGB XII beinhaltet folgende Leistungen.
- Bezugsbetreuung im Wohn- und Lebensumfeld
- bei Wohnungslosigkeit Möglichkeit der Aufnahme in eine Wohnung aus dem Trägerbestand
- bedarfsorientierte Hilfe bei der Lebens- und Krankheitsbewältigung
- Krisenbegleitung
- spezielle Berücksichtigung von Suchtproblemen (u.a. Rückfallprävention,
Konsumkontrollprogramme)
- Kooperation mit anderen Hilfeträgern

Alle  Mitarbeiter sind festangestellte Diplom-Sozialarbeiter, Diplom-Pädagogen oder Diplom-
Psychologen.  Zusätzlich  verfügen  einige  Mitarbeiter  über  sozialpsychiatrische  oder
"""


def test_list_parse_regex():
    parsed = words.lists.regex.parse_single(CONTENT)
    assert len(parsed) == 6


RAW = """\
+ Die  Konsumenten  haben  ein  Budget  von  400  Talern  je  Runde.  Wenn
Brote  und  Fische  gleich  teuer  sind  pro  Stück,  ist  es  optimal  für  die
Konsumenten  gleich  viele  Brote  und  Fische  zu  kaufen.  Taler,  die  die
Konsumenten  in  einer  Runde  nicht  verbrauchen,  können  die
Konsumenten  zurückgeben.  Alle  Konsumenten  erhalten  dieselben
Experimentvorgaben.
"""


def test_list_parse_regex_regression():
    parsed = words.lists.regex.parse_single(RAW)
    assert len(parsed) == 1
    end = parsed[0]
    assert end.endswith('Experimentvorgaben.')
