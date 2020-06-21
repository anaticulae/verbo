#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
import glob
import os

import utila
import utilatest

import tests.resources
import words
import words.cli

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


def write_capsys(capsys):
    """Save logged capsys to filespace"""
    stdout, stderr = capsys.readouterr()
    utila.file_create('logging.txt', stdout)
    utila.file_create('error.txt', stderr)


def pdfs():
    """Collect all pdf files in test folder"""
    pattern = os.path.join(tests.resources.RESOURCES, '**/*.pdf')
    located = glob.glob(pattern, recursive=True)
    return located


def relative_path(item):
    item = item.replace(tests.resources.RESOURCES, '')
    start_with_slash = item[0] in ('/', '\\')
    if start_with_slash:
        item = item[1:]

    item = utila.forward_slash(item)
    return item


def prepare(item):
    return item.replace(utila.NEWLINE, '').replace(' ', '_')[0:40]
