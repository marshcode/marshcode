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


logging_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(name)s %(message)s [in %(filename)s:%(lineno)d]')
def initialize_logging():
    """
    Overview: Helper function that will configure logging to the console
    
    Parameters:
        app: Flask application object to enable logging on
        
        """

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging_formatter)
    root_logger.addHandler(stream_handler)

def add_file_logging(file_name, level):
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging_formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)

def initialize_blueprints(app):
    """
    Overview:Helper function to register all necessary blueprints on the given app object
    
    Parameters:
        app: Flask application to register all default blueprints on.
    
    """
    app.register_blueprint(homeblueprint.home_page)
    app.register_blueprint(jlprint.jlp, url_prefix="/jlp")
    app.register_blueprint(bezierblueprint.bezier, url_prefix="/bezier")
    app.register_blueprint(lsyslegblueprint.lsyslegacy, url_prefix="/lsysleg")

def create_app(name='davesite', configuration='Default'):
    """
    Overview: Factory method that is responsible for the following.  Returns the configured Flask app object.
        
            * Reading the configuration.  The configuration is kept in config.py
                
            * Registering the blueprints.  Any blueprints to be added to the application are be added here.     
            
            * Logging: DaveSite uses the built-in python logging module to provide console and file logging.
                       All errors are logged to the console while only warnings and above are logged to the file.
    
    Parameters:
        name:                  package that davesite currently resides under.  
        configuration:         string that points to one of the classes in config.py
        
    Returns: A properly configured Flask application
    """
    app = Flask(name)
    initialize_logging()

    try:
        app.config.from_object('davesite.app.config.{config}'.format(config=configuration))
        initialize_blueprints(app)
    except Exception:
        app.logger.exception("Error while starting app:")
        sys.exit(-1)

    add_file_logging(app.config.get('ERROR_LOG_FILE', 'error.log'), logging.WARN)

    app.wsgi_app = URLPrefixMiddleware(app.wsgi_app, app.config.get('SCRIPT_NAME', '/'))
    return app