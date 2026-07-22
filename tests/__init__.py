#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Testing Words Module
====================

Required resources:

  * text
  * font
  * position
  * page-size, to determine the distance from left border to text
"""

import hoverpower
import utilo
import utilotest

import words

hoverpower.setup(words.ROOT)

run, fail = utilotest.create_cli_runner(words)

utilotest.register_marker('huge')


def assert_length(sentences, count, msg=''):
    if len(sentences) == count:
        return
    for sentence in sentences:
        utilo.log(sentence, end='\n\n')
    assert len(sentences) == count, f'{len(sentences)}=={count} {msg}'
