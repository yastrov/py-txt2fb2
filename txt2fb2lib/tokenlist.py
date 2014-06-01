#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regular expression for match tokens.
"""

token_list = (
        (r'\n$', 'ENDOFLINE'),
        (r'^$', 'EMPTYLINE'),
        (r'^\s+', 'SPACE'),
        (r'\d[\.,\d]*', 'NUMBER'),
        (r'\.|\?|!', 'ENDOFSENTENS'),
        (r'-|—', 'TIRE'),
        (r'"', 'CAVYCHKI'),
        (r'(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]\.jpg|png|gif|jpeg|GPG|JPEG', 'IMGURL'),
        (r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', 'URL'),
        (r'\<([A-Za-zА-Яа-я\d].+\.(gif|jpg|png|JPG|jpeg|JPEG|PNG))\>', 'IMGFILEPATH'),
        (r'[A-Za-zА-Яа-я-`]+', 'WORD'),
        (r'\S', 'SUMBOL'),
        (r'.', 'NONE')
    )