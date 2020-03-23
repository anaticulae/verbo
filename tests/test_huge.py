# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import pytest
import serializeraw
import utila

import tests
import words

# TODO: Reduce list of unsupported documents
# this documents does not passes the current implementation
UNSUPPORTED_DOCUMENTS = {
    'paper/page_10_double_column_with_tables.pdf',
    'paper/page_6_double_column.pdf',
    'paper/page_6_double_column_with_math.pdf',
    'book/leftright.pdf',
}

EXPECTED_FAILURE = {  # yapf:disable
    # 'docu/twine.pdf': 'font extracting problem',
    'howto_argparse/howto_argparse.pdf': 'not every headlines can be detected',
    # ambigous sections, groupme works, words does not work
    # 'order/howtowrite_pages9.pdf': 'headline detection does not works correctly',
}

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
    pdf = tests.pdfs()
    # skip documents cause of to few computing power
    ignore = SKIP_DOCUMENTS | UNSUPPORTED_DOCUMENTS
    pdf = [
        item for item in pdf if all([
            not tests.relative_path(item) in ignore,
            # skip generated pdfs to avoid double work
            not 'notitle' in item,
        ])
    ]
    # select 5 items to reduce required test power
    # random is not good when reproducing an error, may use it later.
    pdf = pdf[0:5]
    result = []

    def determine_mark(pdf):
        relative = tests.relative_path(pdf)
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
            id=tests.relative_path(item),
            marks=determine_mark(item),
        )
        result.append(double)
    return result


@pytest.fixture(params=params())
def rawresult(request, tmpdir):
    tmpdir = str(tmpdir)
    tocpath = os.path.join(tmpdir, 'toc')
    generalpath = os.path.join(tmpdir, 'general')
    for item in [tocpath, generalpath]:
        os.makedirs(item)

    pdf, toccmd, generalcmd = request.param
    rawtoc = f'rawmaker -i {pdf} -j=8 --pages=0:20 -o {tocpath} --prefix=oneline {toccmd}'
    rawgeneral = f'rawmaker -i {pdf} -j=8 --pages=0:20 -o {generalpath} {generalcmd}'
    linero = f'linero -o {generalpath}'

    completed = utila.run(rawtoc)
    assert completed.returncode == utila.SUCCESS, str(completed)

    completed = utila.run(rawgeneral)
    assert completed.returncode == utila.SUCCESS, str(completed)

    completed = utila.run(linero)
    assert completed.returncode == utila.SUCCESS, str(completed)

    return (tmpdir, tocpath, generalpath)


@pytest.fixture
def groupme(rawresult):  # pylint:disable=W0621
    tmpdir, tocpath, generalpath = rawresult

    groupmepath = os.path.join(tmpdir, 'groupme')
    os.makedirs(groupmepath)

    runme = 'groupme -i %s -i %s -o %s -j=8'
    runme = runme % (generalpath, tocpath, groupmepath)

    completed = utila.run(runme)
    assert completed.returncode == utila.SUCCESS, str(completed)
    return (tmpdir, tocpath, generalpath, groupmepath)


@pytest.fixture
def sections_result(groupme):  # pylint:disable=W0621
    tmpdir, tocpath, generalpath, groupmepath = groupme

    sectionspath = os.path.join(tmpdir, 'sections')
    os.makedirs(sectionspath)

    runme = 'sections -i %s -i %s -i %s -o %s -j=8'
    runme = runme % (generalpath, tocpath, groupmepath, sectionspath)

    completed = utila.run(runme)
    if completed.returncode != utila.SUCCESS:
        utila.log(completed.stdout)
        utila.log(completed.stderr)
    assert completed.returncode == utila.SUCCESS
    return (tmpdir, tocpath, generalpath, sectionspath, groupmepath)


@pytest.fixture
def words_result(sections_result):  # pylint:disable=W0621
    tmpdir, tocpath, generalpath, sectionspath, groupmepath = sections_result

    wordspath = os.path.join(tmpdir, 'words')
    os.makedirs(wordspath)

    runme = 'words -i %s -i %s -i %s -o %s -j=8'
    runme = runme % (generalpath, sectionspath, groupmepath, wordspath)

    completed = utila.run(runme)
    if completed.returncode:
        utila.error((utila.format_completed(completed)))
    assert completed.returncode == utila.SUCCESS

    files = [
        ('words__word_result.yaml', 2000),
        ('words__headlines_headlines.yaml', 380),
    ]
    for item, expected_length in files:
        path = os.path.join(wordspath, item)
        content = utila.file_read(path)
        assert len(content) > expected_length, content

    return (tmpdir, tocpath, generalpath, sectionspath, wordspath)


@utila.skip_longrun
def test_huge_sections_extractor(testdir, sections_result):  # pylint:disable=W0621
    assert sections_result


@utila.skip_longrun
@pytest.mark.usefixtures('testdir')
def test_huge_running_words(words_result, request):  # pylint:disable=W0621
    """Run rawmaker -> sections -> words. Ensure that this chain works for
    huge pdf example provided by power tool."""
    testfile = request.node.name.split('[')[1].split(']')[0]
    expected_headlines = HEADLINE_COUNT.get(testfile, 0)

    headlines = serializeraw.load_headlines(
        os.path.join(
            words_result[4],
            words.WORDS_HEADLINES,
        ))
    headlines = utila.flatten(headlines)

    if expected_headlines:
        assert len(headlines) == expected_headlines, headlines


@utila.skip_longrun
@pytest.mark.usefixtures('groupme')
@pytest.mark.usefixtures('testdir')
def test_huge_running_groupme():
    """Run rawmaker > groupme"""
