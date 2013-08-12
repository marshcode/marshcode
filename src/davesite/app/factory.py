'''
Created on Aug 9, 2013

@author: david
'''


from flask import Flask

from davesite.homepage import blueprint as homeblueprint


def create_app(name):
    app = Flask(name)
    
    app.register_blueprint(homeblueprint.home_page)
    
    return app