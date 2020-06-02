# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import tests
import tests.resources
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


def test_textflow_quotation(testdir, monkeypatch):
    pages = '--pages=10:20'
    source = tests.resources.MASTER72

    current = extract_quotation(source, pages, testdir, monkeypatch)
    assert current
    assert len(current) >= 30, str(current)

    dumped = textflow.quotation.serialize.dump_quotations(current)
    loaded = textflow.quotation.serialize.load_quotations(dumped)
    assert loaded == current


def test_textflow_quotation_bachelor76(testdir, monkeypatch):
    pages = '--pages=4,5'
    source = tests.resources.BACHELOR76
    quotations = extract_quotation(source, pages, testdir, monkeypatch)

    expected = 5
    assert len(quotations) == expected


BACHELOR76_EXPECTED = """\
„Digitalisierung“

„Gesetzen der Digitalisierung“

„Alles, was digitalisiert und in Informationen verwandelt werden kann, \
wird digitalisiert und in Informationen verwandelt“1

„Was automatisiert werden kann, wird automatisiert“2

„Jede Technologie, die zum Zweck der Überwachung und Kontrolle \
kolonisiert werden kann, wird, was immer auch ihr ursprünglicher Zweck \
war, zum Zwecke der Überwachung und Kontrolle kolonisiert“3

„Digitalisierung und Industrie 4.0 im Mittelstand – \
Gestaltungsmöglichkeiten der digitalen Infrastruktur entlang der \
Wertschöpfungskette“

„Unter dem Begriff Digitalisierung verstehen wir die Transformation von \
Geschäftsmodellen mit Hilfe von Informations- und \
Kommunikationstechnologien zur Reduktion von Schnittstellen, zur \
funktionsübergreifenden Vernetzung und zur Erhöhung der Effektivität und \
Effizienz.“

„Industrie 4.0“
"""


@pytest.mark.xfail(reason='broken list parser and no line `-` connector'
                   ', require quotation out of sentence extractor')
def test_textflow_validate_quotation_bachelor76(testdir, monkeypatch):
    pages = '--pages=4:10'
    source = tests.resources.BACHELOR76
    # run words
    tests.run(f'-i {source} {pages}', monkeypatch=monkeypatch)
    tests.textflow_.run(
        f'-i {source} -i {testdir.tmpdir} {pages} --quotation',
        monkeypatch=monkeypatch,
    )
    path = textflow.path.quotation(testdir.tmpdir)
    quotations = textflow.quotation.serialize.load_quotations(path)
    raw = (2 * utila.NEWLINE).join([item.sentence for item in quotations])

    assert raw == BACHELOR76_EXPECTED
