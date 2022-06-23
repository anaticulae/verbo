#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import words

ResultFile = utila.ResultFile

DESCRIPTION = 'TODO'

TEXTINPUT = [
    ResultFile('rawmaker', 'oneline_text_text'),
    ResultFile('rawmaker', 'oneline_text_positions'),
    ResultFile('rawmaker', 'oneline_fonts_header'),
    ResultFile('rawmaker', 'oneline_fonts_content'),
    ResultFile('words', 'headlines_headlines'),
    ResultFile('rawmaker', 'border_pages'),
    ResultFile('groupme', 'footer_footerheader'),
    ResultFile('rawmaker', 'boxes_boxes'),
    ResultFile('words', 'list_list'),
]

# TODO: USE ONELINE CONTENT FOR TEXT COMPUTATION?!

WORKPLAN = [
    utila.create_step(
        'abbreviation',
        inputs=[
            ResultFile('words', 'sentences_sentences'),
        ],
        output=('detected',),
    ),
    utila.create_step(
        'boxed',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('headlines', 'result_result'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('rawmaker', 'boxes_boxes'),
            ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('boxed',),
    ),
    utila.create_step(
        'footerlink',
        inputs=TEXTINPUT,
        output=('footerlink',),
    ),
    utila.create_step(
        'headlines',
        inputs=[
            ResultFile('headlines', 'result_result'),
        ],
        output=('headlines', 'oneline'),
    ),
    utila.create_step(
        'links',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('headlines', 'result_result'),
        ],
        output=('links',),
    ),
    utila.create_step(
        'text',
        inputs=TEXTINPUT + [
            ResultFile('magic', 'content_content', optional=True),
            ResultFile('rawmaker', 'formula_formula', optional=True),
        ],
        output=('text',),
    ),
    # TODO: IS THAT RIGHT?
    utila.create_step(
        'word',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('headlines', 'result_result'),
            ResultFile('words', 'list_list'),
            ResultFile('words', 'boxed_boxed'),
        ],
        output=('result',),
    ),
    utila.create_step(
        'sentences',
        inputs=[
            ResultFile('words', 'word_result'),
            ResultFile('words', 'list_list'),
            ResultFile('headlines', 'result_result'),
            # ResultFile('words', 'boxed_boxed'),
        ],
        output=('sentences', 'bounding'),
    ),
]


def main():
    utila.featurepack(
        root=words.ROOT,
        workplan=WORKPLAN,
        featurepackage='words.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=words.PROCESS,
            pages=True,
            version=words.__version__,
        ),
    )
