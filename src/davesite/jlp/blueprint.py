'''
Created on Aug 12, 2013

@author: david
'''

from flask import Blueprint, render_template


jlp = Blueprint('jlp', __name__,
                        template_folder='templates',
                        static_folder = 'static')


@jlp.route('/')
def index():
    return render_template('jlp/index.html')
