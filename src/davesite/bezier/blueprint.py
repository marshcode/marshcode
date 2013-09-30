'''
Created on Aug 12, 2013

@author: david
'''

from flask import Blueprint, render_template


bezier = Blueprint('bezier', __name__,
                        template_folder='templates',
                        static_folder = 'static')


@bezier.route('/')
def index():
    return render_template('bezier/index.html')
