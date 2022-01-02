# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.sections

import words.headlines.utils


def test_headlines_determine_contentrange():
    sections = iamraw.Sections(content=[
        iamraw.MultipleSection(
            start=0,
            end=3,
            trust=1.0,
            content=[
                iamraw.sections.Bibliography(start=0.0, end=0.5, trust=1.0),
                iamraw.sections.TitlePage(start=0.5, end=1.0, trust=1.0),
                iamraw.sections.Text(start=1, end=1, trust=1.0),
                iamraw.sections.Text(start=2, end=2, trust=1.0)
            ])
    ])
    contentrange = words.headlines.utils.determine_contentrange(sections)

    # TODO: CHECK (1, 1)
    expected = [(0.0, 0.5), (0.5, 1.0), (1, 1), (2, 3)]
    assert contentrange == expected
