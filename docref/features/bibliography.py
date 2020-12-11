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
import utila

import docref.bibliography.parser
import docref.figure
import words.utils


def work(text: str, headlines: str, pages: tuple = None) -> str:
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    text = serializeraw.load_text(text, headlines=headlines, pages=pages)

    parsed = docref.figure.parse_text(
        text,
        pattern=PATTERN,
        compare_content=False,
    )
    parsed = remove_invalid(parsed, text)
    dumped = serializeraw.dump_docref(parsed)
    return dumped


def remove_invalid(items, text):
    lookup = words.utils.sentence_lookup(text)
    result = []
    for item in items:
        sentence = lookup[item.page][item.sentence]
        plain = words.utils.sentence_plain(sentence, item.marked)
        for reference, mark in zip(plain, item.marked):
            if not valid(reference):
                utila.error(f'docref:bib:invalid reference: {reference}')
                continue
            result.append(iamraw.DocRef(item.page, item.sentence, [mark]))
    return result


def valid(item: str):
    return docref.bibliography.parser.parse(item) is not None


PATTERN = (
    '[Hof11, S. 309-311]',
    '[Hof11, S. 314f]',
    '[Mag13]',
    '[RNB12, S. 62ff]',
    '(Fornoff 2016: 53; Erll 2017: 11-12)',
    '(Górny et al. 2012: 14)',
    '(Hahn; Traba 2015: 17)',
    '(Koreik 2010: 1478)',
    '(Robbe 2009: 51-52)',
    '(ebd.: 21; Fornoff 2016: 45-48)',
    '(ebd.: 51)',
    '(ebd.: 51-60)',
    '(ebd: 51-60)',
    '(vgl. Darilek 2014),',
    '(vgl. Darilek 2014b),',
    '(vgl. Defrance; Pfeil 2014; vgl. Frank 2005)',
)
