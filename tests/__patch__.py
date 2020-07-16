# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila


def todo(path, pages: str = None) -> tuple:
    """Determine todo entree as input for test data generator."""
    # TODO: REPLACE AFTER UPGRADING POWER
    # TODO: REPLACE WITH HEY APROACH
    pages = ':' if pages is None else pages
    path = utila.forward_slash(path)
    result = (path, pages)
    return result


power.todo = todo


def incremental_todo(resources: list) -> list:
    result = []
    for item in resources:
        try:
            path, _ = item
        except ValueError:
            path = item
        path = power.link(path)
        if not os.path.exists(str(path)):
            utila.debug(f'missing, run generator: {path}')
            result.append(item)
    return result


power.generator.incremental_todo = incremental_todo
