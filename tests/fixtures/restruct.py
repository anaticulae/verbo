# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.path
import iamraw.sections
import power
import serializeraw
import utilatest

import words.feature
import words.feature.boxed
import words.feature.headlines
import words.headlines
import words.loader
import words.text
import words.text.chapter


def restructured_sections():
    utilatest.fixture_requires(power.DOCU027_PDF)
    source = iamraw.path.sections_(power.link(power.DOCU027_PDF))
    extracted = serializeraw.load_sections(source)
    dumped = serializeraw.dump_sections(extracted)
    return dumped


def restructured_headlines():
    sections_ = restructured_sections()
    src = power.link(power.DOCU027_PDF)
    dumped, _ = words.feature.headlines.work(
        sectionlist=sections_,
        textx=iamraw.path.text(src),
        text_position=iamraw.path.textposition(src),
        font_header=iamraw.path.fontheader(src),
        font_content=iamraw.path.fontcontent(src),
        oneline_text=iamraw.path.text(src, prefix='oneline'),
        oneline_text_position=iamraw.path.textposition(src, prefix='oneline'),
        oneline_font_header=iamraw.path.fontheader(src, prefix='oneline'),
        oneline_font_content=iamraw.path.fontcontent(src, prefix='oneline'),
        sizeandborder=iamraw.path.sizeandborder(src),
        boxes=iamraw.path.boxed(src),
        headerfooters=iamraw.path.headerfooters(src),
    )
    return dumped


def restruct_resources():
    utilatest.fixture_requires(power.DOCU027_PDF)
    headlines = restructured_headlines()
    source = power.link(power.DOCU027_PDF)
    loaded = words.feature.load_resources(
        text=iamraw.path.text(source),
        textposition=iamraw.path.textposition(source),
        fontheader=iamraw.path.fontheader(source),
        fontcontent=iamraw.path.fontcontent(source),
        headlines=headlines,
        pagesizes=iamraw.path.sizeandborder(source),
        headerfooters=iamraw.path.headerfooters(source),
        boxes=iamraw.path.boxed(source),
        lists=words.path.lists(source),
    )
    return loaded


def restructured_textexample(require_headlinelevel: bool = True):
    loaded = restruct_resources()
    extracted = words.text.chapter.extract_texts(
        loaded,
        require_headlinelevel=require_headlinelevel,
    )
    assert extracted is not None
    return extracted


def restructured_boxed():
    source = power.link(power.DOCU027_PDF)
    headlines = restructured_headlines()
    undefined = serializeraw.dump_text(restructured_textexample())
    extracted, _ = words.loader.load_resources(
        undefined,
        iamraw.path.text(source),
        iamraw.path.textposition(source),
        border=iamraw.path.sizeandborder(source),
        headlines=headlines,
        headerfooters=iamraw.path.headerfooters(source),
    )
    boxes = serializeraw.load_boxes(iamraw.path.boxed(source))
    result = words.feature.boxed.process_content(extracted, boxes)
    return result
