# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila

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


def test_extract_levelfour_bachelor90():
    source = power.link(power.BACHELOR090_PDF)
    navigators = serializeraw.create_pagetextcontentnavigators_frompath(
        path=source,
        prefix='oneline',
        pages=utila.ranged_tuple(11, 90),
    )
    headlines = words.headlines.levelfour.headlines(navigators)
    current = '\n'.join(item.text for item in headlines)
    assert current == EXPECTED
