# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw
import iamraw.sections
import sections.feature.section
import texmex
import utila


def document_textdistance(
        navigators: texmex.PageTextContentNavigators,
        digits: int = 1,
) -> float:
    """Determine the most common text distance"""
    result = []
    for navigator in navigators:
        if not navigator:
            # empty page
            continue
        bounds = texmex.textbounds(navigator, navigator.content)
        # ignore empty content
        bounds = [item.bounds for item in bounds if item.text.strip()]
        ydist = [item.bottomdist for item in bounds]
        for yfirst, ysecond in zip(ydist[:-1], ydist[1:]):
            distance = yfirst - ysecond
            result.append(distance)
    result = utila.roundme(result, digits=digits, convert=False)  # pylint:disable=R0204
    mode = utila.mode(result)
    return mode


def prepare_chapter_and_content(sections_, chapter):
    assert isinstance(sections_, iamraw.Sections)
    assert sections_, 'no sections provided'
    if chapter is None:
        # process all chapter
        # TODO: clearify code
        content = determine_contentrange(sections_)
        chapter = list(range(len(content)))
    else:
        content = sections.feature.section.chapters(sections_)
        chapter = [chapter] if isinstance(chapter, int) else chapter
    return chapter, content


def determine_contentrange(items) -> 'words.headlines.ChapterRanges':
    """Iterate thrue `sections` and search for `Chapter` to determine
    section start and end.

    In some cases no `Chapter` is present. This can happen if you
    analyse only a few pages or a single one. In this case the start and
    end is defined by normal items.

    Returns:
        list of `ChapterRange` (start, end)
    """
    # analyze all chapter of the document
    contents = [
        item for item in items if isinstance(
            item,
            (
                iamraw.MainPart,
                iamraw.MultipleSection,
                iamraw.sections.Appendix,
                iamraw.sections.Unknown,
            ),
        )
    ]
    chapters = flat_chapters(contents)

    if not chapters and contents:
        # no chapter is present - create `virtual chapter`
        chapters = [[item for item in content.content] for content in contents]
        chapters = utila.flatten(chapters)
    if not chapters:
        # TODO: INVESTIGATE HERE
        return []
    result = items_before_firstchapter(chapters, contents)
    for current, after in zip(chapters[:-1], chapters[1:]):
        floatrange = isinstance(current.end, float) or isinstance(after.start, float) # yapf:disable
        if current.end == after.start and floatrange:
            # multi page: content on same page
            result.append((current.start, current.end))
        else:
            result.append((current.start, after.start - 1))
    result.append((chapters[-1].start, contents[-1].end))
    # ensure ascending page numbers
    assert all([start <= end for start, end in result]), str(result)
    return result


def flat_chapters(contents):
    result = []
    for item in contents:
        if isinstance(item, iamraw.MainPart):
            result.extend(item.content)
        elif isinstance(item, iamraw.sections.Appendix):
            result.append(item)
    result = utila.select_type(
        result,
        (iamraw.sections.Chapter, iamraw.sections.Appendix),
    )
    return result


def items_before_firstchapter(chapters, contents):
    """Determine items before the first **loaded** chapter starts.

    This is required, when loading a part in the middle of a document.
    To extract headlines, it is required to have `Chapter` separators to
    determine the range of the different chapter. Parts of chapter are
    not loaded if start of chapter is not selected.
    """
    assert chapters
    # check if content exists before the first chapter starts
    firstchapter_start = chapters[0].start
    before = [[
        item for item in content.content if item.start < firstchapter_start
    ] for content in contents]
    # remove empty pages
    before = [item for item in before if item]
    before = utila.flatten(before)
    if not before:
        return []
    return [(before[0].start, before[-1].end)]


def groupby_headlinelevel(chapters):
    extracted = [item for item in chapters.values()]

    flatten = utila.flatten(extracted)
    grouped = []
    if flatten:
        if isinstance(flatten[0].level, dict):
            # HACK NOLEVEL?
            flatten[0].level = None
        grouped.append([flatten[0]])
    for item in flatten[1:]:
        if isinstance(item.level, dict):
            # HACK NOLEVEL?
            item.level = None
        if item.level is None or item.level == 1:
            grouped.append([item])
        else:
            grouped[-1].append(item)
    return grouped


# TODO: CODE DUPLICATION, COLLECT DIFFERENT HEADLINE PARSING APPROACHES
# AND CONVERT TO SINGLE ONE.
HEADLINE = re.compile(
    ('^'
     r'(?P<level>(\d{1,2}\.?)+\d{0,2})'
     r'[ ]{1,5}'
     r'(?P<text>.+?)'
     '$'),
    re.VERBOSE,
)


def parse_headline(line):
    line = line.strip()
    return re.match(HEADLINE, line)
