# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

FIRST = """
Faktultät IV
Institut für gute Getränke

Modellierung und Simulation eines hybriden Lokomotivantriebs

Masterarbeit

vorgelegt von:

B.Sc. Helmut Konrad Fahrendholz 321240

Hochschullehrer: Prof. Dr.-Ing. Cuba Libre
Zweitgutachter: Prof. Dr.-Ing. Coffee Lover
Betreuer: Dipl. Ing. Thomas MÜller

Technische Universität Berlin, Fakultät IV, Institut für gute Getränke,
Fachgebiet Trinken und Essen,

Berlin, 19. April 2016
"""

FIRST_INSTITUTION = iamraw.Institution(
    courseofstudies=None,
    department='IV',
    field='Trinken und Essen',
    institute='gute Getränke',
    university='Technische Universität Berlin',
)
FIRST_EXPECTED = iamraw.TitlePage(
    # title='Modellierung und Simulation eines hybriden Lokomotivantriebs',
    thesis=iamraw.TitleThesisType(
        iamraw.DocumentType.MASTER,
        'Masterarbeit',
        'Masterarbeit',
    ),
    date=iamraw.TitleDate(
        2016,
        4,
        19,
        'Berlin',
        True,
        'Berlin, 19. April 2016',
    ),
    author=iamraw.Person(
        iamraw.AcademicTitle.BSC,
        'Fahrendholz',
        'Helmut Konrad',
        'B.Sc. Helmut Konrad Fahrendholz',
    ),
    matrikel=iamraw.Matrikel(321240, '', '321240'),
    examiner=[
        iamraw.Person(
            iamraw.AcademicTitle.MASTER,
            'MÜller',
            'Thomas',
            'Betreuer: Dipl. Ing. Thomas MÜller',
        ),
        iamraw.Person(
            iamraw.PROF_DR,
            'Libre',
            'Cuba',
            'Hochschullehrer: Prof. Dr.-Ing. Cuba Libre',
        ),
        iamraw.Person(
            iamraw.PROF_DR,
            'Lover',
            'Coffee',
            'Zweitgutachter: Prof. Dr.-Ing. Coffee Lover',
        ),
    ],
    institution=FIRST_INSTITUTION,
)

SECOND = """
Steuerung und Überwachung intelligenter Gebäudetechnik

Masterarbeit

zur Erlangung des akademischen Grades Master of Science
an der Hochschule für Technik und Wirtschaft Berlin,
Fachbereich Wirtschaftswissenschaften II,
Studiengang Angewandte Kunst

vorgelegt von B.Sc. Thomas Helmer
Matrikelnummer: 161647

1. Betreuer: Prof. Dr. Carsten Semilov
2. Betreuer: Dr.-Ing. Dirk Contemporary

Berlin, den 8. August 2015
"""

SECOND_FONTSTORE = None

SECOND_INSTITUTION = iamraw.Institution(
    university='Hochschule für Technik und Wirtschaft Berlin',
    field='Wirtschaftswissenschaften II',
    courseofstudies='Angewandte Kunst',
)
SECOND_EXPECTED = iamraw.TitlePage(
    # title='Steuerung und Überwachung intelligenter Gebäudetechnik',
    thesis=iamraw.TitleThesisType(
        iamraw.DocumentType.MASTER,
        'Masterarbeit',
        'Masterarbeit',
    ),
    date=iamraw.TitleDate(
        2015,
        8,
        8,
        'Berlin',
        True,
        'Berlin, den 8. August 2015',
    ),
    author=iamraw.Person(
        iamraw.AcademicTitle.BSC,
        'Helmer',
        'Thomas',
        'vorgelegt von B.Sc. Thomas Helmer',
    ),
    matrikel=iamraw.Matrikel(
        161647,
        'Matrikelnummer:',
        'Matrikelnummer: 161647',
    ),
    examiner=[
        iamraw.Person(
            iamraw.AcademicTitle.DR,
            'Contemporary',
            'Dirk',
            '2. Betreuer: Dr.-Ing. Dirk Contemporary',
        ),
        iamraw.Person(
            iamraw.PROF_DR,
            'Semilov',
            'Carsten',
            '1. Betreuer: Prof. Dr. Carsten Semilov',
        ),
    ],
    institution=SECOND_INSTITUTION,
)

THIRD = """

Technische Universität Berlin

Fakultät I – Geisteswissenschaften
Institut für Sprache und Kommunikation
Studiengang: Kommunikation und Sprache
Studienschwerpunkt: Medienwissenschaft

Identittsbildung 2.0
Selbstdarstellung und Privatheit im Social Web
___________________________________________________________________


Masterarbeit
Vorgelegt von   Tabea Canham



Gutachter:    Prof. Dr. Nobert Bolz
Zweitgutachter:  Dipl.-Medienberater Stephan Frühwirt


Abgabedatum:   31.7.2014
"""
THIRD_INSTITUTION = iamraw.Institution(
    courseofstudies='Kommunikation und Sprache',
    department='Geisteswissenschaften',
    institute='Sprache und Kommunikation',
    university='Technische Universität Berlin',
)

THIRD_EXPECTED = iamraw.TitlePage(
    institution=THIRD_INSTITUTION,
    author=iamraw.Person(
        title=iamraw.AcademicTitle.STUDENT,
        name='Canham',
        firstname='Tabea',
        raw='Vorgelegt von   Tabea Canham',
    ),
    date=iamraw.TitleDate(
        year=2014,
        month=7,
        day=31,
        location=None,
        valid=False,  # TODO: Check why invalid
        raw='31.7.2014',
    ),
    examiner=[
        iamraw.Person(
            title=iamraw.AcademicTitle.MASTER,
            name='Frühwirt',
            firstname='Stephan',
            raw='Dipl.-Medienberater Stephan Frühwirt',
        ),
        iamraw.Person(
            title=iamraw.PROF_DR,
            name='Bolz',
            firstname='Nobert',
            raw='Prof. Dr. Nobert Bolz',
        ),
    ],
    thesis=iamraw.TitleThesisType(
        iamraw.DocumentType.MASTER,
        title='Masterarbeit',
        raw='Masterarbeit',
    ),
)
