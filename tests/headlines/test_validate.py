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
import utilatest

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

DISS264_HEADLINES = """\
1 Einleitung
    1.1 Problembeschreibung
    1.2 Entwicklungs- und Handlungsansätze aus BMBF geförderten Projekten
    1.3 Zielsetzung und Kernfragen
    1.4 Aufbau der Arbeit
2 Demographischer Wandel in der Arbeitswelt
    2.1 Geschichtlicher Hintergrund der Demographie
    2.2 Begriffliche Grundlagen
        2.2.1 Demographie
        2.2.2 Alter und seine Abgrenzungskriterien
        2.2.3 Betriebliche Personalpolitik
        2.2.4 Arbeitsmarktpolitik
    2.3 Hauptelemente der demographischen Entwicklung
        2.3.1 Lebenserwartung
        2.3.2 Geburtenentwicklung
        2.3.3 Migration
        2.3.4 Entwicklung der Bevölkerungszahlen innerhalb der Bundesrepublik Deutschland und Zusammensetzung der Altersstruktur
            2.3.4.1 Bevölkerungsentwicklung insgesamt
            2.3.4.2 Bevölkerung im erwerbsfähigen Alter
            2.3.4.3 Altenquotient als Indikator der Alterung
    2.4 Theoretische Erklärungsansätze
        2.4.1 Psychologische Erklärungsansätze
        2.4.2 Erklärungsansätze aus der Arbeitsmarkttheorie
        2.4.3 Industriesoziologische Erklärungsansätze
        2.4.4 Erklärungsansätze aus der „Sozialpolitikwissenschaft“
    2.5 Auswirkungen des demographischen Wandels auf die Arbeitswelt und die gesetzliche Rentenversicherung
        2.5.1 Erwerbsbeteiligung und Arbeitslosigkeit älterer Arbeitnehmer
        2.5.2 Entwicklung der Renten nach Rentenarten
    2.6 Zusammenfassung und Schlussfolgerung
3 Gesetzliche Rahmenbedingungen und arbeitsmarktpolitische Maßnahmen
    3.1 Konsequenzen der demographischen Entwicklung für die gesetzliche Rentenversicherung
            Anhebung des Rentenzugangsalters
            Beitragserhöhung oder Rentenniveausenkung
    3.2 Veränderte rechtliche Rahmenbedingungen auf dem Arbeitsmarkt und in den sozialen Sicherungssystemen
            Regelungen der Altersteilzeitarbeit und Altersrente wegen Arbeitslosigkeit
            Erleichterte Befristung von Arbeitsverhältnissen mit älteren Arbeitnehmern
            Förderung der Weiterbildung für Arbeitnehmer ab 50 Jahre
            Entgeltsicherung für ältere Arbeitnehmer
            Befreiung des Arbeitgebers von Beiträgen zur Arbeitslosenversicherung
    3.3 Regionale arbeitsmarktpolitische Programme und Maßnahmen
        3.3.1 Bundesprogramm „Perspektive 50plus“
        3.3.2 Programme aus dem Bayerischen Arbeitsmarktfonds
        3.3.3 Arbeitsmarktpolitisches Programm in Thüringen „50-plus“
        3.3.4 Kampagne „Zeitarbeit mit 50 plus“ in Nordrhein-Westfalen
    3.4 Bildungsmaßnahmen zur Sicherung der Beschäftigungsfähigkeit und Verbesserung der Wiedereingliederungschancen älterer Arbeitnehmer
    3.5 Maßnahmen zur alterns- und altersgerechten Erwerbsarbeit von überbetrieblichen Akteuren
    3.6 Zusammenfassung und Schlussfolgerung
4 Ältere Arbeitnehmer in Unternehmen – Chancen, Risiken und Modelle
    4.1 Neuorientierung der betrieblichen Personalpolitik
        4.1.1 Alternsgerechte Arbeitsgestaltung
        4.1.2 Betriebliche Gesundheitsförderung
        4.1.3 Weiterbildung und lebensbegleitendes Lernen"""

BACHELOR63_HEADLINES = """\
1 Einleitung
2 Grundlagen
    2.1 Blutdruck
    2.2 Ultraschall-Doppler -Blutflussmessung
    2.3 Digitale Regelung
    2.4 Programmiersprache LabVIEW
    2.5 Valsalva-Press-Versuch
3 Aufgabenstellung
    3.1 Bestehender Versuchsaufbau
    3.2 Anforderungen an den neuen Versuchsaufbau
4 Material und Methoden
    4.3 Erstellung einer Bedienoberfläche
    4.4 Überarbeitung der Sondenfixierung
5 Ergebnisse
    5.1 Optimierter Versuchsaufbau
    5.2 Testmessungen
6 Diskussion und Ausblick
7 Anhang
    7.1 Programmstruktur
        7.1.1 Hauptprogramm
        7.1.2 Sub-VI „Messprogramm“
    7.2 Hardwareaufbau
        7.2.1 Schalt- und Anschlusspläne
            7.2.1.1 Schaltplan Verteilerplatine
            7.2.1.4 Pneumatikplan Druckerzeugungseinheit Quelle: Diplomarbeit Thomas Eberhard [Ebe96]
        7.2.2 Zeichnungen
            7.2.2.1 Frontplatte
    7.3 Sondenfixierung
        7.3.1 Zeichnung Befestigungsblock
    7.4 Testmessungen
        7.4.1 Messprotokoll
Literaturverzeichnis"""


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.MASTER098_PDF, MASTER98_HEADLINES, id='master98'),
    pytest.param(power.BACHELOR090_PDF, BACHELOR90_HEADLINES, id='bachelor90'),
    pytest.param(
        power.DISS264_PDF,
        DISS264_HEADLINES,
        id='diss264',
        marks=pytest.mark.xfail,
    ),
    pytest.param(power.BACHELOR063_PDF, BACHELOR63_HEADLINES, id='bachelor63'),
])
@utilatest.skip_nightly
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
        for headline in chapter:
            if headline.level is None:
                intent = ''
            else:
                intent = (headline.level - 1) * '    '
            collected.append(intent + headline.text)
    return utila.NEWLINE.join(collected)
