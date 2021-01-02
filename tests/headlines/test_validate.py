# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
1 Einleitung
2 Theoretische Grundlagen
    2.1 Von der mémoire collective zu den Lieux de mémoire
    2.2 Binationale Erinnerungsorte
    2.3 Das dialogische Erinnern von Aleida Assmann
    2.4 Erinnerungsorte im DaF-Landeskundeunterricht
3 Der Elysée-Vertrag – Ein deutsch-französischer Erinnerungsort
    3.1 Die Vorgeschichte
    3.2 Adenauer, de Gaulle und der Elysée-Vertrag
    3.3 Mythos Elysée-Vertrag
    3.4 Die Entwicklung des Elysée-Vertrags vom Ereignis zum Erinnerungsort
4 Didaktisierung
    4.1 Eignung des Elysée-Vertrags für den DaF-Landeskundeunterricht
    4.2 Zielgruppe und Sprachniveau
    4.3 Zielsetzungen
    4.4 Vorstellung der Materialien
5 Reflexion
    5.1 Reflexion der Themenwahl
    5.2 Reflexion der Zielgruppe
    5.3 Reflexion der inhaltlichen Lernziele
    5.4 Reflexion der sprachlichen Lernziele
    5.5 Reflexion der Methodik und des Materials
    5.6 Reflexion der kulturdidaktischen Lernziele
6 Fazit und Ausblick
7 Verzeichnisse
    7.1 Literaturverzeichnis
    7.2 Tabellenverzeichnis
8 Anhang
Erklärung"""

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
        2.1.1 Invasive Messung des arteriellen Drucks
        2.1.2 Nicht-invasive Messung des arteriellen Drucks
            2.1.2.1 Auskultatorische Methode
            2.1.2.2 Oszillometrische Methode
            2.1.2.3 Volumenkompensationsmethode
    2.2 Ultraschall-Doppler -Blutflussmessung
    2.3 Digitale Regelung
        2.3.1 Grundprinzip der Regelungste chnik
        2.3.2 Besonderheiten der digitalen Regelung
        2.3.3 Der PI-Regler
    2.4 Programmiersprache LabVIEW
    2.5 Valsalva-Press-Versuch
3 Aufgabenstellung
    3.1 Bestehender Versuchsaufbau
    3.2 Anforderungen an den neuen Versuchsaufbau
4 Material und Methoden
    4.1 Realisierung einer digitalen Steuerung/Regelung
        4.1.1 Programmierung
        4.1.2 Anpassung der Hardware
    4.2 Anpassung der Messwerte mit alternativem Verfahren
        4.2.1 Oszillometrische Bestimmung des mittleren arteriellen Blutdrucks
        4.2.2 Anpassung der Druckwerte
        4.2.3 Manuelle Eingabe alternativer Werte
    4.3 Erstellung einer Bedienoberfläche
        4.3.1 Anforderungen an die Bedienoberfläche
        4.3.2 Hauptprogramm
        4.3.3 Sub-VI „Messprogramm“
    4.4 Überarbeitung der Sondenfixierung
5 Ergebnisse
    5.1 Optimierter Versuchsaufbau
    5.2 Testmessungen
        5.2.1 Durchführung
        5.2.2 Ergebnisse
6 Diskussion und Ausblick
7 Anhang
    7.1 Programmstruktur
        7.1.1 Hauptprogramm
        7.1.2 Sub-VI „Messprogramm“
        7.1.3 Blockdiagramm der optimierten Regelschleife
    7.2 Hardwareaufbau
        7.2.1 Schalt- und Anschlusspläne
            7.2.1.1 Schaltplan Verteilerplatine
            7.2.1.2 Schaltplan Netzversorgung
            7.2.1.3 Anschlussplan
            7.2.1.4 Pneumatikplan Druckerzeugungseinheit
        7.2.2 Zeichnungen
            7.2.2.1 Frontplatte
            7.2.2.2 Rückwand
    7.3 Sondenfixierung
        7.3.1 Zeichnung Befestigungsblock
    7.4 Testmessungen
        7.4.1 Messprotokoll
Literaturverzeichnis"""

