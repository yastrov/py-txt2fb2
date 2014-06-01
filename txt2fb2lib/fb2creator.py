#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert plain txt file to FB2 (FictionBook) format.
Include devision by paragraph and inclide image files.

Fiction Book creator here. 

Required Python 3.4 or higher.
"""

__all__ = ['convert_image', 'FB2Creator']

__author__ = 'Yuri Astrov <yuriastrov@gmail.com>'
__copyright__ = "Copyright 2014, Txt2FB2"
__credits__ = ["Yuri Astrov", ]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Yuri Astrov"
__email__ = "yuriastrov@gmail.com"

import os
exists = os.path.exists
basename =  os.path.basename
pjoin = os.path.join

def convert_image(filename):
    """
    Convert with PIL any image to PNG.
    Return filename after convert.
    """
    new_filename = filename.replace(
        filename.split('.')[-1], 'png'
        )
    if exists(new_filename):
        return new_filename
    from PIL import Image
    im = Image.open(filename)
    im.save( new_filename, 'PNG')
    return new_filename

from xml.etree import ElementTree as ET
from base64 import b64encode

def _make_sub_element(parent, tag):
    ns = '{http://www.gribuser.ru/xml/fictionbook/2.0}'
    return ET.SubElement(parent, ''.join((ns, tag)))

class FB2Creator:
    def __init__(self):
        ET.register_namespace('',"http://www.gribuser.ru/xml/fictionbook/2.0") #some name
        self.root = ET.Element("{http://www.gribuser.ru/xml/fictionbook/2.0}FictionBook")
        self.root.set('xmlns:xlink',"http://www.w3.org/1999/xlink")
        self.tree = ET.ElementTree(self.root)
        self.description = _make_sub_element(self.root, 'description')
        self.body = _make_sub_element(self.root, 'body')
        self.sectionstack = []

    def make_titleinfo(self, genres=None, title='Title',
                        annotation="Annotation", lang='rus', cover=None):
        self.titleinfo = _make_sub_element(self.description, 'title-info')
        if not genres:
            genres = ('nonfiction',)
        if genres:
            for genre in genres:
                _genre = _make_sub_element(self.titleinfo, 'genre')
                _genre.text = genre
        self.book_author = _make_sub_element(self.titleinfo, 'author')
        self.booktitle = _make_sub_element(self.titleinfo, 'book-title')
        if title: self.booktitle.text = title
        self.annotation = _make_sub_element(self.titleinfo, 'annotation')
        if annotation: self.annotation.text = annotation
        self.lang = _make_sub_element(self.titleinfo, 'lang')
        self.lang.text = lang
        if cover:
            if not exists(cover):
                return
            b_name = basename(cover)
            end = b_name.split('.')[-1]
            if not (end in ["jpg", "jpeg", 'png', 'JPG', 'JPEG', 'png']):
                cover = convert_image(fname)
            with open(cover, "rb") as f_im:
                data = f_im.read()
                data = b64encode(data)
                b_name = basename(fname)
                if end in ["jpg", "jpeg"]:
                    end = "jpeg"
                elif end == ".png":
                    end = "png"
                binary = _make_sub_element(self.root, 'binary')
                binary.set("id", b_name)
                binary.set("content-type", ''.join(("image/", end)) )
                binary.text = data.decode('utf-8') #or may use str(data, 'utf-8')
                image = _make_sub_element(self.titleinfo, 'image')
                image.set("xlink:href", ''.join(('#', b_name)) )

    def set_book_author(self, firstname=None, lastdname=None, middlename=None):
        if firstname:
            _firstname = _make_sub_element(self.book_author, 'first-name')
            _firstname.text = firstname
        if lastdname:
            _lastdname = _make_sub_element(self.book_author, 'last-name')
            _lastdname.text = lastdname
        if middlename:
            _middlename = _make_sub_element(self.book_author, 'middle-name')
            _middlename.text = middlename

    def make_documentinfo(self):
        import time
        self.documentinfo = _make_sub_element(self.description, 'document-info')
        self.doc_author = _make_sub_element(self.documentinfo, 'author')
        self.date = _make_sub_element(self.documentinfo, 'date')
        self.date.set('value', time.strftime("%Y-%m-%d"))
        self.date.text = time.strftime("%Y")
        self.id = _make_sub_element(self.documentinfo, 'id')
        self.id.text = ''.join(("YA-",time.strftime("%Y%m%d%H%M%S")))
        version = _make_sub_element(self.documentinfo, 'version')
        version.text = '1.0'

    def set_doc_author(self, firstname=None, lastdname=None, middlename=None, nickname=None):
        if firstname:
            _firstname = _make_sub_element(self.doc_author, 'first-name')
            _firstname.text = firstname
        if lastdname:
            _lastdname = _make_sub_element(self.doc_author, 'last-name')
            _lastdname.text = lastdname
        if middlename:
            _middlename = _make_sub_element(self.doc_author, 'middle-name')
            _middlename.text = middlename
        if nickname:
            _nick = _make_sub_element(self.doc_author, 'nickname')
            _nick.text = nickname

    def open_section(self):
        section = None
        if len(self.sectionstack):
            section = _make_sub_element(self.section, 'section')
        else:
            section = _make_sub_element(self.body, 'section')
        self.sectionstack.append(section)
        self.section = section

    def close_section(self):
        if len(self.sectionstack):
            self.sectionstack.pop()
        if len(self.sectionstack):
            self.section = self.sectionstack[-1]

    def make_title(self, title_string):
        title = _make_sub_element(self.section, 'title')
        p = _make_sub_element(title, 'p')
        p.text = title_string

    def make_p(self, text):
        if (not text) or (text == ''):
            return
        self.p = _make_sub_element(self.section, 'p')
        self.p.text = text

    def make_emptyline(self):
        empty = _make_sub_element(self.section, 'empty-line')

    def add_image(self, fname, encoding='utf-8', dir_name=None):
        if not exists(fname):
            if dir_name is None:
                dir_name = os.getcwd()
            fname = pjoin(dir_name, fname)
            if not exists(fname):
                return
        b_name = basename(fname)
        end = b_name.split('.')[-1]
        if not (end in ["jpg", "jpeg", 'png', 'JPG', 'JPEG', 'png']):
            fname = convert_image(fname)
        with open(fname, "rb") as f_im:
            data = f_im.read()
            data = b64encode(data)
            if end in ["jpg", "jpeg", 'JPG', 'JPEG']:
                end = "jpeg"
            elif end == "png":
                end = "png"
            binary = _make_sub_element(self.root, 'binary')
            binary.set("id", b_name)
            binary.set("content-type", ''.join(("image/", end)) )
            binary.text = data.decode(encoding) #or may use str(data, 'utf-8')
            image = _make_sub_element(self.section, 'image')
            image.set("xlink:href", ''.join(('#', b_name)) )

    def add_poem(self):
        self.poem = _make_sub_element(self.section, 'poem')

    def add_poem_stanza(self):
        self.stanza = _make_sub_element(self.poem, 'stanza')

    def add_poem_v(self, text):
        v = _make_sub_element(self.stanza, 'v')
        v.text = text

    def add_poem_title(self, title):
        _title = _make_sub_element(self.poem, 'title')
        _title.text = title

    def to_file(self, fname, encoding='utf-8', pretty_print=False):
        if pretty_print:
            rough_string = ET.tostring(self.root, encoding)
            import xml.dom.minidom as minidom
            reparsed = minidom.parseString(rough_string)
            with open(fname, "w", encoding=encoding) as f:
                reparsed.writexml(f, indent="\n", addindent="   ", encoding=encoding)
        else:
            self.tree.write(fname,
                            xml_declaration=True, encoding=encoding,
                            method="xml")

    def to_str(self, encoding='utf-8', pretty_print=False):
        rough_string = ET.tostring(self.root, encoding)
        if pretty_print:
            import xml.dom.minidom as minidom
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="    ")
        else:
            return rough_string