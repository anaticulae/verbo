# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest

import tests
import words.path

SENTENCE_12 = """Die IKT bildet dabei das Verknüpfungselement und \
ermöglicht eine unternehmensübergreifende Optimierung sämtlicher \
Prozesse entlang der Wertschöpfungskette.\
"""
SENTENCE_13 = """Dadurch wird die Informations- und Kommunikationstechnik \
zu einem zentralen Bestandteil für die Digitalisierung.{{hn:15:nh}}\
"""


@utilotest.nightly
def test_text_extract_p7p8p9(td, mp):
    utilotest.fixture_requires(hoverpower.BACHELOR076_PDF)
    source = hoverpower.link(hoverpower.BACHELOR076_PDF)
    cmd = f'--text  --headlines -i={source} --pages=7,8,9'
    tests.run(cmd, mp=mp)
    text = words.path.text(td.tmpdir)
    headlines = words.path.headlines(td.tmpdir)
    headlines = serializeraw.load_headlines(
        content=headlines,
        pages=(7, 8, 9),
    )
    text = serializeraw.load_text(text, headlines=headlines)
    sentences = []
    for page in text:
        for _, content in page.content:
            sentences.extend(content)
    # Ensure that page is merged correctly
    assert sentences[12] == SENTENCE_12
    # First complete sentence after page break
    assert sentences[13] == SENTENCE_13
