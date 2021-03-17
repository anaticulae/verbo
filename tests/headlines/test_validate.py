# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw
import utila
import utilatest

import tests
import words
import words.path

EXPECTED = os.path.join(words.ROOT, 'tests/headlines/expected')


class LazyFile:

    # TODO: MOVE TO UTILA

    def __init__(self, path):
        self.path = path
        self.content = None

    def lazy(self):
        if self.content is not None:
            return
        self.content = utila.file_read(self.path).strip()

    def __eq__(self, value):
        self.lazy()
        return self.content == value


file_read = lambda x: LazyFile(os.path.join(EXPECTED, x))  # pylint:disable=C0103

BACHELOR037_HEADLINES = file_read('bachelor037')
BACHELOR051_HEADLINES = file_read('bachelor051')
BACHELOR063_HEADLINES = file_read('bachelor063')
BACHELOR090_HEADLINES = file_read('bachelor090')

DISS266_HEADLINES = file_read('diss266')

# TODO: 5.2 Die ´Demenzkampagne Ostfildern „Wir sind Nachbarn!“`: Oktober 2007 – Juni 2008
# 5.2 Die  ´Demenzkampagne  Ostfildern  „Wir  sind  Nachbarn!“`:
# 4. Zivilgesellschaftliche Perspektive und Bürgerschaftliches
BACHELOR128_HEADLINES = file_read('bachelor128')
# Anhang 1: Prävalenz von Demenzen in Abhängigkeit vom Al-
# Anhang 3: Freiwillig Engagierte und „nur“ gemeinschaftlich
# Anhang 4: Freiwillig Engagierte nach Altersgruppen
# Anhang 5: Freiwilliges Engagement und Bereitschaft zum
# Anhang 7: Leitfragebogen
# Anhang 8: Thesenpapier"""

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
    pytest.param(power.BACHELOR037_PDF, BACHELOR037_HEADLINES, id='bachelor37'),
    pytest.param(power.MASTER098_PDF, MASTER98_HEADLINES, id='master98'),
    pytest.param(power.MASTER155_PDF, MASTER155_HEADLINES, id='master155'),
    pytest.param(power.BACHELOR090_PDF, BACHELOR090_HEADLINES, id='bachelor90'),
    pytest.param(
        power.DISS264_PDF,
        DISS264_HEADLINES,
        id='diss264',
        marks=pytest.mark.xfail,
    ),
    pytest.param(power.BACHELOR063_PDF, BACHELOR063_HEADLINES, id='bachelor63'),
    pytest.param(power.BACHELOR051_PDF, BACHELOR051_HEADLINES, id='bachelor51'),
    pytest.param(power.DOCU27_PDF, DOCU027_HEADLINES, id='docu27'),
    pytest.param(power.BACHELOR128_PDF, BACHELOR128_HEADLINES, id='bsc128'),
    pytest.param(
        power.MASTER110_PDF,
        MASTER110_HEADLINES,
        id='master110',
        marks=pytest.mark.xfail(reason='require ffi special char converter'),
    ),
    pytest.param(power.DISS266_PDF, DISS266_HEADLINES, id='diss266'),
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
