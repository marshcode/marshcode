'''
Created on Aug 9, 2013

@author: david
'''


from flask import Flask

from davesite.homepage import blueprint as homeblueprint
from davesite.jlp import blueprint as jlprint
from davesite.maze import blueprint as mazeprint

def create_app(name):
    app = Flask(name)
    
    app.register_blueprint(homeblueprint.home_page)
    app.register_blueprint(jlprint.jlp, url_prefix="/jlp")
    app.register_blueprint(mazeprint.maze, url_prefix="/maze")
    
    return app