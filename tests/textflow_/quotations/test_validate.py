# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import utila
import utilatest

import tests.textflow_
import tests.textflow_.quotations.utils
import textflow


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.MASTER072_PDF, 'master072', id='master072'),
])
@utilatest.longrun
def test_validate_quotations_x(source, expected, testdir, monkeypatch):
    expected = file_read(expected)
    current = tests.textflow_.quotations.utils.extract_quotations(
        source,
        ':',
        testdir,
        monkeypatch,
    )
    current: str = quotations_raw(current)
    assert current == expected


def file_read(name):
    path = os.path.join(textflow.ROOT, 'tests/textflow_/quotations/expected')
    loaded = utila.file_read(os.path.join(path, name))
    loaded = loaded.strip()
    return loaded


def quotations_raw(quotes):
    quotes = [
        f'{str(quote.page).zfill(3)} {quote.sentence}' for quote in quotes
    ]
    raw = utila.NEWLINE.join(quotes).strip()
    return raw
