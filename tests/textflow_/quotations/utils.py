# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import tests
import tests.textflow_
import textflow.path
import textflow.quotation.serialize


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
