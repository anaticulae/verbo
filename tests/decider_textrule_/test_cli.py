# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests.decider_textrule_


def test_decider_textrule_run(monkeypatch):
    """Run help and version command to reach basic test coverage"""
    cmd = '--help'
    tests.decider_textrule_.run(cmd, monkeypatch=monkeypatch)
