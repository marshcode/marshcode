'''
Created on Aug 9, 2013

@author: david
'''
import logging.handlers
import sys

from flask import Flask

from davesite.homepage import blueprint as homeblueprint
from davesite.jlp import blueprint as jlprint

def create_app(name):
    app = Flask(name)
    
    try:
        app.config.from_object('davesite.app.default_config')
        app.config.from_envvar('DAVESITE_CONFIG', silent=True)
    
    
        app.register_blueprint(homeblueprint.home_page)
        app.register_blueprint(jlprint.jlp, url_prefix="/jlp")
    
        if not app.debug:
            logging.basicConfig(filename = app.config['ERROR_LOG_FILE'], level = logging.WARNING,
                                format = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
            
            
        
        def is_dropdown(item):
            return not isinstance(item, basestring)
        menu_items = app.config['MENU']
        @app.context_processor
        def menu_ctx_processor():
            return dict(menu=list(menu_items),
                        is_dropdown = is_dropdown)
    except Exception:
        app.logger.exception("Error while starting app:")
        sys.exit(-1)
    
    return app