BACHELOR051_HEADLINES = """\
1 Einleitung und Problemstellung
2 Zielsetzung
3 Gegenwärtiger Kenntnisstand
    3.1 Heutige Lebens- und Arbeitswelt
        3.1.1 Heutige Lebenswelt
        3.1.2 Heutige Arbeitswelt
    3.2 Begriffserklärung Gesundheit
        3.2.1 Allgemeine Gesundheit
        3.2.2 Psychische Gesundheit
    3.3 Themengebiet Stress
        3.3.1 Begriffserklärung Stress
        3.3.2 Stressmodell nach Lazarus
        3.3.3 Begriffserklärung Individuelles Stresserleben
        3.3.4 Begriffserklärung Stressbewältigung
        3.3.5 Folgen von Stress
    3.4 Sportaktivität und individuelles Stresserleben
    3.5 Funktionsweise EMS-Training und Studienlage
        3.5.1 Funktionsweise EMS-Training
        3.5.2 Studienlage EMS-Training und individuelles Stresserleben
4 Methodik
    4.1 Untersuchungsablauf und Probandenrekrutierung
        4.1.1 Untersuchungsablauf
        4.1.2 Probandenrekrutierung
    4.2 Erhebungsinstrument Individuelles Stresserleben
    4.3 Standardisiertes EMS-Krafttrainingsprogramm
        4.3.1 Beschreibung EMS-Krafttrainingsprogramm
        4.3.2 Durchführung beim Kunden zu Hause
    4.4 Auswertung der Befragung
        4.4.1 Deskriptive Auswertung
        4.4.2 Inferenzstatistische Auswertung
5 Ergebnisse
    5.1 Deskriptive Ergebnisse
    5.2 Inferenzstatistische Ergebnisse
6 Diskussion
    6.1 Methodendiskussion
    6.2 Ergebnisdiskussion
    6.3 Schlussfolgerungen und Ausblick
7 Zusammenfassung
8 Literaturverzeichnis
9 Abbildungs-, Tabellen-, Abkürzungsverzeichnis
    9.1 Abbildungsverzeichnis
    9.2 Tabellenverzeichnis
    9.3 Abkürzungsverzeichnis
Anhang"""

DOCU027_HEADLINES = """\
RestructuredText Tutorial
RestructuredText Guide
    Basics
    Blockquotes
    Code: Block
RestructuredText Customizations
Sphinx Tutorial
    Step 1
        Getting Set Up
        Documenting a Project
        Aside: Other formats
    Step 2
        Referencing Code
Sphinx Guide
Sphinx Customizations
Testing your Documentation
Indices and tables"""

