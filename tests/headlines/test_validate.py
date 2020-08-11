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

BACHELOR90_HEADLINES = """\
1. Einleitung
    1.1. Motivation
    1.2. Zielsetzung und Aufbau der Arbeit
2. Grundlagen eingebetteter Systeme
    2.1. Embedded System
        2.1.1. Systembegriff
        2.1.2. Computersysteme
        2.1.3. Entwicklungen im Embedded-Bereich
    2.2. Standards in der eingebetteten Softwareentwicklung
        2.2.1. AUTOSAR
        2.2.2. MISRA-C
    2.3. Controller Area Network - CAN
        2.3.1. Topologie
        2.3.2. Datenübertragung
            Abitrierungsphase
            Bitstromkompressor
            CAN-Nachricht
3. Methodik
    3.1. Modellgetriebene Softwareentwicklung
        3.1.1. Entwicklungswerkzeuge
        3.1.2. Stand der Technik im Automobilbereich
    3.2. Automatische Codegenerierung aus Modellen
        3.2.1. Konzept
            Geschützte Bereiche
            Generierung für eine abstrakte Schnittstelle
            Parametrisierte Codegenerierung
        3.2.2. Probleme beim Erzeugen von Quellcode
        3.2.3. Validierung der Ergebnisse
    3.3. Strategien zur Zerlegung der Probleme
        3.3.1. Randbedingungen
        3.3.2. Modularisierung
        3.3.3. Information Hiding
        3.3.4. Kopplung
    3.4. Umsetzung des Softwaresystems
        3.4.1. Manuell erzeugter Quellcode
        3.4.2. Modulweise Automatisierung, manuelle Verknüpfung
        3.4.3. Vollständige Automatisierung
        3.4.4. Zusammenfassung der Umsetzung
    3.5. Simulink
        3.5.1. Embedded Coder
        3.5.2. Verwendung von S-Funktionen
        3.5.3. Erzeugen des Simulinkmodells
            Konfiguration des Simulinkmodells
            Anpassen der Simulation
            Kommunikation durch Ports
    3.6. Testen der Software
        3.6.1. Softwarespezifikation
        3.6.2. Grundprinzip der Prüfung
        3.6.3. Klassifikation der Tests nach Komplexität
        3.6.4. Testen eingebetteter Systeme
            Model in the loop
            Software in the loop
            Hardware in the loop
        3.6.5. Bewertung des Testens als Prüfverfahren
    3.7. Debugging der Software
    3.8. Eignung für die Umsetzung
4. Umsetzung
    4.1. Problemstellung
    4.2. Vorgehen um Code zu erzeugen
    4.3. Übersicht der praktischen Entwicklung
        4.3.1. Entwicklungsumgebung Ubuntu
            Programm anlegen3
            Programm verwalten
        4.3.2. Arbeit auf der OBU
    4.4. Allgemeiner Aufbau der Algorithmen
    4.5. Umsetzung der Algorithmen
        4.5.1. Algorithmus zur Durchmesserberechnung
        4.5.2. Moduldefinition
            Einlesen
            Buffer
            Durchmesser
            Statistische Auswertung
    4.6. Komponententest
        4.6.1. Testen der Komponente Einlesen
            Lesen vom Speicher
            Deserialisierung der Nachrichten
        4.6.2. Testen des Buffers
        4.6.3. Testen der Durchmesserberechnung
        4.6.4. Verifikation des Histogramms
    4.7. Integration und Integrationstest der entwickelten Komponenten
        4.7.1. Manuelle Integration
        4.7.2. Vollständige Integration in Simulink
            Integrationstest Einlesen
            Manueller Einzeltest der Gesamtintegration
            Test der Gesamtintegration mit Histogramm
            Ergebnis der Integration
        4.7.3. Bewertung
5. Diskussion und Ausblick
            Simulink-Modell
            Putty
            SSH
            Player - Ubuntu
Literaturverzeichnis"""


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.MASTER098_PDF, MASTER98_HEADLINES, id='master98'),
    pytest.param(power.BACHELOR090_PDF, BACHELOR90_HEADLINES, id='bachelor90'),
])
def test_headlines_validate(source, expected, testdir, monkeypatch):
    source = power.link(source)
    tests.run(f'-i {source} --headlines', monkeypatch=monkeypatch)

    headlines = words.path.headlines(testdir.tmpdir)
    parsed = serializeraw.load_headlines(headlines)

    raw = raw_headlines(parsed)
    assert raw == expected


def raw_headlines(parsed) -> str:
    collected = []
    for chapter in parsed:
        if chapter:
            collected.append(chapter[0].text)
        else:
            collected.append('None')
        for headline in chapter[1:]:
            collected.append('    ' + headline.text)
    return utila.NEWLINE.join(collected)
