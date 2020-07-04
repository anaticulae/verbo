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
import power
import utila

WORKER = 12


def extract_examples():
    if os.path.exists(power.generated()):
        return
    extract()


PACKAGE = [
    (power.MASTER072_PDF, power.link(power.MASTER072_PDF), None),
    (power.BACHELOR076_PDF, power.link(power.BACHELOR076_PDF), None),
    (power.HOMEWORK040_PDF, power.link(power.HOMEWORK040_PDF), None),
    (power.BACHELOR037_PDF, power.link(power.BACHELOR037_PDF), None),
    (power.DOCU07_PDF, power.link(power.DOCU07_PDF), None),
    (power.DOCU09_PDF, power.link(power.DOCU09_PDF), None),
    (power.DOCU27_PDF, power.link(power.DOCU27_PDF), None),
]


def run_package(pdf, outpath, pages=None):
    relative = utila.make_relative(pdf, power.REPOSITORY)
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
    utila.log(f'root: {power.REPOSITORY}')
    for pdf, _, __ in PACKAGE:
        assert pdf.endswith('.pdf') and os.path.exists(pdf), pdf

    # ensure that generation directory exists
    os.makedirs(power.generated())
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
            except Exception as error:
                utila.error(error)
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