# TODO: 5.2 Die ´Demenzkampagne Ostfildern „Wir sind Nachbarn!“`: Oktober 2007 – Juni 2008
BACHELOR128_HEADLINES = """\
1. Einleitung
    1.1 Problemstellung
    1.2 Zielsetzung der Arbeit
    1.3 Gliederung und Vorgehensweise der Arbeit
2. Demenz
    2.1 Das Bild der ´Demenz`
    2.2 Demenz – Ablehnung oder Akzeptanz?
    2.3 Folgen für Menschen mit Demenz
    2.4 Bedarf von Menschen mit Demenz
3. Kommune
    3.1 Demenz und Kommune – wie gehören diese Begriffe zusammen?
    3.2 Sozialpolitische Aufgaben
    3.3 Kommunale Aufgaben
        3.3.1 Aufgaben in der Altenplanung
        3.3.2 Das Thema Demenz in die Öffentlichkeit rücken
    4.1 Die Zivilgesellschaft
        4.1.1 Begriffsbestimmung
        4.1.2 Aspekte für eine aktive Zivilgesellschaft
        4.1.3 Grundbausteine eines zivilgesellschaftlichen Demenzmodells
        4.1.4 „Leben und Sterben, wo ich hingehöre!“
    4.2. Das Bürgerschaftliche Engagement
        4.2.1 Begriffsbestimmung
        4.2.2 Merkmale und Akteure
        4.2.3 Formen
        4.2.4 Hochkonjunktur bürgerschaftliches Engagement – wie und warum?
    4.3 Bedeutungen für eine demenzfreundliche Kommune
5. Initiative: ´Demenzfreundliche Kommune`
    5.1 Auf dem Weg zum Verein „Aktion Demenz e.V.“
        5.2.1 Projektplanung
        5.2.2 Projektbeteiligte
        5.2.3 Ziele und Inhalte des Projektes
        5.2.4 Projektdurchführung
        5.2.5 Ergebnisse und Wirkungen
    5.3 Das ´Projekt-Demenz-Arnsberg`: Januar 2008 – etwa Dezember 2010
        5.3.1 Projektplanung
        5.3.2 Projektbeteiligte
        5.3.3 Ziele und Inhalte des Projektes
        5.3.4 Projektdurchführung
        5.3.5 Ergebnisse und Wirkungen
6. Empirische Untersuchung
    6.1 Methodische Vorgehensweise
        6.1.1 Strukturiertes Leitfadeninterview am Beispiel des Experteninterviews
        6.1.2 Auswahl der Interviewpartner
        6.1.3 Aufbau und Inhalt des Interviewleitfaden
        6.1.4 Vorbereitung und Durchführung der Interviews
        6.1.5 Vorgehensweise der Auswertung
    6.2 Verarbeitungen der Erkenntnisse
        6.2.1 Auswertung der Interviewergebnisse
            6.2.1.1 Ergebnisse in Bezug auf den Theorieteil
            6.2.1.2 Ergebnisse in Bezug auf den Praxisteil
    6.3. Gemeinsamkeiten und Unterschiede der vorgestellten Initiativen
7. Handlungsempfehlungen
8. Fazit und Ausblick
    8.1 Fazit
    8.2 Ausblick
Quellenverzeichnis
Bibliografie
Zeitschriftenartikel
Internetquellen
Anhangsverzeichnis
Eidesstattliche Versicherung"""

MASTER110_HEADLINES = """\
Einleitung
    1.1 Stufen eines Bildverarbeitungssystems
    1.2 Aufbau der Arbeit
    1.3 Wissenschaftlicher Beitrag
Stand der Technik
    2.1 Tiefenbild Segmentierungstechniken
    2.2 Objekterkennung
        2.2.1 Template Matching
        2.2.2 Principal-Component-Analysis (PCA)
        2.2.3 Klassi kation von Merkmalen
Tiefenbilder
    3.1 Erzeugung von Tiefenbildern
    3.2 Eigenschaften von Tiefenbildern
Konturextraktion
    4.1 Bildvorverarbeitung
        4.1.1 Kontrastverbesserung
        4.1.2 Glattung durch lokale Operatoren
        4.1.3 Glattung durch morphologische Operatoren
    4.2 Segmentierungsverfahren
        4.2.1 Canny Kantendetektion
        4.2.2 k-means Clustering
        4.2.3 Schwellwertverfahren
    4.3 Konturextraktion
    4.4 Verbesserungen am Eingabebild
        4.4.1 Parallele Projektion
        4.4.2 Entfernung der Bodenpunkte im Tiefenbild
        4.4.3 Manipulation der Grauwertinterpolation
    4.5 Endfassung des Konturextraktionsalgorithmus
Konturreprasentation und Merkmalsextraktion
    5.1 Anforderungen an die Konturreprasentationen
    5.2 Anforderung an die Merkmale
    5.3 Einfache geometrische Merkmale
    5.4 Merkmalsextraktion mittels Momenten
        5.4.1 Hu-Momente
        5.4.2 Zernike-Momente
    5.5 Reprasentation durch den Curvature-Scale-Space (CSS)
        5.5.1 Krummung einer ebenen Kurve
        5.5.2 Eigenschaften der CSS-Reprasentation
        5.5.3 Merkmalsextraktion mit der Eigen-CSS Methode
        5.5.4 CSS-Reprasentation zur Beschreibung von teilweise verdeckten Objekten
    5.6 Angular-Radial-Transformation (ART)
    5.7 Reprasentation durch Fourier-Deskriptoren
    5.8 Border-Signature
Klassi kation
    6.1 Merkmalsauswahl
        6.1.1 plus l-take away r Algorithmus
        6.1.2 Principal-Component-Analysis (PCA)
    6.2 Klassi kationsstrategien
    6.3 Klassi kation mittels Support-Vector-Machines (SVM)
        6.3.2 Duales Optimierungsproblem
        6.3.3 SVM zur Klassi kation von mehreren Objekten
    6.4 Viola Jones AdaBoost Klassi kator
Performanzevaluation
    7.1 Receiver-Operating-Characteristics (ROC)-Analyse
        7.1.1 ROC-Kurven
        7.1.2 Flache unter der ROC-Kurve (AUC)
        7.1.3 Multi-Klassen ROC-Analyse
        7.1.4 Konvexe Hulle der ROC-Kurve und kombinierte Klassi katoren
        7.1.5 Linien gleicher Exaktheit und der optimale Schwellwert
    7.2 Ergebnis der Performanz-Analyse
        7.2.1 Vergleich mit dem Viola Jones AdaBoost Klassi kator
        7.2.2 Klassi kation von verdeckten Konturen
Zusammenfassung und Ausblick
Freeman-Kettencode
Literaturverzeichnis"""

