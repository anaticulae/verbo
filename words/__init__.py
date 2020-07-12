#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import words.__patch__

__version__ = '0.12.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS = 'words'
PACKAGE = PROCESS

HEADLINE_STEP = 'headlines'
HEADLINE_STEP_RESULT = 'headlines'
HEADLINES = f'{HEADLINE_STEP}_{HEADLINE_STEP_RESULT}'

WORDS_HEADLINES = f'{PROCESS}__{HEADLINES}.yaml'
