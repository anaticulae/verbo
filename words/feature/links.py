# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import serializeraw


def work(text: str, headlines: str, pages: tuple = None) -> str:
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    texts = serializeraw.load_text(text, headlines, pages=pages)

    processed = process_text(texts)
    dumped = serializeraw.dump_hyperlinks(processed)  # pylint:disable=E1101
    return dumped


def process_text(texts):
    result = []
    for page, sentence in sentences(texts):
        extracted = process_chunk(sentence)
        for item in extracted:
            item.page = page
        result.extend(extracted)
    return result


def process_chunk(sentence):
    result = []
    hyperlinks = german.hyperlink(sentence)
    for hyperlink in hyperlinks:
        result.append(iamraw.ExtractedHyperLink(href=hyperlink))  # pylint:disable=E1101
    return result


def sentences(texts):
    for chunk in texts:
        for section in chunk.content:
            for page, sentence in zip(section.pages, section.content):
                yield page, sentence
