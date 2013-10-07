'''
Created on Aug 12, 2013

Blueprints and handler methods for the Bezier Curve Viewer.

Most of the work is done in templates/bezier/index.html.  Future work will see server side code loading and saving curves

@author: david
'''

from flask import Blueprint, render_template


bezier = Blueprint('bezier', __name__,
                        template_folder='templates',
                        static_folder = 'static')


@bezier.route('/')
def index():
    return render_template('bezier/index.html')
