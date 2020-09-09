# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import tests
import tests.textflow_
import textflow.features.quotation
import textflow.path
import textflow.quotation.serialize


def extract_quotation(source, pages, testdir, monkeypatch):
    # run words
    tests.run(f'-i {source} {pages}', monkeypatch=monkeypatch)
    tests.textflow_.run(
        f'-i {source} -i {testdir.tmpdir} {pages} --quotation',
        monkeypatch=monkeypatch,
    )
    outpath = textflow.path.quotation(testdir.tmpdir)
    extracted = textflow.quotation.serialize.load_quotations(outpath)
    return extracted


@utilatest.skip_longrun
def test_textflow_quotation_master72_pages10_20(testdir, monkeypatch):
    pages = '--pages=10:21'
    source = power.link(power.MASTER072_PDF)

    current = extract_quotation(source, pages, testdir, monkeypatch)
    assert current
    assert len(current) >= 30, str(current)

    dumped = textflow.quotation.serialize.dump_quotations(current)
    loaded = textflow.quotation.serialize.load_quotations(dumped)
    assert loaded == current


def test_textflow_quotation_bachelor76(testdir, monkeypatch):
    pages = '--pages=4,5'
    source = power.link(power.BACHELOR076_PDF)
    quotations = extract_quotation(source, pages, testdir, monkeypatch)

    expected = 5
    assert len(quotations) == expected


# TODO: ADJUST EXPECTED AFTER IMPROVING PARSER
BACHELOR76_EXPECTED = """\
„ Digitalisierung ”

„ Gesetzen der Digitalisierung ”

„ Alles , was digitalisiert und in Informationen verwandelt werden kann , wird\
 digita - lisiert und in Informationen verwandelt ”

„ Was automatisiert werden kann , wird automatisiert ”

„ Jede Technologie , die zum Zweck der Überwachung und Kontrolle kolonisiert wer\
 - den kann , wird , was immer auch ihr ursprünglicher Zweck war , zum Zwecke der\
 Überwachung und Kontrolle kolonisiert ”

„ Digitalisierung und Industrie 4.0 im Mittelstand – Gestaltungsmöglich - \
keiten der digitalen Infrastruktur entlang der Wertschöpfungskette ”

„ Unter dem Begriff Digitalisierung verstehen wir die Transformation von \
Geschäftsmodellen mit Hilfe von Informations - und Kommunikationstechnologien \
zur Reduktion von Schnittstellen , zur funktionsübergreifenden Vernetzung und\
 zur Erhöhung der Effektivität und Effizienz ”

„ Industrie 4.0 ”"""

# „ digitale Revolution ”

# „ Cyber - Physischen Systemen ”

# „ In - dustrie 4.0 ”"""


@utilatest.skip_longrun
def test_textflow_validate_quotation_bachelor76_page4_10(testdir, monkeypatch):
    quotations = extract_quotations(
        power.BACHELOR076_PDF,
        '4:10',
        testdir,
        monkeypatch,
    )

    expected = len(BACHELOR76_EXPECTED.split('\n\n'))
    assert len(quotations) == expected

    raw = (2 * utila.NEWLINE).join([item.sentence for item in quotations])
    assert raw == BACHELOR76_EXPECTED


def test_textflow_validate_quotation_bachelor76_page8(testdir, monkeypatch):
    quotations = extract_quotations(
        power.BACHELOR076_PDF,
        '8',
        testdir,
        monkeypatch,
    )
    assert len(quotations) == 2


def extract_quotations(
        source,
        pages: str,
        testdir,
        monkeypatch,
) -> textflow.quotation.data.ExtractedQuotation:
    source = power.link(source)
    # run words
    tests.run(f'-i {source} --pages={pages}', monkeypatch=monkeypatch)
    tests.textflow_.run(
        f'-i {source} -i {testdir.tmpdir} --pages={pages} --quotation',
        monkeypatch=monkeypatch,
    )
    path = textflow.path.quotation(testdir.tmpdir)
    result = textflow.quotation.serialize.load_quotations(path)
    return result
