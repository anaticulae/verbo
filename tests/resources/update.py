# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hey.example
import power
import utila

WORKER = 12

PACKAGE = [
    (power.MASTER072_PDF, None),
    (power.BACHELOR076_PDF, None),
    (power.MASTER098_PDF, '0:20'),
    (power.HOMEWORK040_PDF, None),
    (power.BACHELOR037_PDF, None),
    (power.DOCU07_PDF, None),
    (power.DOCU09_PDF, None),
    (power.DOCU27_PDF, None),
]


def extract_examples():
    if os.path.exists(power.generated()):
        return
    utila.log(f'root: {power.REPOSITORY}')

    hey.example.extract(
        files=PACKAGE,
        destination=power.generated(),
        groupme=True,
        sections=True,
        worker=WORKER,
    )
