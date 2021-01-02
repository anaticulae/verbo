# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utila

import docref

DESCRIPTION = """\
Docref parses all in-doc-refrences which connect text elements(siehe
Abbildung 5) with structure elements(figure, table, etc.).
"""

WORKPLAN = [
    utila.create_step(
        'bibliography',
        inputs=[
            utila.ResultFile('words', 'text_text'),
            utila.ResultFile('words', 'headlines_headlines'),
        ],
        output=('parsed',),
    ),
    utila.create_step(
        'figure',
        inputs=[
            utila.ResultFile('words', 'text_text'),
            utila.ResultFile('words', 'headlines_headlines'),
        ],
        output=('parsed',),
    ),
    utila.create_step(
        'section',
        inputs=[
            utila.ResultFile('words', 'text_text'),
            utila.ResultFile('words', 'headlines_headlines'),
        ],
        output=('parsed',),
    ),
    utila.create_step(
        'table',
        inputs=[
            utila.ResultFile('words', 'text_text'),
            utila.ResultFile('words', 'headlines_headlines'),
        ],
        output=('parsed',),
    ),
]

# pylint:disable=C0103
main = functools.partial(
    utila.featurepack,
    root=docref.ROOT,
    workplan=WORKPLAN,
    featurepackage='docref.features',
    config=utila.FeaturePackConfig(
        description=DESCRIPTION,
        multiprocessed=True,
        name=docref.PROCESS,
        pages=True,
        version=docref.__version__,
    ),
)
