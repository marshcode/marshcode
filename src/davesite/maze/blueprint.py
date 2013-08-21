'''
Created on Aug 20, 2013

@author: david
'''
'''
Created on Aug 12, 2013

@author: david
'''

from flask import Blueprint, render_template


maze = Blueprint('maze', __name__,
                        template_folder='templates',
                        static_folder = 'static')


@maze.route('/')
def index():
    return render_template('maze/index.html')
