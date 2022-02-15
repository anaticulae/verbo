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

import functools

import power
import utila
import utilatest

import words
import words.cli

power.setup(words.ROOT)

run = functools.partial(  #pylint:disable=C0103
    utilatest.run_command,
    main=words.cli.main,
    process=words.PROCESS,
    success=True,
)

fail = functools.partial(  #pylint:disable=C0103
    utilatest.run_command,
    main=words.cli.main,
    process=words.PROCESS,
    success=False,
)

utilatest.register_marker('huge')


def assert_length(sentences, count, msg=''):
    if len(sentences) == count:
        return
    for sentence in sentences:
        utila.log(sentence, end='\n\n')
    assert len(sentences) == count, f'{len(sentences)}=={count} {msg}'
