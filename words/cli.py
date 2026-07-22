#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utilo

import words

ResultFile = utilo.ResultFile

DESCRIPTION = 'TODO'

TEXTINPUT = [
    ResultFile('rawmaker', 'oneline_text_text'),
    ResultFile('rawmaker', 'oneline_text_positions'),
    ResultFile('rawmaker', 'oneline_fonts_header'),
    ResultFile('rawmaker', 'oneline_fonts_content'),
    ResultFile('words', 'headlines_headlines'),
    ResultFile('rawmaker', 'border_pages'),
    ResultFile('footnote', 'result_result'),
    ResultFile('rawmaker', 'boxes_boxes'),
    ResultFile('lists', 'result_result'),
]

# TODO: USE ONELINE CONTENT FOR TEXT COMPUTATION?!

WORKPLAN = [
    utilo.create_step(
        'abbreviation',
        inputs=[
            ResultFile('words', 'sentences_sentences'),
        ],
        output=('detected',),
    ),
    utilo.create_step(
        'boxed',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('headlines', 'result_result'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('rawmaker', 'boxes_boxes'),
            ResultFile('footnote', 'result_result'),
        ],
        output=('boxed',),
    ),
    utilo.create_step(
        'footerlink',
        inputs=TEXTINPUT,
        output=('footerlink',),
    ),
    utilo.create_step(
        'headlines',
        inputs=[
            ResultFile('headlines', 'result_result'),
        ],
        output=('headlines', 'oneline'),
    ),
    utilo.create_step(
        'links',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('headlines', 'result_result'),
        ],
        output=('links',),
    ),
    utilo.create_step(
        'text',
        inputs=TEXTINPUT + [
            ResultFile('magic', 'content_content', optional=True),
            ResultFile('rawmaker', 'formula_formula', optional=True),
        ],
        output=('text',),
    ),
    # TODO: IS THAT RIGHT?
    utilo.create_step(
        'word',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('headlines', 'result_result'),
            ResultFile('lists', 'result_result'),
            ResultFile('words', 'boxed_boxed'),
        ],
        output=('result',),
    ),
    utilo.create_step(
        'sentences',
        inputs=[
            ResultFile('words', 'word_result'),
            ResultFile('lists', 'result_result'),
            ResultFile('headlines', 'result_result'),
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('footnote', 'result_result'),
        ],
        output=('sentences', 'bounding'),
    ),
]


def main():
    utilo.featurepack(
        root=words.ROOT,
        workplan=WORKPLAN,
        featurepackage='words.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=words.PROCESS,
            pages=True,
            version=words.__version__,
        ),
    )
