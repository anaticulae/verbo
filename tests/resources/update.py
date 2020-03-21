# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import concurrent.futures
import os

import detector.feature.titlepage
import utila

import tests.resources
import words

WORKER = 12


def install_requirements():
    utila.clean_install(words.ROOT, words.PACKAGE)


def sync_resources():
    completed = utila.run('power --all', tests.resources.RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


def extract_examples():
    if os.path.exists(tests.resources.GENERATED):
        return
    extract()
    extract_without_titlepage()


# yapf:disable
PACKAGE = [
    # (tests.resources.BACHELOR111_PDF, tests.resources.BACHELOR111, None),
    (tests.resources.BACHELOR37_PDF, tests.resources.BACHELOR37, '0:30'),
    # (tests.resources.BACHELOR63_PDF, tests.resources.BACHELOR63, '0,1,2,3,4,5,6,7,8,59,60,61'),
    # (tests.resources.HOWTO_ARGPARSE_PDF, tests.resources.HOWTO_ARGPARSE, None),
    (tests.resources.HOWTO_PYPORTING_PDF, tests.resources.HOWTO_PYPORTING, None),
    # (tests.resources.LEFTRIGHT_PDF, tests.resources.LEFTRIGHT, None),
    (tests.resources.MASTER72_PDF, tests.resources.MASTER72, None),
    (tests.resources.PYPORTING_PDF, tests.resources.PYPORTING, None),
    (tests.resources.RESTRUCT_PDF, tests.resources.RESTRUCT, None),
    # (tests.resources.TECHNICAL24_PDF, tests.resources.TECHNICAL24, None),
    # (tests.resources.TWINE_PDF, tests.resources.TWINE, None),
]
# SINGLE = [
#     (tests.resources.BACHELOR56_PDF, tests.resources.BACHELOR56, '0:55'),
#     (tests.resources.HOMEWORK50_PDF, tests.resources.HOMEWORK50, '6'),
#     (tests.resources.HOWTOWRITE9_PDF, tests.resources.HOWTOWRITE9, '0:10'),
#     (tests.resources.MASTER116_PDF, tests.resources.MASTER116, '0,1,2,3,4,96,97,98,99,100'),
#     (tests.resources.MASTER89_PDF, tests.resources.MASTER89, '0:89'), # complete
# ]


def run_package(pdf, outpath, pages=None):
    utila.log(f'run {pdf}')
    todo = []
    todo.extend(create_todo_rawmaker(pdf, outpath, pages=pages))

    todo.append(('groupme', outpath, outpath, ''))
    todo.append(('sections', outpath, outpath, '--all'))
    # required by abbreviation test
    todo.append(('words', outpath, outpath, '--all'))

    todo = [
        f'{executable} -i {inpath} -o {outpath} {configuration}'
        for (executable, inpath, outpath, configuration) in todo
    ]
    todo = ' && '.join(todo)  # pylint:disable=R0204
    completed = utila.run(todo)
    utila.assert_success(completed)
    return todo


def run_single(pdf, dest, pages=None):
    """Extract only rawmaker and linero and nothing more."""
    todo = create_todo_rawmaker(pdf, dest, pages=pages)
    todo = [
        f'{executable} -i {inpath} -o {outpath} {configuration}'
        for (executable, inpath, outpath, configuration) in todo
    ]
    todo = ' && '.join(todo)  # pylint:disable=R0204
    completed = utila.run(todo)
    utila.assert_success(completed)
    return todo


def extract():
    for pdf, _, __ in PACKAGE:
        assert pdf.endswith('.pdf') and os.path.exists(pdf), pdf

    # ensure that generation directory exists
    os.makedirs(tests.resources.GENERATED)
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER) as executor:
        futures_standard = {
            executor.submit(run_package, pdf, out, pages=pages): pdf
            for pdf, out, pages in PACKAGE
        }
        # futures_singles = {
        #     executor.submit(run_single, pdf, out, pages=pages): pdf
        #     for pdf, out, pages in SINGLE
        # }
        futures = {}
        futures.update(futures_standard)
        # futures.update(futures_singles)
        for future in concurrent.futures.as_completed(futures):
            try:
                comment = future.result()
                utila.log(comment)
            except Exception:
                utila.error(f'{future} failed.')
                raise


def create_todo_rawmaker(inpath, outpath, pages=None):
    # default config
    # TODO: move configuration to global var
    config = '--all --char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25 '
    pages = f' --pages {pages} ' if pages is not None else ' '
    result = [
        (
            'rawmaker -j8',
            inpath,
            outpath,
            # oneline configuration
            detector.feature.titlepage.RAWMAKER_CONFIGURATION + pages,
        ),
        (
            'rawmaker -j8',
            inpath,
            outpath,
            config + pages,
        ),
        (
            'linero',
            outpath,
            outpath,
            '',
        ),
    ]
    return result



# def extract_without_titlepage():
#     destination = tests.resources.NO_TITLE
#     without_titlepage = [
#         os.path.join(destination, f'{item}.pdf')
#         for item in hey.example.output_names(tests.resources.NO_TITLE_EXAMPLE)
#     ]
#     todo = [
#         f'jam -i {inpath} -o {outpath} --remove=0' for inpath, outpath in zip(
#             tests.resources.NO_TITLE_EXAMPLE,
#             without_titlepage,
#         )
#     ]
#     returncode = utila.run_parallel(todo, worker=WORKER)
#     assert returncode == utila.SUCCESS, str(returncode)
#     hey.example.extract(without_titlepage, destination, pages='0:10')
