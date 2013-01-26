import os
from tornado.options import define

define('allow_data', default=True, help='Allows requests to be returned as an dictionary/json by appending .data to the end of requests')
define('site_root', default=os.path.dirname(__file__), help='Full path to site root')
define('page_dir', default='page', help='The directory where the page.md files are stored')
define('static_dir', default='static', help='The directory where all of the static (css, js, img, etc.) files are stored')
define('page_404', default=os.path.join(os.path.dirname(__file__), 'page', '404.md'), 
    help='The path to the 404.md page')
define('sort_article_by', default='modified', help='Parameter to sort articles by; modifed or created')
define('theme_dir', default='theme', help='This is where the themes are located')
define('theme', default='emehrkay', help='The theme to be used with the website')