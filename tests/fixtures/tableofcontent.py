# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.toc.strategy
import serializeraw

import tests.resources


def headlines_frompath(path: str, pages=None):
    loaded = serializeraw.create_pagetextcontentnavigators_frompath(
        path,
        pages=pages,
        prefix='oneline',
        validate_leftright=False,  # do not check writing text over border
    )
    result = groupme.toc.strategy.load(content=loaded)
    return result


def master72_toc():
    return headlines_frompath(tests.resources.MASTER72, pages=(1, 2))


def bachelor111_toc():
    return headlines_frompath(
        tests.resources.BACHELOR111,
        pages=(1, 2, 3, 4),
    )


def technical24_toc():
    return headlines_frompath(tests.resources.TECHNICAL24, pages=(1))
