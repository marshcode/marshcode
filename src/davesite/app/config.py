__author__ = 'david'

from davesite.templates.widgets import HeaderLink

class Default(object):
    # enable flask debug mode.  If this is active, the python logging system will not be configured
    DEBUG = False

    # Log file containing warnings and above.  It is reccomended that this be an absolute path in the second config file
    ERROR_LOG_FILE = "davesite.error.log"

    # Script location on the server (relative to the root).  Use this to adjust the prefix created by flask.url_for
    SCRIPT_NAME = '/'

    HEADER_LINKS = dict()

class MarshCode(Default):
    SCRIPT_NAME = '/projects'

    HEADER_LINKS = dict(bezier=HeaderLink('Project Writeup', '/?page_id=117'))