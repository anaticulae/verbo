# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator
import statistics

import configo
import doctextstyle.cluster
import doctextstyle.features
import doctextstyle.parser
import doctextstyle.utils
import groupme.toc.group
import groupme.toc.strategy
import iamraw
import utila

HEADLINES_COUNT_MIN = configo.HV_INT_PLUS(5).value

MAX_LEVELFOUR_PER_PAGE = configo.HV_INT_PLUS(4).value


def headlines(ptns):  # pylint:disable=R0914
    # TODO: MOVE TO DOCTEXTSTYLE?
    parsed = doctextstyle.parser.parses(ptns)
    flat = doctextstyle.utils.flatten(parsed)
    text = doctextstyle.features.text(flat)

    textsize, textfont = text[0], text[1]

    # remove too small text size
    flat = [item for item in flat if item.size >= textsize]
    # remove non textual items
    flat = [item for item in flat if item.font != textfont]
    # test if some data is left
    if not flat:
        return []
    # left adjusted text
    left = utila.mode([item.left for item in flat])
    flat = [item for item in flat if utila.near(left, item.left, diff=5.0)]
    # headlines often/always have a distance before and after
    flat = [item for item in flat if item.after is None or item.after >= 10.0]
    flat = [item for item in flat if item.before is None or item.before >= 10.0]
    # remove numbered headlines
    flat = [
        item for item in flat
        if groupme.toc.group.numbered_level(item.hashed) is None
    ]
    clusters = doctextstyle.cluster.cluster(
        flat,
        selection=(
            doctextstyle.cluster.ClusterProperty.SIZE,
            doctextstyle.cluster.ClusterProperty.FONT,
        ),
        minsize=HEADLINES_COUNT_MIN,
    )
    paged = grouped(parsed)
    best = select_best(clusters, paged)
    result = []
    for item in best:
        current = page_and_container(item, paged)
        if current is None:
            utila.error(f'could not find {item}')
            continue
        page, container = current
        headline = iamraw.Headline(
            container=container,
            level=4,
            page=ptns[page].page,
            raw=item.hashed,
            title=item.hashed,
        )
        result.append(headline)
    result = sorted(result, key=operator.attrgetter('page', 'container'))
    if tomany_headlines_perpage(result):
        # disable feature if too many items detected
        return []
    return result


def tomany_headlines_perpage(result: list) -> bool:
    pages = sorted([item.page for item in result])
    if not pages:
        return False
    pages = utila.groupby_diff(pages, diff=0)
    maxpage = len(utila.longest(pages, number=1))
    if maxpage > MAX_LEVELFOUR_PER_PAGE:
        return True
    return False


MIN_LEVELFOUR_WORD_COUNT_DIFF = configo.HV_FLOAT_PLUS(0.7).value
MAX_LEVELFOUR_WORD_COUNT_DIFF = configo.HV_FLOAT_PLUS(1.3).value


def valid_levelfour(extracted, levelfour) -> bool:
    """Disable potential levelfour headlines which seem out of range by
    word count."""
    if not extracted:
        return False
    if not levelfour:
        return False

    extracted = utila.flatten(extracted)
    headline_words = (len(headline.title.split()) for headline in extracted)
    levelfour_words = (len(headline.title.split()) for headline in levelfour)

    mean = statistics.mean(headline_words)
    mean_levelfour = statistics.mean(levelfour_words)

    # valid range
    lower_bound = mean * MIN_LEVELFOUR_WORD_COUNT_DIFF
    upper_bound = mean * MAX_LEVELFOUR_WORD_COUNT_DIFF
    return lower_bound <= mean_levelfour <= upper_bound


# TODO: DIRTY BUT WORKS


def select_best(clusters, paged) -> list:
    result = []
    for cluster in clusters:
        pages = pageclusters(cluster, paged)
        quote = len(set(pages)) / len(pages)
        if quote < 0.5:
            continue
        if len(pages) < 8:
            continue
        result.append(cluster)
    result = sorted(result, key=len, reverse=True)
    # select largest cluster
    result = result[0] if result else []
    return result


def pageclusters(cluster, paged):
    result = []
    for item in cluster:
        page, _ = page_and_container(item, paged)
        result.append(page)
    return sorted(result)


def page_and_container(selected, parsed):
    for page, content in enumerate(parsed):
        for index, item in enumerate(content):
            if selected != item:
                continue
            return page, index
    return None


def grouped(pages: iamraw.PageTextPropertiesList) -> iamraw.TextProperties:
    result = []
    for page in pages:
        collected = []
        for length, hashed, size, font, distance, ypos, left, right in zip(
                page.length,
                page.hashed,
                page.sizes,
                page.fonts,
                page.distances,
                page.ypos,
                page.left,
                page.right,
        ):
            collected.append(
                iamraw.TextProperty(
                    length=length,
                    hashed=hashed,
                    size=size,
                    font=font,
                    before=distance.top,
                    after=distance.bottom,
                    top=ypos[0],
                    bottom=ypos[1],
                    left=left,
                    right=right,
                    page=page.page,
                ))
        result.append(collected)
    return result
