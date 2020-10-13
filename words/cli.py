#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila
from utila import ResultFile
from utila import create_step as step
from utila import featurepack

from words import PROCESS
from words import ROOT
from words import __version__

DESCRIPTION = 'TODO'

TEXTINPUT = [
    ResultFile('rawmaker', 'text_text'),
    ResultFile('rawmaker', 'text_positions'),
    ResultFile('rawmaker', 'fonts_header'),
    ResultFile('rawmaker', 'fonts_content'),
    ResultFile('words', 'headlines_headlines'),
    ResultFile('rawmaker', 'border_pages'),
    ResultFile('groupme', 'footer_footerheader'),
    ResultFile('rawmaker', 'boxes_boxes'),
    ResultFile('words', 'list_list'),
]

WORKPLAN = [
    step(
        'abbreviation',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('words', 'headlines_headlines'),
        ],
        output=('detected',),
    ),
    step(
        'boxed',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('words', 'headlines_headlines'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('rawmaker', 'boxes_boxes'),
            ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('boxed',),
    ),
    step(
        'footerlink',
        inputs=TEXTINPUT,
        output=('footerlink',),
    ),
    step(
        'headlines',
        inputs=[
            ResultFile('sections', 'section_result'),
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('rawmaker', 'fonts_header'),
            ResultFile('rawmaker', 'fonts_content'),
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
            ResultFile('rawmaker', 'oneline_fonts_header'),
            ResultFile('rawmaker', 'oneline_fonts_content'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('rawmaker', 'boxes_boxes'),
            ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('headlines', 'oneline'),
    ),
    step(
        'list',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('words', 'headlines_headlines'),
            ResultFile('groupme', 'footer_footerheader'),
            ResultFile('magic', 'content_content', optional=True),
        ],
        output=('list',),
    ),
    step(
        'text',
        inputs=TEXTINPUT,
        output=('text',),
    ),
    # TODO: IS THAT RIGHT?
    step(
        'word',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('words', 'headlines_headlines'),
            ResultFile('words', 'list_list'),
            ResultFile('words', 'boxed_boxed'),
        ],
        output=('result',),
    ),
]


def main():
    featurepack(
        root=ROOT,
        workplan=WORKPLAN,
        featurepackage='words.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=PROCESS,
            pages=True,
            version=__version__,
        ),
    )
