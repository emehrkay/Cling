# Cling

<img src="https://github.com/emehrkay/Cling/raw/master/static/img/default/logo_small.png" />

Static-site based on Tornado. See example at <http://www.clingpy.com>.

## Installation

*Assuming that you have virtualenv installed*

* Create an environment for your site

```
virtualenv your_app
cd your_app
```

* Place Cling project fils in your_app directory
* Start the virtual environment inside of your_app

```
. bin/activate
```

* Install dependencies 

```
pip install -r requirements.txt
```

* Start the application

```
python cling.py
```

* Begin adding your content


## Adding Content

Since Cling.py is built on top of Tornadoweb, it makes use of Torando's templating engine and UI modules.

### Page System

Cling.py is a Markdown-based application that utilized version 2.2 of the Python Markdown utility. By default pages are stored in the ```page``` directory. Pages stored in the root of the directory (index.md, 404.md) will not show up under any category, but they are accessible via their slug (.com/404 .com/index). Storing pages directly in the root page directory is a good way to have pages that you do not want to show up in the table of contents. 

To create a new category simply add a new directory in the ```page``` directory; categories can have sub-categories by using the same process and are probably infinite (didn't test it). When a category is accessed via the url (.com/category), the toc.md page is parsed and shows all of the pages for the given category. This will first check for the existence of an index.md file in that directory and use that instead of the toc.md.

The table of contents page will order files either by date created or date modified as defined in the confif.py and will only consider files that end with ```.md```. Each page listed in the table of contents will also list all of the categories associated with the page. 

To create draft pages simply save a file anywhere in the ```page``` directory with any extension other than ```.md```. If you create a draft called ```new_info.txt``` under /info, browsing to .com/info/new_info will not load the file, the 404 page will be loaded. To preview the file you add ```.preview``` and the file's extension to the end of the url .com/info/new_info.txt.preview and the page will be loaded. Previewing non-.md files is an option configurable in config.py.

#### Tornado Module System

Each page is first rendered via the Markdown parser and is passed through the Tornado templating engine supplying the page with request metadata, ui modules, and localization functionality. 

Pages can simply include template logic and it will be parsed before the page is rendered.

If you wanted to display the table of contents module inside one of your ```.md``` pages, you would simply pepper it with (where desired):

```
{{ modules.TOC() }}
```

## Site Administration

The admin.py script allows for you to enable|disable themes by running a simple command:

```
python admin.py theme [enable|disable] $theme_name
```

This will either create or remove a symlink insdie of the ```static_dir`` that points to the theme's static directory. 

## Theming

Writing a custom theme is pretty simple and allows for a lot of customization. 

A successful theme must follow a few rules:
	
* Must contain a static directory. Anything in this directory will be publicly accessible, so take caution.
* To overwrite any html file in the template directory, it must follow the same directory structure. For example, if you want a different base page, the file must live in $theme_name/base.html.

## Site Configuration

All site configuration options are located in config.py.

* allow_data -- if a request is sent to a Cling.py site via Ajax, a json object is returned. If allow\_data is set to True, appending .data to the end of the request will return the same data. This also works with previews: .com/test/test.txt.preview.data will load the data for a non-.md file. Defaulted to True
* allow_preview -- allows loading of non-.md files. Defaulted to True
* site_root -- full path to the site installation.
* page_dir -- The directory where the page.md files are stored. Relative to the site\_root.
* static_dir -- The directory where the static files (js, css, img, etc.) are stored. Relative to the site\_root.
* theme_dir -- The directory where the themes are stored. Relative to the site\_root.
* page_404 -- The path to the 404.md page. Relative to the page\_dir.
* sort\_article_by -- Parameter to sort articles by: modified or created.
* theme -- The theme to use for your Cling.py website.

## Folder Structure

* Cling
	* admin.py -- site administration functionality
    * config.py -- site configuration, has default values
    * cling.py -- main library
    * logo -- assets for art, currently contains psd for the logo
    * page -- default markdown pages
        * 404.md -- the default 404 page
        * index.md -- the default landing page
        * toc.md -- the table of contents page
    * static -- static site assets
        * css -- stylesheets 
        * js - JavaScript
        * img -- images
    * template -- the default set of site templates
        * asset 
            * footer.html -- site footer
            * toc.html -- template to create the table of contents list
        * base.html -- the main html > body markup
        * page -- the different page templates. If your page/markdown.md file is going to use a different template, it goes in here
            * base.html -- default page template used
            * page.html -- frames a page
            * toc.html -- frames the table of contents page. This also calls the TOC ui module
    * utils.py -- utility functions that are used throughout the application

#License

Licensed under MIT (see LICENSE)