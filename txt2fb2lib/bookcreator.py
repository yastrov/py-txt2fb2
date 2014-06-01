#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert plain txt file to FB2 (FictionBook) format.
Include devision by paragraph and include image files.

Very Simple Finity State Machine here.

Required Python 3.4 or higher.
"""

__author__ = 'Yuri Astrov <yuriastrov@gmail.com>'
__copyright__ = "Copyright 2014, Txt2FB2"
__credits__ = ["Yuri Astrov", ]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Yuriy Astrov"
__email__ = "yuriastrov@gmail.com"

__all__ = ['txt2fb2',]

import re

from enum import Enum, unique
@unique
class STATE(Enum):
    MAKING_SECTION = 1
    MAKING_TITLE = 2
    MAKING_TEXT = 3
    MAKING_IMG = 4
    INIT = 5

from .titlematcher import testTitle, testNewPart
testTitle = re.compile(testTitle, re.UNICODE)
testNewPart = re.compile(testNewPart, re.UNICODE)
from .fb2creator import FB2Creator
from .booktokenize import tokenize, Data

def stack_to_str(__stack):
    while __stack and __stack[0].tag == "SPACE":
        __stack.pop(0)
    s = ''
    if __stack:
        s = ''.join( map(lambda x: x[0], __stack) )
        __stack.clear()
    return s

def txt2fb2(fdiscr, encoding=None,
            covername=None, title=None,
            annotation=None, dir_name=None,
            author_firstname=None, author_lastname=None,
            author_middlename=None,
            genres=None):
    FB2 = FB2Creator()
    FB2.make_titleinfo(title=title, cover=covername, 
                        genres=genres)
    FB2.set_book_author(lastdname=author_lastname,
                        firstname=author_firstname,
                        middlename=author_middlename)
    FB2.make_documentinfo()
    FB2.set_doc_author(lastdname=author_lastname,
                       firstname=author_firstname,
                       middlename=author_middlename)
    __state = STATE.INIT
    __stack = []
    flag_part_previous = 0
    flag_point_previous = 0
    for token in tokenize(fdiscr.readline, encoding=encoding):
        val, tag, pos, line_num, line_v = token
        if __state == STATE.INIT:
            if testNewPart.match(line_v):
                FB2.open_section()
                flag_part_previous = 1
                __state = STATE.MAKING_TITLE
            elif testTitle.match(line_v):
                FB2.open_section()
                __state = STATE.MAKING_TITLE
            else: __stack.append(token)
            __stack.append(token)
            
        elif __state == STATE.MAKING_TITLE:
            if tag in ['ENDOFLINE',]:
                s = stack_to_str(__stack)
                FB2.make_title(s)
                __state = STATE.MAKING_TEXT
            elif tag =='SPACE' and pos == 0:
                pass
            else:
                __stack.append(token)

        elif __state == STATE.MAKING_TEXT:
            if tag == 'IMGFILEPATH':
                if __stack:
                    s = stack_to_str(__stack)
                    FB2.make_p(s)
                FB2.add_image(val, dir_name=dir_name)
            elif pos == 0 and tag == 'ENDOFLINE':#
                s = stack_to_str(__stack)
                FB2.make_p(s)
                FB2.make_emptyline()
            elif tag == 'ENDOFLINE':
                pass
            
            elif testNewPart.match(line_v):
                FB2.make_p(stack_to_str(__stack))
                FB2.close_section()
                FB2.close_section()
                FB2.open_section()
                __state = STATE.MAKING_TITLE
                __stack.append(token)
                flag_part_previous = 1

            elif testTitle.match(line_v):
                FB2.make_p(stack_to_str(__stack))
                if flag_part_previous != 1:
                    FB2.close_section()
                flag_part_previous = 0
                FB2.open_section()
                __state = STATE.MAKING_TITLE
                __stack.append(token)
            elif pos == 0 and tag in ["SPACE", 'TIRE', 'CAVYCHKI'] and flag_point_previous:
                FB2.make_p(stack_to_str(__stack) )
                __state = STATE.MAKING_TEXT
                if tag != 'SPACE':
                    __stack.append(token)
                flag_point_previous = 0
            else:
                if pos == 0 and val[0].islower():
                    __stack.append( Data(' ', 'SPACE', 0, 0, '') )
                if tag == 'ENDOFSENTENS':
                    flag_point_previous = 1
                elif tag != 'SPACE':
                    flag_point_previous = 0
                __stack.append(token)
        elif __state == STATE.MAKING_IMG:
            FB2.add_image(val)
        continue
    if __stack:
        s = stack_to_str(__stack)
        FB2.make_p(s)
    return FB2