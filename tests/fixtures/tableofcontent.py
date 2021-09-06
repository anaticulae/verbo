# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.toc.strategy
import power
import serializeraw


def headlines_frompath(path: str, pages=None, prefix='oneline'):
    loaded = serializeraw.ptcn_frompath(
        path,
        pages=pages,
        prefix=prefix,
        validate_leftright=False,  # do not check writing text over border
    )
    result = groupme.toc.strategy.load(content=loaded)
    return result


def master72_toc():
    return headlines_frompath(power.link(power.MASTER072_PDF), pages=(1, 2))
