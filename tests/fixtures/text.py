# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import power

import words.feature


@configo.cache_small
def bachelor051_textrequired(pages=None):
    return words.feature.load_resources_frompath(
        power.link(power.BACHELOR051_PDF),
        pages=pages,
    )
