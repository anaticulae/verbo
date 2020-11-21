# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import tests
import words.path


def test_links_master75(testdir, monkeypatch):
    # TODO: MASTER&% TEXT SECTION EXTRACTION IS BROKEN
    cmd = f'-i {power.link(power.MASTER075_PDF)} --links'
    tests.run(cmd, monkeypatch=monkeypatch)

    loaded = serializeraw.load_hyperlinks(words.path.links(testdir.tmpdir))  # pylint:disable=E1101

    for item in loaded:
        print(item)

    assert len(loaded) == 22
