'''
Created on Aug 9, 2013

This module handles all application instantiation and configuration.

@author: david
'''
import logging
import sys

from flask import Flask

from davesite.homepage import blueprint as homeblueprint
from davesite.jlp import blueprint as jlprint
from davesite.bezier import blueprint as bezierblueprint
from davesite.lsyslegacy import blueprint as lsyslegblueprint

class URLPrefixMiddleware(object):
    """Middleware used to insert prefixes on any links created with flask.url_for
       The application configuration must contain a variable SCRIPT_NAME that equals the desired prefix.   
    """
    def __init__(self, app, prefix):
        """
        app: WSGI application to prefix.
        prefix: The url prefix to use
        """
        self.app = app
        self.prefix = prefix
        
    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = self.prefix
        return self.app(environ, start_response)

def handle_menu(app):
    """Helper method that reads the menu structure out of the configuration and defines a few template oriented methods
    used during rendering"""
    def is_dropdown(item):
        return not isinstance(item, basestring)
    menu_items = app.config['MENU']
    @app.context_processor
    def menu_ctx_processor():
        return dict(_menu=list(menu_items),
                    is_dropdown = is_dropdown)

def handle_logging(app):
    """Helper function that will configure logging to the console and to a file"""
    logging.basicConfig(filename = app.config['ERROR_LOG_FILE'], level = logging.DEBUG,
                        format = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')     
    
    root_logger = logging.getLogger()
    root_logger.handlers[0].setLevel(logging.WARNING) #[0] is the file handler
    
    stream_handler = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(stream_handler)


def handle_blueprints(app):
    """Helper function to register all necessary blueprints on the given app object"""
    app.register_blueprint(homeblueprint.home_page)
    app.register_blueprint(jlprint.jlp, url_prefix="/jlp")
    app.register_blueprint(bezierblueprint.bezier, url_prefix="/bezier")
    app.register_blueprint(lsyslegblueprint.lsyslegacy, url_prefix="/lsysleg")

def create_app(name='davesite', environmental_config="DAVESITE_CONFIG"):
    """Factory method that is responsible for the following:
        
    * Reading the configuration.  Two configuration vectors are provided:
        1)  A default configuration file in the source tree provides sensible defaults
        2)  An environmental variable that points to a valid configuration file.
        
    * Registering the blueprints.  Any blueprints to be added to the application are be added here.     
    
    * Logging: DaveSite uses the built-in python logging module to provide console and file logging.
               All errors are logged to the console while only warnings and above are logged to the file.
               
    * Menu:  The menu structure seen in the header bar is defined in the configuration file.  The structure and any helper functions are setup and injected 
             into the templating engine here.
    
    name:                  package that davesite currently resides under.  
    environmental_config:  environmental variable that points to a valid configuration file.
    """
    app = Flask(name)
    
    try:
        app.config.from_object('davesite.app.default_config')
        app.config.from_envvar(environmental_config, silent=True)
    
        handle_blueprints(app)
        
        if not app.debug:
            handle_logging(app)
            
        handle_menu(app)
    
    except Exception:
        app.logger.exception("Error while starting app:")
        sys.exit(-1)
    
    app.wsgi_app = URLPrefixMiddleware(app.wsgi_app, app.config.get('SCRIPT_NAME', '/'))
    return app