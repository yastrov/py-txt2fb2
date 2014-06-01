#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert plain txt file to FB2 (FictionBook) format.
Include devision by paragraph and inclide image files.

Required Python 3.4 or higher.
"""

__author__ = 'Yuri Astrov <yuriastrov@gmail.com>'
__copyright__ = "Copyright 2014, Txt2FB2"
__credits__ = ["Yuri Astrov", ]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Yuriy Astrov"
__email__ = "yuriastrov@gmail.com"

import re
from collections import namedtuple

Data = namedtuple('Data', ["string", "tag", "pos", 'line_num', 'line_val'])

from .tokenlist import token_list

def _compile(expr):
    return re.compile(expr, re.UNICODE)

token_exprs = list(map(lambda x: (_compile(x[0]), x[1] ), token_list))
del token_list

def tokenize(readline, encoding=None):
    global token_exprs
    lnum = -1
    while True:             # loop over lines in stream
        try:
            line = readline()
        except StopIteration:
            line = b''
            raise StopIteration

        if encoding is not None:
            line = line.decode(encoding)
        lnum += 1
        pos, end = 0, len(line)
        if pos == end: break
        while pos < end:
            match = None
            for pattern, tag in token_exprs:
                match = pattern.match(line, pos)
                if match:
                    text = match.group(0)
                    if tag:
                        if tag in ['IMGFILEPATH',]:
                            yield Data(match.group(1), tag, pos, lnum, line)
                        else:
                            yield Data(text, tag, pos, lnum, line)
                    pos = match.end(0)
                    break