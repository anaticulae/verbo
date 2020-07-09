#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila
from utila import ResultFile as RF
from utila import create_step as step
from utila import featurepack

from words import HEADLINE_STEP
from words import HEADLINE_STEP_RESULT
from words import HEADLINES
from words import PROCESS
from words import ROOT
from words import __version__

DESCRIPTION = 'TODO'

ResultFile = lambda producer, name: RF(producer=producer, name=name)  # pylint:disable=C0103

TEXTINPUT = [
    ResultFile('rawmaker', 'text_text'),
    ResultFile('rawmaker', 'text_positions'),
    ResultFile('rawmaker', 'fonts_header'),
    ResultFile('rawmaker', 'fonts_content'),
    ResultFile('words', HEADLINES),
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
            ResultFile('words', HEADLINES),
        ],
        output=('detected',),
    ),
    step(
        'boxed',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('words', HEADLINES),
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
        HEADLINE_STEP,
        inputs=[
            ResultFile('sections', 'section_result'),
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('rawmaker', 'fonts_header'),
            ResultFile('rawmaker', 'fonts_content'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('rawmaker', 'boxes_boxes'),
            ResultFile('groupme', 'footer_footerheader'),
        ],
        output=(HEADLINE_STEP_RESULT,),
    ),
    step(
        'list',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('words', HEADLINES),
            ResultFile('groupme', 'footer_footerheader'),
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
            ResultFile('words', HEADLINES),
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
