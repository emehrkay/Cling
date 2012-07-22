#!/usr/bin/env python
# encoding: utf-8
"""
utils.py

cling utilities
"""
import markdown
import os
import re

from tornado.options import options

def directory_listing(directory):
    """this function creates a simple dict where the key is the name 
    of the file and the value is the category that it belongs to
    
    args:
        string directory -- the directory to read
    """
    pages = []
    
    for path, dirs, files in os.walk(directory):
        cat = path.split(os.sep)[1:]

        if len(cat):
            for f in files:
                if f.endswith('.md') and f != 'index.md':
                    fixed = name_to_slug(f[:-3])
                    pages.append((fixed, cat, os.path.join(path, f)))
                    
    def sort(page):
        if options.sort_article_by == 'modified':
            return os.path.getmtime(page[2])
        else:
            return os.path.getctime(page[2])
            
    pages.sort(key=sort, reverse=True)
    
    return pages
    

def category_listing(directory, category=None):
    """this function creates a directory listing as a dictionary
    it will only allow .md files to be listed
    
    args:
        string directory -- the path to the md files
        string category -- the name where the pages will listed under
    """
    list_pages = {}
    sorted_pages = {}
    
    if category is not None and category not in list_pages:
        list_pages[category] = []
    
    for dir_file in os.listdir(directory):
        full = os.path.join(directory, dir_file)
        
        if os.path.isdir(full):
            sub_category = dir_file
            
            if category is not None:
                sub_category = '%s%s%s' % (category, '/', dir_file)
                
            sub_list = category_listing(full, sub_category)
            list_pages = dict(list_pages.items() + sub_list.items())
        elif category is not None :
            if dir_file.endswith('.md'):
                list_pages[category].append(name_to_slug(dir_file))

    for key, value in sorted(list_pages.items(), key=lambda x: x[1]):
        sorted_pages[key] = value

    return sorted_pages

    
def name_to_slug(name):
    """simple function that transforms a name to a slug
    
    args:
        string name -- the name to be converted
    """
    if name.endswith('.md'):
        name = name[:-3]
    return re.sub('\W', '-', name)
    
    
def slug_to_name(slug):
    """simple function that transforms a slug to a name
    
    args:
        string name -- the name to be converted
    """
    return re.sub('-', ' ', slug)

    
def get_file_contents(file_name):
    """get file contents
    
    args:
        string file_name -- path to file to read
    """
    with open(file_name) as f:
        return f.read()


def parse_page(page, auto_index=True):
    """this function takes a page written in markdown and returns
    a list of strings including: title, slug, date, template, parsed
    
    args:
        string page -- the file to be parsed
    """
    full = os.path.join(options.page_dir, page)
    full_file = '%s.md' % full
    md = markdown.Markdown(extensions = ['meta'])
    
    if os.path.isfile(full_file):
        md_page = full_file
    elif os.path.isdir(full):
        dir_index = os.path.join(full, 'index.md')
        
        if os.path.isfile(dir_index) and auto_index:
            md_page = dir_index
        else:
            md_page = os.path.join(options.page_dir, 'toc.md')
    elif os.path.exists(full_file) is False:
        md_page = os.path.join(options.page_dir, '404.md')
    else:
        md_page = os.path.join(options.page_dir, 'index.md')

    content = get_file_contents(md_page)
    parsed = md.convert(content)
    meta = md.Meta
    title = str(meta.get('title', [''])[0])
    slug = name_to_slug(md_page.split(os.sep)[-1])
    date = str(meta.get('date', ['today'])[0])
    template = str(meta.get('template', ['page/base'])[0])
    lead_image = str(meta.get('lead_image', [''])[0])
    
    return title, lead_image, slug, date, template, parsed