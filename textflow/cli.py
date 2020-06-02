#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import functools

import utila

import textflow

DESCRIPTION = ('Textflow extracts the text alignment, spaces between '
               'words and line endings for every line.\n')

WORKPLAN = [
    utila.create_step(
        'alignment',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('current', 'expected'),
    ),
    utila.create_step(
        'lineending',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('lastchar',),
    ),
    utila.create_step(
        'quotation',
        inputs=[
            utila.ResultFile('words', 'word_result'),
            utila.ResultFile('words', 'list_list'),
        ],
        output=('quotation',),
    ),
]

# pylint:disable=C0103
main = functools.partial(
    utila.featurepack,
    root=textflow.ROOT,
    workplan=WORKPLAN,
    featurepackage='textflow.features',
    config=utila.FeaturePackConfig(
        description=DESCRIPTION,
        multiprocessed=True,
        name=textflow.PROCESS,
        pages=True,
        version=textflow.__version__,
    ),
)
