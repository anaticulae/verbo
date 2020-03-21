# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# pylint:disable=W0611
from tests.fixtures.restruct import restructured_boxed
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_textexample
from tests.fixtures.restruct import restructured_textexample_dumped
from words.feature.boxed import dump_boxedcontent
from words.feature.boxed import load_boxedcontent


def test_boxed_work(
        # pylint:disable=W0621
        restructured_boxed):
    dumped = dump_boxedcontent(restructured_boxed)
    assert len(dumped) > 2000, str(dumped)


def test_boxed_dump_and_load(
        # pylint:disable=W0621
        restructured_boxed):
    dumped = dump_boxedcontent(restructured_boxed)

    loaded = load_boxedcontent(dumped)
    assert loaded == restructured_boxed
