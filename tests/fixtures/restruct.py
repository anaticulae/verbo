# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import iamraw.path
import iamraw.sections
import power
import sections.creator
import sections.feature.chapter
import sections.feature.index
import sections.feature.section
import sections.feature.toc
import sections.feature.whitepage
import serializeraw

import words.feature
import words.feature.boxed
import words.feature.headlines
import words.feature.list
import words.headlines
import words.loader.input
import words.text
import words.text.chapter


def restructured_sections():
    extracted = sections.feature.section.extract_sections_frompath(
        power.link(power.DOCU27_PDF))
    dumped = serializeraw.dump_sections(extracted)
    return dumped


def restructured_headlines():
    sections_ = restructured_sections()
    source = power.link(power.DOCU27_PDF)

    dumped = words.feature.headlines.work(
        sectionlist=sections_,
        text=iamraw.path.text(source),
        text_position=iamraw.path.textposition(source),
        font_header=iamraw.path.fontheader(source),
        font_content=iamraw.path.fontcontent(source),
        sizeandborder=iamraw.path.sizeandborder(source),
        boxes=iamraw.path.boxed(source),
        headerfooters=iamraw.path.headerfooters(source),
    )
    return dumped


def restructured_sections_manual() -> iamraw.sections.Sections:
    result = iamraw.sections.Sections()

    def analyse(section, start, end):
        return section(result, start, end, iamraw.sections.PERCENT_100)
        # TODO: reactivate [start, START] later
        # return section(result, [start, START], [end, END], iamraw.sections.PERCENT_100)

    def add_children(parent, ctor, start, end):
        # new = ctor(parent, [start, START], [end, END], PERCENT_100)
        new = ctor(parent, start, end, iamraw.sections.PERCENT_100)
        return new

    # Page, Start
    # Intro
    intro = analyse(sections.creator.add_introduction, 0, 1)
    add_children(intro, sections.creator.add_title, 0, 0)
    add_children(intro, sections.creator.add_whitepage, 1, 1)

    # First pages with tables
    table_first = analyse(sections.creator.add_table, 2, 5)
    add_children(table_first, sections.creator.add_toc, 2, 2)
    add_children(table_first, sections.creator.add_whitepage, 3, 3)
    add_children(table_first, sections.creator.add_text, 4, 4)
    add_children(table_first, sections.creator.add_whitepage, 5, 5)

    # Content starts here
    content = analyse(sections.creator.add_content, 6, 25)
    sections.creator.add_chapter(content, 6, 7, number=1)
    sections.creator.add_chapter(content, 8, 9, number=2)
    sections.creator.add_chapter(content, 10, 11, number=3)
    sections.creator.add_chapter(content, 12, 17, number=4)
    sections.creator.add_chapter(content, 18, 19, number=5)
    sections.creator.add_chapter(content, 20, 21, number=6)
    sections.creator.add_chapter(content, 22, 23, number=7)
    sections.creator.add_chapter(content, 24, 25, number=8)

    # Second pages with table
    table_second = analyse(sections.creator.add_table, 26, 26)
    add_children(table_second, sections.creator.add_index, 26, 26)

    return result


def restruct_resources():
    headlines = restructured_headlines()
    loaded = words.feature.load_resources(
        text=iamraw.path.text(power.link(power.DOCU27_PDF)),
        textposition=iamraw.path.textposition(power.link(power.DOCU27_PDF)),
        fontheader=iamraw.path.fontheader(power.link(power.DOCU27_PDF)),
        fontcontent=iamraw.path.fontcontent(power.link(power.DOCU27_PDF)),
        headlines=headlines,
        pagesizes=iamraw.path.sizeandborder(power.link(power.DOCU27_PDF)),
        headerfooters=iamraw.path.headerfooters(power.link(power.DOCU27_PDF)),
        boxes=iamraw.path.boxed(power.link(power.DOCU27_PDF)),
        lists=words.path.lists(power.link(power.DOCU27_PDF)),
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
    headlines = restructured_headlines()
    undefined = serializeraw.dump_text(restructured_textexample())
    extracted, _ = words.loader.input.load_resources(
        undefined,
        iamraw.path.text(power.link(power.DOCU27_PDF)),
        iamraw.path.textposition(power.link(power.DOCU27_PDF)),
        border=iamraw.path.sizeandborder(power.link(power.DOCU27_PDF)),
        headlines=headlines,
        headerfooters=iamraw.path.headerfooters(power.link(power.DOCU27_PDF)),
    )
    boxes = serializeraw.load_boxes(
        iamraw.path.boxed(power.link(power.DOCU27_PDF)))
    result = words.feature.boxed.process_content(extracted, boxes)
    return result


def restructured_list_work():
    headlines = restructured_headlines()
    undefined = serializeraw.dump_text(restructured_textexample())

    extracted, contentborder = words.loader.input.load_resources(
        undefined,
        iamraw.path.text(power.link(power.DOCU27_PDF)),
        iamraw.path.textposition(power.link(power.DOCU27_PDF)),
        headlines=headlines,
        border=iamraw.path.sizeandborder(power.link(power.DOCU27_PDF)),
        headerfooters=iamraw.path.headerfooters(power.link(power.DOCU27_PDF)),
    )
    worker = functools.partial(
        words.feature.list.process_page,
        contentborder=contentborder,
    )
    result = words.loader.input.process_input(
        extracted,
        worker,
    )
    return result
