# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import docref


def docref_figure(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, docref.PROCESS, 'figure_parsed', prefix)


def docref_section(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, docref.PROCESS, 'section_parsed', prefix)


def docref_table(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, docref.PROCESS, 'table_parsed', prefix)


def docref_bibliography(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, docref.PROCESS, 'bibliography_parsed', prefix)  # yapf:disable
