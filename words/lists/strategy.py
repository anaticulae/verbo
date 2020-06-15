# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import texmex

import words.lists.geometry
import words.lists.vertical


def extract_lists(ptcns, headlines):
    textfeed = texmex.document_textfeed(ptcns)

    result = []
    for navigator in ptcns:
        pageslist = []

        geo = words.lists.geometry.analyze_page(navigator, headlines, textfeed)
        vertical = words.lists.vertical.analyze_page(navigator)

        # TODO: CHOOSE BETTER SELECTOR
        selected = geo if len(geo) > len(vertical) else vertical

        for lists in selected:
            # TODO: REPLACE 0,0 with correct one
            pageslist.append((0, 0, lists))
        if not pageslist:
            continue
        result.append([navigator.page, pageslist, len(navigator)])
    return result
