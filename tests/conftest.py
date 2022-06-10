# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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
    (power.BACHELOR241_PDF, '70:90'),
    (power.BOOK173_PDF, '0:100'),
    (power.DISS178_PDF, '16:70'),
    (power.DISS205_PDF, '0:50'),
    (power.DISS264_PDF, '0:100'),
    (power.HOME050_PDF, '30:40'),
    (power.MASTER063_PDF, '20:30'),
    power.BACHELOR032A_PDF,
    power.BACHELOR037_PDF,
    power.BACHELOR051_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR067_PDF,
    power.BACHELOR076_PDF,
    power.BACHELOR090_PDF,
    power.BACHELOR128_PDF,
    power.DISS143_PDF,
    power.DISS172_PDF,
    power.DISS218_PDF,
    power.DISS266_PDF,
    power.DOCU009_PDF,
    power.DOCU027_PDF,
    power.MASTER072_PDF,
    power.MASTER075_PDF,
    power.MASTER098_PDF,
    power.MASTER099_PDF,
    power.MASTER110_PDF,
    power.MASTER116_PDF,
    power.MASTER155_PDF,
]

WORKER = 4


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    utila.log(f'root: {power.REPOSITORY}')
    genex.extract(
        files=resources,
        destination=power.generated(),
        base=power.REPOSITORY,
        caption=True,
        cleanup=True,
        codero=True,
        figureo=True,
        formulero=True,
        groupme=True,
        headlines=True,
        magic=True,
        sections=True,
        tablero=True,
        words=True,
        worker=WORKER,
        pages=':',
    )
