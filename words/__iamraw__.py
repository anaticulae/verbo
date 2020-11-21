# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import typing

import iamraw
import serializeraw
import utila
import yaml


@dataclasses.dataclass
class ExtractedHyperLink:
    href: str = None
    visited: str = None
    page: int = None
    raw: str = None


ExtractedHyperLinks = typing.List[ExtractedHyperLink]

iamraw.ExtractedHyperLink = ExtractedHyperLink
iamraw.ExtractedHyperLinks = ExtractedHyperLinks


def dump_hyperlinks(links: ExtractedHyperLinks) -> str:
    result = []
    for hyperlink in links:
        result.append(dataclasses.asdict(hyperlink))
    dumped = yaml.safe_dump(result)
    return dumped


def load_hyperlinks(content: str, pages: tuple = None) -> ExtractedHyperLinks:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.safe_load(content)
    result = []
    for item in loaded:
        hyperlink = iamraw.ExtractedHyperLink(**item)
        if utila.should_skip(hyperlink.page, pages):
            continue
        result.append(hyperlink)
    return result


serializeraw.dump_hyperlinks = dump_hyperlinks
serializeraw.load_hyperlinks = load_hyperlinks