MASTER155_HEADLINES = """\
1. Einleitung
    1.1. Zielsetzung und Aufbau der Arbeit
    1.2. Literaturüberblick
2. Mikroökonomische Grundlagen
    2.1. Nachfragetheorie
    2.2. Produktion und Kosten
    2.3. Vollkommener Markt
    2.4. Abweichungen vom vollkommenen Markt
3. Aufbau des Marktexperiments
    3.1. Experimentelles Design
    3.2. Instruktionen
    3.3. Abfrage der Risikoeinstellung
    3.4. Vergütung
4. Hypothesen und methodisches Vorgehen
    4.1. Hypothesen
    4.2. Methodisches Vorgehen
        4.2.1. Regressionsanalyse
        4.2.2. Stichprobenziehung
        4.2.3. Deskriptive Statistik der Stichprobe
5. Ergebnisse des Marktexperiments
    5.1. Vorgehensweise bei der Modellschätzung
    5.2. Ergebnisse der Modellschätzungen
6. Diskussion und Schlussfolgerungen
7. Summary
Literaturverzeichnis
Anhang"""


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.MASTER098_PDF, MASTER98_HEADLINES, id='master98'),
    pytest.param(power.MASTER155_PDF, MASTER155_HEADLINES, id='master155'),
    pytest.param(power.BACHELOR090_PDF, BACHELOR90_HEADLINES, id='bachelor90'),
    pytest.param(
        power.DISS264_PDF,
        DISS264_HEADLINES,
        id='diss264',
        marks=pytest.mark.xfail,
    ),
    pytest.param(power.BACHELOR063_PDF, BACHELOR63_HEADLINES, id='bachelor63'),
    pytest.param(power.BACHELOR051_PDF, BACHELOR051_HEADLINES, id='bachelor51'),
    pytest.param(power.DOCU27_PDF, DOCU027_HEADLINES, id='docu27'),
    pytest.param(power.BACHELOR128_PDF, BACHELOR128_HEADLINES, id='bsc128'),
    pytest.param(
        power.MASTER110_PDF,
        MASTER110_HEADLINES,
        id='master110',
        marks=pytest.mark.xfail(reason='require ffi special char converter'),
    ),
])
@utilatest.nightly
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
            if headline.raw_level:
                line = intent + headline.raw_level + ' ' + headline.title
            else:
                line = intent + headline.title
            collected.append(line)
    return utila.NEWLINE.join(collected)
