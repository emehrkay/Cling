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

define('page_dir', default=os.path.join(os.path.dirname(__file__), 'page'), 
    help='The directory where the page.md files are stored')
define('page_404', default=os.path.join(os.path.dirname(__file__), 'page', '404.md'), 
    help='The path to the 404.md page')
define('sort_article_by', default='modified', help='Parameter to sort articles by; modifed or created')

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

        routes = [
            (r'/([\w_\-\/]+)?', PageHandler),
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
        
    
    def parse_page(self, page=None):
        """method used to render a page from the page directory
        
        args:
            stirng page 
        """
        title, lead_image, slug, date, template, content = parse_page(page)
        content = self._template_string(content)
        template = '%s.html' % os.path.join('template', template)
        content = self.render_string(template, content=content, page=os.path.join(options.page_dir, page))
        page_content = self.render_string('template/page/page.html', title=title, 
            slug=slug, date=date, content=content, page=page, lead_image=lead_image)
            
        return title, slug, date, template, page_content
        
    def is_ajax(self):
        return 'X-Requested-With' in self.request.headers and \
            self.request.headers['X-Requested-With'] == 'XMLHttpRequest'

        
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

        if path is None:
            path = 'index'

        path = slug_to_name(path)
        
        if ajax is False:
            if path is None or str(path).lower() != 'toc':
                title, slug, date, template, content= self.parse_page('toc')
                page_content += content

            if path is None or str(path).lower() != 'index':
                title, slug, date, template, content = self.parse_page('index')
                page_content += content


        title, slug, date, template, content = self.parse_page(path)
        page_content += content
                
        if ajax is True:
            self.write({
                'title': title,
                'slug': slug,
                'date': date,
                'path': '/' + path,
                'content': page_content
            })
        else:
            self.render('template/base.html', title=title, page_content=page_content)


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

