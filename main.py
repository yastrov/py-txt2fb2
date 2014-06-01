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

import logging
import re
import os
import sys
logger = logging.getLogger(__name__)
from txt2fb2lib.bookcreator import txt2fb2

def main():
    try:
        if not sys.stdin.isatty():
            FB2 = txt2fb2(f)
            sys.stdout.write(FB2.to_str())
            exit()
        import argparse
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("path",
                                help="filename with txt file.")
        parser.add_argument("output",
                                help="filename with output file.")
        parser.add_argument('-e', '--encoding',
                            default=None)
        parser.add_argument('-t', '--title',
                            default=None,
                            help='book title')
        parser.add_argument('-f', '--firstname',
                            default=None,
                            help='author firstname')
        parser.add_argument('-l', '--lastname',
                            default=None,
                            help='author lastname')
        parser.add_argument('-m', '--middlename',
                            default=None,
                            help='author middlename')
        parser.add_argument('-v', "--version", action='version',
                                version='%(prog)s {}'.format(__version__),
                                help="print version")
        args = parser.parse_args()
        dir_name = os.path.dirname(args.path)
        with open(args.path, 'r', encoding='utf-8') as f:
            FB2 = txt2fb2(f, title=args.title,
                            author_firstname=args.firstname,
                            author_lastname=args.lastname,
                            author_middlename=args.middlename,
                            dir_name=dir_name, encoding=args.encoding)
            FB2.to_file(args.output, pretty_print=True)
    except Exception as e:
        logger.exception(e)

if __name__ == "__main__":
    main()