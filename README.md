# Cling

[Cling.py icon](https://github.com/emehrkay/Cling/raw/master/static/img/default/logo_small.png)

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

## Folder Structure

* Cling
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
    * utils.py -- utilities that are used throughout the application

## Site Configuration

* page_dir -- The directory where the page.md files are stored
* page_404 -- The path to the 404.md page
* sort\_article_by -- Parameter to sort articles by; modified or created

## Adding Content

Since Cling.py is built on top of Tornadoweb, it makes use of Torando's templating engine and UI modules.

### Page System

Cling.py is a Markdown-based application that utilized version 2.2 of the Python Markdown utility. By default pages are stored in the ```page``` directory. Pages stored in the root of the directory (index.md, 404.md) will not show up under any category, but they are accessible via their slug (.com/404 .com/index).

To create a new category simply add a new directory in the ```page``` directory; categories can have sub-categories by using the same process and are probably infinite (didn't test it). When a category is accessed via the url (.com/category), the toc.md page is parsed and shows all of the pages for the given category. This will first check for the existence of an index.md file in that directory and use that instead of the toc.md.

The table of contents page will order files either by date created or date modified as defined in the confif.py and will only consider files that end with ```.md```. Each page listed will also list all of the categories associated with the page.

#### Tornado Module System

Each page is first rendered via the Markdown parser and is passed through the Tornado templating engine supplying the page with request metadata, ui modules, and localization functionality. 

Pages can simply include template logic and it will be parsed before the page is rendered.

```
{{ modules.TOC() }}
```

#License

Licensed under MIT (see LICENSE)