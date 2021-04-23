# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utila

import words

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = words.PACKAGE

power.setup(words.ROOT)

RESOURCES = [
    power.DISS266_PDF,
    power.MASTER116_PDF,
    power.MASTER155_PDF,
    power.MASTER072_PDF,
    power.MASTER110_PDF,
    power.BACHELOR090_PDF,
    power.MASTER099_PDF,
    (power.DISS264_PDF, '0:100'),
    (power.BACHELOR241_PDF, '70:90'),
    power.BACHELOR076_PDF,
    power.BACHELOR051_PDF,
    power.BACHELOR128_PDF,
    power.BACHELOR063_PDF,
    power.MASTER098_PDF,
    power.MASTER075_PDF,
    (power.BACHELOR056_PDF, '0:20'),
    power.HOME040_PDF,
    power.BACHELOR037_PDF,
    power.DOCU07_PDF,
    power.DOCU09_PDF,
    power.DOCU27_PDF,
    (power.MASTER091B_PDF, '0:20'),
]

WORKER = 6


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run([power.generated()])


def extract(resources):
    utila.log(f'root: {power.REPOSITORY}')
    genex.extract(
        files=resources,
        destination=power.generated(),
        base=power.REPOSITORY,
        groupme=True,
        sections=True,
        words=True,
        magic=True,
        spacestation=True,
        worker=WORKER,
        pages=':',
        rawmaker=genex.CONFIG.replace('--char_margin=3.1', '--char_margin=5.0'),
    )
