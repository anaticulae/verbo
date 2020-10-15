# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilatest

import tests.fixtures.master72.seventytwo as fseventytwo
import words.text.chapter


@utilatest.longrun
def test_text_chapter_split_page2():
    # ensure that empty headline is inserted at page start
    required = fseventytwo.textrequired(pages=(4))
    splitted = words.text.chapter.split(required)
    assert len(splitted) == 1, str(splitted)  # ensure to have one page 4
    secondpage = splitted[0]
    assert secondpage
    firstsection = secondpage.content[0]
    assert firstsection.headline.title is None, firstsection.headline.title
    assert firstsection.headline.page == 4, str(firstsection.headline)

    # 2 headline sections on page
    # first empty none-section, than second `1.1 Fragestellung und Zielsetzung`
    assert len(secondpage.content) == 2, secondpage.content
