import os
from tornado.options import define

define('page_dir', default=os.path.join(os.path.dirname(__file__), 'page'), 
    help='The directory where the page.md files are stored')
define('page_404', default=os.path.join(os.path.dirname(__file__), 'page', '404.md'), 
    help='The path to the 404.md page')
define('sort_article_by', default='modified', help='Parameter to sort articles by; modifed or created')