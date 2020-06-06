# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import utila

import words

RESOURCES = os.path.join(words.ROOT, 'tests/resources')

BACHELOR = os.path.join(RESOURCES, 'bachelor')
BOOK = os.path.join(RESOURCES, 'book')
DOCU = os.path.join(RESOURCES, 'docu')
HOMEWORK = os.path.join(RESOURCES, 'homework')
MASTER = os.path.join(RESOURCES, 'master')
ORDER = os.path.join(RESOURCES, 'order')
TECHNICAL = os.path.join(RESOURCES, 'technical')

GENERATED = os.path.join(RESOURCES, 'generated')
NO_TITLE = os.path.join(GENERATED, 'notitle')

RESTRUCT = os.path.join(GENERATED, 'restruct')
RESTRUCT_PDF = os.path.join(DOCU, 'restructuredtext.pdf')

HOWTO_PYPORTING = os.path.join(GENERATED, 'howto_pyporting')
HOWTO_PYPORTING_PDF = os.path.join(DOCU, 'howto_pyporting.pdf')

PYPORTING = os.path.join(GENERATED, 'porting_module')
PYPORTING_PDF = os.path.join(DOCU, 'porting_extension_modules.pdf')

BACHELOR37 = os.path.join(GENERATED, 'page_37_tables')
BACHELOR37_PDF = os.path.join(BACHELOR, 'page_37_tables.pdf')

MASTER72 = os.path.join(GENERATED, 'page_72_noimages_toc')
MASTER72_PDF = os.path.join(MASTER, 'page_72_noimages_toc.pdf')

HOMEWORK40 = os.path.join(GENERATED, 'page_40_images_toc')
HOMEWORK40_PDF = os.path.join(HOMEWORK, 'page_40_images_toc.pdf')

BACHELOR76 = os.path.join(GENERATED, 'page76')
BACHELOR76_PDF = os.path.join(BACHELOR, 'page76.pdf')

REQURIED_RESOURCES = [
    BACHELOR37,
    BACHELOR37_PDF,
    BACHELOR76,
    BACHELOR76_PDF,
    HOMEWORK40,
    HOMEWORK40_PDF,
    MASTER72,
    MASTER72_PDF,
    PYPORTING,
    PYPORTING_PDF,
    RESOURCES,
    RESTRUCT,
    RESTRUCT_PDF,
]

REQURIED_RESOURCES = [utila.forward_slash(item) for item in REQURIED_RESOURCES]
