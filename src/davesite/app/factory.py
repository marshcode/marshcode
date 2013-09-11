'''
Created on Aug 9, 2013

@author: david
'''
import logging.handlers
import sys

from flask import Flask

from davesite.homepage import blueprint as homeblueprint
from davesite.jlp import blueprint as jlprint

from davesite.app import menu

def create_app(name):
    app = Flask(name)
    
    try:
        app.config.from_object('davesite.app.default_config')
        app.config.from_envvar('DAVESITE_CONFIG', silent=True)
    
    
        app.register_blueprint(homeblueprint.home_page)
        app.register_blueprint(jlprint.jlp, url_prefix="/jlp")
    
        if not app.debug:
            file_handler = logging.handlers.RotatingFileHandler(app.config['ERROR_LOG_FILE'], "a", 2 * 1024 * 1024, 5)
            file_handler.setLevel(logging.WARNING)
            
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(logging.WARNING)

            app.logger.addHandler(file_handler)
            app.logger.addHandler(stream_handler)
            
        menu_items = menu.read_menu(app.config['MENU_JSON'])
        @app.context_processor
        def menu_ctx_processor():
            
            def is_dropdown(item):
                return not isinstance(item, basestring)
            return dict(menu=menu_items,
                        is_dropdown = is_dropdown)
    except Exception:
        app.logger.exception("Error while starting app:")
        sys.exit(-1)
    
    return app