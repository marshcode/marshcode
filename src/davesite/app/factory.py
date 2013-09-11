'''
Created on Aug 9, 2013

@author: david
'''


from flask import Flask

from davesite.homepage import blueprint as homeblueprint
from davesite.jlp import blueprint as jlprint

from davesite.app import menu

def create_app(name):
    app = Flask(name)
    app.config.from_object('davesite.app.default_config')
    
    
    app.register_blueprint(homeblueprint.home_page)
    app.register_blueprint(jlprint.jlp, url_prefix="/jlp")
        
    menu_items = menu.read_menu()
    @app.context_processor
    def menu_ctx_processor():
        
        def is_dropdown(item):
            return hasattr(item,'keys')
        
        return dict(menu=menu_items,
                    is_dropdown = is_dropdown)
    
    return app