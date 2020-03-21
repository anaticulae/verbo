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


# yapf:disable
PACKAGE = [
    (tests.resources.BACHELOR37_PDF, tests.resources.BACHELOR37, None),
    (tests.resources.HOWTO_PYPORTING_PDF, tests.resources.HOWTO_PYPORTING, None),
    (tests.resources.MASTER72_PDF, tests.resources.MASTER72, None),
    (tests.resources.PYPORTING_PDF, tests.resources.PYPORTING, None),
    (tests.resources.RESTRUCT_PDF, tests.resources.RESTRUCT, None),
]


def run_package(pdf, outpath, pages=None):
    relative = utila.make_relative(pdf, tests.resources.RESOURCES)
    utila.log(f'run: {relative}')
    todo = []
    todo.extend(create_todo_rawmaker(pdf, outpath, pages=pages))

    todo.append(('groupme', outpath, outpath, '-j8'))
    todo.append(('sections', outpath, outpath, '-j8'))

    todo = [
        f'{executable} -i {inpath} -o {outpath} {configuration}'
        for (executable, inpath, outpath, configuration) in todo
    ]
    todo = ' && '.join(todo)  # pylint:disable=R0204
    completed = utila.run(todo)
    utila.assert_success(completed)
    utila.log(f'completed: {relative}')
    return todo



def extract():
    utila.log(f'root: {tests.resources.RESOURCES}')
    for pdf, _, __ in PACKAGE:
        assert pdf.endswith('.pdf') and os.path.exists(pdf), pdf

    # ensure that generation directory exists
    os.makedirs(tests.resources.GENERATED)
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER) as executor:
        futures_standard = {
            executor.submit(run_package, pdf, out, pages=pages): pdf
            for pdf, out, pages in PACKAGE
        }
        futures = {}
        futures.update(futures_standard)
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
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
