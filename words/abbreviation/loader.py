# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw


def load_text(
        content: str,
        headlines: iamraw.PagesHeadlineList,
        pages=None,
) -> iamraw.PageContentTexts:
    loaded = serializeraw.load_text(content, headlines, pages)
    result = []
    for pagenumber, pagecontent in loaded:
        result.append(
            iamraw.PageContentText(
                page=pagenumber,
                content=pagecontent,
            ))
    return result


def dump_text(text: iamraw.PageContentTexts) -> str:
    converted = [(page.text, page.content) for page in text]
    dumped = serializeraw.dump_text(converted)
    return dumped
