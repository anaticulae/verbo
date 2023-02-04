# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import genex
import power
import pytest
import serializeraw
import utila
import utilatest

# TODO: Reduce list of unsupported documents
# this documents does not passes the current implementation
UNSUPPORTED_DOCUMENTS = {
    'paper/page_10_double_column_with_tables.pdf',
    'paper/page_6_double_column.pdf',
    'paper/page_6_double_column_with_math.pdf',
    'book/leftright.pdf',
}

# yapf:disable
EXPECTED_FAILURE = {
    # 'docu/twine.pdf': 'font extracting problem',
    'howto_argparse/howto_argparse.pdf': 'not every headlines can be detected',
    'bachelor/bachelor085.pdf': 'all content is detected as figure(pdf printer error)',
    # ambigous sections, groupme works, words does not work
    # 'order/howtowrite_pages9.pdf': 'headline detection does not works correctly',
}
# yapf:enable

SKIP_DOCUMENTS = {
    'bachelor/page_111_images_toc.pdf',
    'bachelor/page_159_huge_appendix.pdf',
    'bachelor/page_37_tables.pdf',
    'bachelor/page_56_hard_to_read.pdf',
    'bachelor/page_63_images_toc.pdf',
    'docu/howto_argparse.pdf',
    'docu/twine.pdf',
    'docu/vimguide.pdf',
    'homework/page_40_images_toc.pdf',
    'homework/page_50_math.pdf',
    'master/page_116_images_toc_formular.pdf',
    'master/page_72_noimages_toc.pdf',
    'master/page_78_images_toc.pdf',
    'master/page_83_noimages_toc.pdf',
    'master/page_89_noimages_toc.pdf',
    'order/howtowrite_pages9.pdf',
    # requires to much required test time
    'order/page_38.pdf',
    'technical/page_24_color_figures_images.pdf',
}

HEADLINE_COUNT = {
    'howto_argparse/howto_argparse.pdf': 7,  # 9 with subsections
}


def params():
    pdf = power.PDF
    # skip documents cause of to few computing power
    ignore = SKIP_DOCUMENTS | UNSUPPORTED_DOCUMENTS
    pdf = [
        item for item in pdf if all([
            not utila.make_relative(item, power.REPO) in ignore,
            # skip generated pdfs to avoid double work
            not 'notitle' in item,
        ])
    ]
    # select 5 items to reduce required test power
    # random is not good when reproducing an error, may use it later.
    pdf = pdf[0:5]
    result = []

    def determine_mark(pdf):
        relative = utila.make_relative(pdf, power.REPO)
        if relative in UNSUPPORTED_DOCUMENTS:
            return pytest.mark.xfail(
                reason="unsupported font format with current impl",)
        with contextlib.suppress(KeyError):
            return pytest.mark.xfail(reason=EXPECTED_FAILURE[relative])
        return pytest.mark.huge

    for item in pdf:
        double = pytest.param(
            (
                item,
                '--char_margin 100.0 --boxes_flow 1.0',
                '--char_margin 5.0 --boxes_flow 1.0 --line_margin 0.3',
            ),
            id=utila.file_name(item),
            marks=determine_mark(item),
        )
        result.append(double)
    return result


@utilatest.monday
@pytest.mark.parametrize('source', params())
def test_huge_running_words(source, td, request):  # pylint:disable=W0621
    """Run rawmaker -> sections -> headlines -> words.

    Ensure that this chain works for huge pdf example provided by power
    tool.
    """
    testfile = request.node.name.split('[')[1].split(']')[0]
    expected_headlines = HEADLINE_COUNT.get(testfile, 0)
    source = source[0]
    genex.extract(
        files=[source],
        dest=td.tmpdir,
        groupme=True,
        headlines=True,
        sections=True,
        words=True,
        lists=True,
        headnote=True,
        footnote=True,
        pagenumber=True,
        cleanup=True,
    )
    filename = utila.file_name(power.link(source))
    directory = td.tmpdir.join(filename)
    headlines = serializeraw.load_headlines(directory)
    headlines: list = utila.flat(headlines)
    if expected_headlines:
        assert len(headlines) == expected_headlines, headlines
