#!/usr/bin/env python
# encoding: utf-8
"""
cling.py

main site file
"""

import os.path

from tornado import httpserver, ioloop, web
from tornado.options import define, options
from utils import parse_page, directory_listing, slug_to_name
import config

class Application(web.Application):
    """main appliction launcher"""
    
    def __init__(self):
        settings = {
            'debug': True,
            'autoescape': None,
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'cookie_secret': 'a23,m.r49we342asdf6zxkyjlj889(*9ª•ª•90lij;)',
            'ui_modules': {'TOC': TocModule,}
        }
        
        route = (r'/([\w_\-\/]+)?', PageHandler)
        
        if options.allow_data:
            route = (r'/([\w_\-\/]+)?(?:\.data)?', PageHandler)

        routes = [
            route,
        ]
        web.Application.__init__(self, routes, **settings)
        

class BaseHandler(web.RequestHandler):
    """All web request handlers extends this class"""
    
    def _template_string(self, string, **kwargs):
        template = web.template.Template(string, autoescape=None)
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url,
            options=options,
        )
        args.update(**kwargs)
        args.update(self.ui)
        return template.generate(**args)
        
    def get_template_page(self, page):
        templates = ['%s.html' % os.path.join('template', page)]
        
        if options.theme is not None:
            templates.append('%s.html' % os.path.join(options.theme_dir, options.theme, page))
            #templates.insert(0, theme_template)
        
        for pt in reversed(templates):
            if os.path.isfile(pt):
                page_template = pt
                break
        
        return page_template
    
    def parse_page(self, page=None):
        """method used to render a page from the page directory
        
        args:
            stirng page 
        """
        title, lead_image, slug, date, template, content = parse_page(page)
        content = self._template_string(content)
        content_template = self.get_template_page(template)
        content_rendered = self.render_string(content_template, content=content, page=os.path.join(options.page_dir, page))
        page_template = self.get_template_page('page/page')
        page_content = self.render_string(page_template, title=title, 
            slug=slug, date=date, content=content_rendered, page=page, lead_image=lead_image)
            
        return title, slug, date, template, page_content
        
    def is_ajax(self):
        """simply determines if the request was an ajax
        request or not
        """
        return 'X-Requested-With' in self.request.headers and \
            self.request.headers['X-Requested-With'] == 'XMLHttpRequest'
            
    def is_data(self):
        """method that checks to see if the request was for data"""
        return self.request.uri.endswith('.data')

        
class PageHandler(BaseHandler):
    """main controller class"""
    
    def get(self, path=None):
        """main page loader
        if the path doesnt exists, it is set index
        if path isnt toc, toc is loaded
        if path isnt index, index is loaded
        """
        page_content = ''
        ajax = self.is_ajax()
        data = False
        theme = self.get_argument('theme', None)
        
        if theme is not None:
            options.define('theme', default=theme, mutable=True)

        if path is None:
            path = 'index'
            
        if options.allow_data:
            data = self.is_data()

        path = slug_to_name(path)

        if ajax is False or data is False:
            if path is None or str(path).lower() != 'toc':
                title, slug, date, template, content= self.parse_page('toc')

            if path is None or str(path).lower() != 'index':
                title, slug, date, template, content = self.parse_page('index')


        title, slug, date, template, content = self.parse_page(path)
        page_content += content
                
        if ajax is True or data is True:
            self.write({
                'title': title,
                'slug': slug,
                'date': date,
                'path': '/' + path,
                'content': page_content
            })
        else:
            page_template = self.get_template_page('base') 
            self.render(page_template, title=title, page_content=page_content)


class TocModule(web.UIModule):
    """this class is used to create the table of contents module
    that can be used in all of the templates
    """
    
    def render(self, directory=options.page_dir):
        """
        args:
            string directory -- the directory
        """
        if 'page/toc' in directory:
            directory = options.page_dir

        toc = directory_listing(directory)
        return self.render_string('template/asset/toc.html', data=toc)
        

if __name__ == '__main__':
    """Start the application"""
    http_server = httpserver.HTTPServer(Application())
    http_server.listen(9002)
    ioloop.IOLoop.instance().start()

