# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_textrule

WORKPLAN = [
    utila.create_step(
        'quotation_mark',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
        ],
        output=('user', 'developer'),
    ),
]


def main():
    utila.featurepack(
        root=decider_textrule.ROOT,
        workplan=WORKPLAN,
        featurepackage='decider_textrule.features',
        config=utila.FeaturePackConfig(
            description='',
            multiprocessed=True,
            name=decider_textrule.PROCESS,
            pages=True,
            version=decider_textrule.__version__,
        ),
    )
