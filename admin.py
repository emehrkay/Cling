#!/usr/bin/env python
# encoding: utf-8
"""
admin.py

Created by mark henderson on 2013-01-12.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import config
from tornado.options import options

class Theme(object):
    usage = 'admin.py theme [enable|disable] theme_name'
    
    def __init__(self, name):
        self.name = name
        self.source = os.path.join(options.site_root, options.theme_dir, self.name, 'static')
        self.dest = os.path.join(options.site_root, options.static_dir, self.name)
    
    def enable(self):
        if not os.path.lexists(self.dest):
            os.symlink(self.source, self.dest)
            return 'Theme: %s enabled' % self.name
        else:
            raise Exception('Theme: %s is already enabled' % self.name)
    
    def disable(self):        
        if os.path.lexists(self.dest):
            os.unlink(self.dest)
            return 'Theme: %s disabled' % self.name
        else:
            raise Exception('Theme: %s is not enabled' % self.name)
    

def get_help():
    return """
    Usage:
    
        Theme management:
            %s
    """ % (Theme.usage)


if __name__ == '__main__':
    try:
        args = sys.argv
        
    	if len(args) < 4 or args[1] != 'theme' or args[2] not in ['enable', 'disable']:
    	    print get_help()
    	else:
    	    theme = Theme(args[3])
    	    print getattr(theme, args[2])()
    except Exception, e:
        print e
        
