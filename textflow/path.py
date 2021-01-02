# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import textflow


def expected(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        textflow.PROCESS,
        'alignment_expected',
        prefix,
    )


def alignment(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        textflow.PROCESS,
        'alignment_current',
        prefix,
    )


def lineending(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        textflow.PROCESS,
        'lineending_lastchar',
        prefix,
    )


def quotation(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        textflow.PROCESS,
        'quotation_quotation',
        prefix,
    )


def blockquote(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        textflow.PROCESS,
        'blockquote_blockquote',
        prefix,
    )
