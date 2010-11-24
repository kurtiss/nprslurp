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

FILE = "{date.year}{date.month}{date.day}_{show}_{part:02d}.mp3"
URL = "http://public.npr.org/anon.npr-mp3/npr/{show}/{date.year}/{date.month}/{file}"
COMMAND = "wget {url} -O {path}q"


def nprslurp(show, working_dir=None):
    working_dir = working_dir or os.getcwd()
    date = None
    delta = None

    if show == "pj":
        date = get_latest_weekday(3)
        delta = datetime.timedelta(days = 7)
    else:
        raise RuntimeError("Unrecognized show: {0}".format(show))
        
    context = dict(
        show = show,
        date = date
    )

    while slurp_one(context, working_dir):
        context['date'] = context['date'] - delta


def slurp_one(context, working_dir):
    for part in itertools.count(1):
        context['part'] = part
        context['file'] = FILE.format(**context)
        context['path'] = os.path.join(working_dir, context['file'])
        context['url'] = URL.format(**context)

        if not os.path.exists(context['path']):
            code = os.system(COMMAND.format(**context))
            if code != 0:
                return part != 1

def get_latest_weekday(weekday):
    today = datetime.datetime.now().date()
    today_weekday = today.weekday()
    latest = None

    if weekday > today_weekday:
        latest = today - datetime.timedelta(days = 6 - (weekday - today_weekday))
    else:
        latest = today + datetime.timedelta(days = today_weekday - weekday)

    return latest