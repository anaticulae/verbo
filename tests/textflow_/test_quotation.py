# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

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
