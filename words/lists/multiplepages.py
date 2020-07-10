# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Multiple Page List Extractor
============================

This strategy is required to parse lists which are very long and
expanded over multiple pages. If the content of some list steps is so
huge, that only one content line is on the page, it is very
hard/impossible to detect this as a valid lists, cause most of the
strategies expect more than one list item on a page. Furthermore it is
hard to distinguish between lists and headlines.
"""
