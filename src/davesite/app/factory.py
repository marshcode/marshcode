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
    """
        Overview: Middleware used to insert prefixes on any links created with flask.url_for  
    """
    def __init__(self, app, prefix):
        """
        Overview:
        
        Parameters:
            app: WSGI application to prefix.
            prefix: The url prefix to use
        """
        self.app = app
        self.prefix = prefix
        
    def __call__(self, environ, start_response):
        """
        Overview: process the wsgi request object
        
        Parameters:
            environ:         wsgi environment object
            start_response:  wsgi response object
        
        Returns: response of the original wsgi app
            
        """
        environ['SCRIPT_NAME'] = self.prefix
        return self.app(environ, start_response)

def handle_logging(app):
    """
    Overview: Helper function that will configure logging to the console and to a file
    
    Parameters:
        app: Flask application object to enable logging on
        
        """
    logging.basicConfig(filename = app.config['ERROR_LOG_FILE'], level = logging.DEBUG,
                        format = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')     
    
    root_logger = logging.getLogger()
    root_logger.handlers[0].setLevel(logging.WARNING) #[0] is the file handler
    
    stream_handler = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(stream_handler)


def handle_blueprints(app):
    """
    Overview:Helper function to register all necessary blueprints on the given app object
    
    Parameters:
        app: Flask application to register all default blueprints on.
    
    """
    app.register_blueprint(homeblueprint.home_page)
    app.register_blueprint(jlprint.jlp, url_prefix="/jlp")
    app.register_blueprint(bezierblueprint.bezier, url_prefix="/bezier")
    app.register_blueprint(lsyslegblueprint.lsyslegacy, url_prefix="/lsysleg")

def create_app(name='davesite', environmental_config="DAVESITE_CONFIG"):
    """
    Overview: Factory method that is responsible for the following.  Returns the configured Flask app object.
        
            * Reading the configuration.  Two configuration vectors are provided:
                1)  A default configuration file in the source tree provides sensible defaults
                2)  An environmental variable that points to a valid configuration file.
                
            * Registering the blueprints.  Any blueprints to be added to the application are be added here.     
            
            * Logging: DaveSite uses the built-in python logging module to provide console and file logging.
                       All errors are logged to the console while only warnings and above are logged to the file.
                       
            * Menu:  The menu structure seen in the header bar is defined in the configuration file.  The structure and any helper functions are setup and injected 
                     into the templating engine here.
    
    Parameters:
        name:                  package that davesite currently resides under.  
        environmental_config:  environmental variable that points to a valid configuration file.
        
    Returns: A properly configured Flask application
    """
    app = Flask(name)
    
    try:
        app.config.from_object('davesite.app.default_config')
        app.config.from_envvar(environmental_config, silent=True)
    
        handle_blueprints(app)
        
        if not app.debug:
            handle_logging(app)
    
    except Exception:
        app.logger.exception("Error while starting app:")
        sys.exit(-1)
    
    app.wsgi_app = URLPrefixMiddleware(app.wsgi_app, app.config.get('SCRIPT_NAME', '/'))
    return app