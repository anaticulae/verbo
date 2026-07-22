# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import utilotest

import words.feature
import words.text.chapter


def headlines() -> str:
    source = hoverpower.link(hoverpower.DOCU027_PDF)
    result = iamraw.path.words_headlines(source)
    return result


def resources():
    utilotest.fixture_requires(hoverpower.DOCU027_PDF)
    source = hoverpower.link(hoverpower.DOCU027_PDF)
    loaded = words.feature.load_resources(
        text=iamraw.path.text(source),
        textposition=iamraw.path.textposition(source),
        fontheader=iamraw.path.fontheader(source),
        fontcontent=iamraw.path.fontcontent(source),
        headlines=iamraw.path.words_headlines(source),
        pagesizes=iamraw.path.sizeandborder(source),
        headerfooters=iamraw.path.headerfooters(source),
        boxes=iamraw.path.boxed(source),
        lists=words.path.lists(source),
    )
    return loaded


def textexample(require_headlinelevel: bool = True):
    loaded = resources()
    extracted = words.text.chapter.extract_texts(
        loaded,
        require_headlinelevel=require_headlinelevel,
    )
    assert extracted is not None
    return extracted
