# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import tests
import words.path


# TODO: MOVE TO TEXMEX
@pytest.mark.xfail(reason='hyperlink merger requires \n at line end')
@utilatest.requires(power.MASTER075_PDF)
def test_links_master75(td, mp):
    # TODO: MASTER75 TEXT SECTION EXTRACTION IS BROKEN
    loaded = hyperlinks(power.MASTER075_PDF, td, mp)
    assert len(loaded) == 22


@utilatest.requires(power.MASTER075_PDF)
def test_links_master75pages15(td, mp):
    loaded = hyperlinks(power.MASTER075_PDF, td, mp, 15)
    assert len(loaded) == 1
    hyperlink = loaded[0].href
    assert hyperlink.startswith('https')
    assert hyperlink.endswith('index.html')
    assert loaded[0].visited


def hyperlinks(source, td, mp, pages=':'):
    cmd = f'-i {power.link(source)} --links --pages={pages}'
    tests.run(cmd, mp=mp)
    loaded = serializeraw.load_hyperlinks(words.path.links(td.tmpdir))  # pylint:disable=e1101
    return loaded
