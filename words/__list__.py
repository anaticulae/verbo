# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import yaml


def dump_lists(lists: list) -> str:
    raw = []
    for (pagenumber, pagecontent) in lists:
        pagenumber = int(pagenumber)
        pageresult = []
        for lists_ in pagecontent:
            # Number, Item
            area = ' '.join([str(item) for item in lists_.area])
            content = []
            for pnumber, item in lists_.data:
                assert item, f'page: {pagenumber}; {pnumber} empty list content'
                content.append(f'{pnumber} {item}')
            pageresult.append({
                'area': area,
                'content': content,
                'id': f'{lists_.paragraph} {lists_.merged}',
            })
        if pageresult:
            raw.append({
                'page': pagenumber,
                'lists': pageresult,
            })
    dumped = yaml.safe_dump(raw)
    return dumped


serializeraw.dump_lists = dump_lists
