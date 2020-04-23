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


def test_textflow_quotation(testdir, monkeypatch):
    pages = '--pages=10:20'
    # run words
    tests.run(f'-i {tests.resources.MASTER72} {pages}', monkeypatch=monkeypatch)
    tests.textflow_.run(
        f'-i {tests.resources.MASTER72} -i {testdir.tmpdir} {pages} --quotation',
        monkeypatch=monkeypatch,
    )
    source = textflow.path.quotation(testdir.tmpdir)
    current = textflow.features.quotation.load_quotations(source)
    assert current
    assert len(current) >= 30, str(current)

    dumped = textflow.features.quotation.dump_quotations(current)
    loaded = textflow.features.quotation.load_quotations(dumped)
    assert loaded == current
