# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def headlines(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'words',
        'headlines_headlines',
        prefix,
    )


def oneline_headlines(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'words',
        'headlines_oneline',
        prefix,
    )


def text(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'words', 'text_text', prefix)


def word(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'words', 'word_result', prefix)


def lists(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'words', 'list_list', prefix)


def links(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'words', 'links_links', prefix)
