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

import tests
import words.path

MASTER98_HEADLINES = """\
1  Einleitung
2  Theoretische Grundlagen
2.1  Von der mémoire collective zu den Lieux de mémoire
2.2  Binationale Erinnerungsorte
2.3  Das dialogische Erinnern von Aleida Assmann
2.4  Erinnerungsorte im DaF-Landeskundeunterricht
3  Der Elysée-Vertrag – Ein deutsch-französischer Erinnerungsort
3.1  Die Vorgeschichte
3.2  Adenauer, de Gaulle und der Elysée-Vertrag
3.3  Mythos Elysée-Vertrag
3.4  Die Entwicklung des Elysée-Vertrags vom Ereignis zum Erinnerungsort
4  Didaktisierung
4.1  Eignung des Elysée-Vertrags für den DaF-Landeskundeunterricht
4.2  Zielgruppe und Sprachniveau
4.3  Zielsetzungen
4.4  Vorstellung der Materialien
5  Reflexion
5.1  Reflexion der Themenwahl
5.2  Reflexion der Zielgruppe
5.3  Reflexion der inhaltlichen Lernziele
5.5  Reflexion der Methodik und des Materials
5.6  Reflexion der kulturdidaktischen Lernziele
6  Fazit und Ausblick
7  Verzeichnisse
7.1  Literaturverzeichnis
7.2  Tabellenverzeichnis
8  Anhang"""


@pytest.mark.parametrize('source, expected', [
    pytest.param(
        power.MASTER098_PDF,
        MASTER98_HEADLINES,
        id='master98',
        marks=pytest.mark.xfail(reason='adjust headline extractor')),
])
def test_headlines_validate(source, expected, testdir, monkeypatch):
    source = power.link(power.MASTER098_PDF)
    tests.run(f'-i {source} --headlines', monkeypatch=monkeypatch)

    headlines = words.path.headlines(testdir.tmpdir)
    parsed = serializeraw.load_headlines(headlines)

    raw = raw_headlines(parsed)
    assert raw == expected


def raw_headlines(parsed) -> str:
    collected = []
    for chapter in parsed:
        for headline in chapter:
            collected.append(headline.text)
    return utila.NEWLINE.join(collected)
