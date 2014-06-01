#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Regular Expression string for detect new part or chapter. Please, change it for you book.
"""

__all__ = ['testTitle', 'testNewPart']


def group(choices):
    c = r'|'.join(choices)
    return ''.join( ('(', c, ')') )

titles = (
        r'\s+Глава\s\d+\.',
        r'\s+ГЛАВА\s\d+\.',
        r'\s+Chapter\s\d+\.',
        r'\s+CHAPTER\s\d+\.',
    )

parts = (
        r'\s+Часть\s\d+\.',
        r'\s+ЧАСТЬ\s\d+\.',
        r'\s+Part\s\d+\.',
        r'\s+PART\s\d+\.',
    )

testTitle = group(titles)
testNewPart = group(parts)
del titles
del parts