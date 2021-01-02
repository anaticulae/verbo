# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import words.headlines.levelfour

EXPECTED = """\
Abitrierungsphase
Bitstromkompressor
CAN-Nachricht
Geschützte Bereiche
Generierung für eine abstrakte Schnittstelle
Parametrisierte Codegenerierung
Konfiguration des Simulinkmodells
Anpassen der Simulation
Kommunikation durch Ports
Model in the loop
Software in the loop
Hardware in the loop
Programm anlegen3
Programm verwalten
Einlesen
Buffer
Durchmesser
Statistische Auswertung
Lesen vom Speicher
Deserialisierung der Nachrichten
Integrationstest Einlesen
Manueller Einzeltest der Gesamtintegration
Test der Gesamtintegration mit Histogramm
Ergebnis der Integration
Simulink-Modell
Putty
SSH
Player - Ubuntu"""


@utilatest.longrun
def test_extract_levelfour_bachelor90():
    source = power.link(power.BACHELOR090_PDF)
    navigators = serializeraw.create_pagetextcontentnavigators_frompath(
        path=source,
        prefix='oneline',
        pages=utila.ranged_tuple(11, 90),
    )
    headlines = words.headlines.levelfour.headlines(navigators)
    current = '\n'.join(item.title for item in headlines)
    assert current == EXPECTED


MASTER116_EXPECTED = """\
Serielle Hybridstruktur
Parallele Hybridstruktur
Leistungsverzweigte Hybridstruktur
Start-Stopp-Funktion
Elektrisches Boosten
Rekuperation
Elektrisches Fahren
Lastpunktanhebung und Lastpunktverlagerung
Railpower GG20B Greengoat
Alstom H3
Toshiba HD300
Übersicht Hybridlokomotiven
Prüfzyklen von Schienenfahrzeugen
Anforderungen an Referenzzyklen für Hybridfahrzeuge
Luftwiderstand
Rollwiderstand
Steigungswiderstand
Beschleunigungswiderstand
Aufbau und Kinematik einer einfachen Planetenradstufe
Leistungsverzweigung
Generator
Elektrische Fahrmaschine
Rückwärtsrechnung
Vorwärtsrechnung
Velodynmodell
Systemregelung durch den Hybridmanager
Vergleich mit der konventionellen Lokomotive
Vergleich mit dem theoretischen Optimum
Vergleich der Methodik"""


@utilatest.longrun
def test_extract_levelfour_master116():
    source = power.link(power.MASTER116_PDF)
    navigators = serializeraw.create_pagetextcontentnavigators_frompath(
        path=source,
        prefix='oneline',
        pages=utila.ranged_tuple(7, 87),
    )
    headlines = words.headlines.levelfour.headlines(navigators)
    current = '\n'.join(item.title for item in headlines)
    assert current == MASTER116_EXPECTED
