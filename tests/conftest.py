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
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import words

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = words.PACKAGE

power.setup(words.ROOT)

RESOURCES = [
    (power.BACHELOR028_PDF, '2:20'),
    (power.BOOK173_PDF, '0:100'),
    (power.DISS205_PDF, '0:50'),
    (power.HOME050_PDF, '30:40'),
    power.BACHELOR032A_PDF,
    power.BACHELOR037_PDF,
    power.BACHELOR051_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR067_PDF,
    power.BACHELOR076_PDF,
    power.BACHELOR077_PDF,
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
        base=power.REPOSITORY,
        caption=True,
        cleanup=True,
        codero=True,
        figureo=True,
        formulero=True,
        groupme=True,
        headlines=True,
        lists=True,
        magic=True,
        sections=True,
        tablero=True,
        words=True,
        worker=WORKER,
    )
