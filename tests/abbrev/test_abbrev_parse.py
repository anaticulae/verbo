# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilo

import tests
import words.path


def abbr(source, pages, td, mp, flat: bool = False):
    source = hoverpower.link(source)
    cmd = f'-i {source} -o {td.tmpdir} --abbreviation --pages={pages}'
    tests.run(cmd, mp=mp)
    abbrpath = words.path.abbr(td.tmpdir)
    result = serializeraw.load_text_abbreviations(abbrpath)
    if flat:
        result = [[item.short for item in page.content] for page in result]
        result = utilo.flat(result)
        result = utilo.unique(result)
    return result


BACHELOR37 = utilo.splititems("""AG ANOVA BP BPM CD CX EKG EN ENBP FMRI IAPS \
IL MA MD MATLAB MDHF PASW PET PFC RS SAM SD SEM SPSS HF US USA al. bzw. ca. \
etc. s. \u2212md
""")


@pytest.mark.xfail(reason='???')
def test_bachelor37abbr(td, mp):
    extracted = abbr(hoverpower.BACHELOR037_PDF, '5:33', td, mp, True)
    extracted = sorted(utilo.lower(*extracted))
    expected = sorted(BACHELOR37)
    assert extracted == expected
