#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py
"""

import datetime
import itertools
import os
from nprslurp.version import VERSION as __version__

__all__ = ['nprslurp']

FILE = "{date.year}{date.month:02d}{date.day:02d}_{show}_{part:02d}.mp3"
URL = "http://public.npr.org/anon.npr-mp3/npr/{show}/{date.year}/{date.month:02d}/{file}"
COMMAND = 'wget "{url}" -O "{path}"'
MAX_WEEK_SKIP_COUNT = 2
MAX_PART_SKIP_COUNT = 1


def nprslurp(show, working_dir=None):
    working_dir = working_dir or os.getcwd()
    date = None
    delta = None
    skips = 0

    if show == "pj":
        date = get_latest_weekday(4)
        delta = datetime.timedelta(days = 7)
    else:
        raise RuntimeError("Unrecognized show: {0}".format(show))
        
    context = dict(
        show = show,
        date = date
    )

    while skips <= MAX_WEEK_SKIP_COUNT:
        if not slurp_one(context, working_dir):
            skips += 1
        else:
            skips = 0
        context['date'] = context['date'] - delta


def slurp_one(context, working_dir):
    skip = 0

    for part in itertools.count(1):
        context['part'] = part
        context['file'] = FILE.format(**context)
        context['path'] = os.path.join(working_dir, context['file'])
        context['url'] = URL.format(**context)

        if not os.path.exists(context['path']):
            code = os.system(COMMAND.format(**context))
            if code != 0:
                skip += 1
                os.remove(context['path'])
                if skip > MAX_PART_SKIP_COUNT:
                    return part == MAX_PART_SKIP_COUNT
            else:
                skip = 0

def get_latest_weekday(weekday):
    today = datetime.datetime.now().date()
    today_weekday = today.weekday()
    latest = None

    if today_weekday >= weekday:
        latest = today - datetime.timedelta(days = today_weekday - weekday)
    else:
        latest = today - datetime.timedelta(days = (6 - weekday) + today_weekday)

    return latest