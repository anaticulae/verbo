# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
    power.MASTER116_PDF,
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
    power.HOMEWORK040_PDF,
    power.BACHELOR037_PDF,
    power.DOCU07_PDF,
    power.DOCU09_PDF,
    power.DOCU27_PDF,
]

WORKER = 6


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run([power.generated()])


def extract(resources):
    # ensure to handle single file generation or common resource subfolder
    # correctly. To determine the output path it is required to determine
    # the parent path of at least two files. If resources provide only a
    # single file the parental determination is not possible. Therefore we
    # have to add the data root of all test files.
    utila.log(f'root: {power.REPOSITORY}')
    resources.append(power.REPOSITORY)

    genex.extract(
        files=resources,
        destination=power.generated(),
        groupme=True,
        sections=True,
        words=True,
        magic=True,
        worker=WORKER,
        pages=':',
        rawmaker=genex.CONFIG.replace('--char_margin=3.1', '--char_margin=5.0'),
    )
