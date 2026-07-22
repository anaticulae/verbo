# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilo
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

hoverpower.setup(__file__)

RESOURCES = [
    (hoverpower.BACHELOR028_PDF, '2:20'),
    (hoverpower.BOOK173_PDF, '0:100'),
    (hoverpower.DISS205_PDF, '0:50'),
    (hoverpower.HOME050_PDF, '30:40'),
    hoverpower.BACHELOR032A_PDF,
    hoverpower.BACHELOR037_PDF,
    hoverpower.BACHELOR051_PDF,
    hoverpower.BACHELOR063_PDF,
    hoverpower.BACHELOR067_PDF,
    hoverpower.BACHELOR076_PDF,
    hoverpower.BACHELOR077_PDF,
    hoverpower.BACHELOR090_PDF,
    hoverpower.BACHELOR128_PDF,
    hoverpower.DISS143_PDF,
    hoverpower.DISS172_PDF,
    hoverpower.DISS218_PDF,
    hoverpower.DISS266_PDF,
    hoverpower.DOCU009_PDF,
    hoverpower.DOCU027_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER075_PDF,
    hoverpower.MASTER098_PDF,
    hoverpower.MASTER110_PDF,
    hoverpower.MASTER116_PDF,
    hoverpower.MASTER155_PDF,
]

WORKER = utilotest.worker_count(4, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    utilo.log(f'root: {hoverpower.REPO}')
    gennex.extract(
        files=resources,
        caption=True,
        cleanup=True,
        codero=True,
        figureo=True,
        footnote=True,
        formulero=True,
        groupme=True,
        headlines=True,
        headnote=True,
        lists=True,
        magic=True,
        pagenumber=True,
        sections=True,
        sections_ref=True,
        tablero=True,
        words=True,
        worker=WORKER,
    )
