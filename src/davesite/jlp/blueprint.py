'''
Created on Aug 12, 2013

@author: david
'''

from flask import Blueprint, render_template
from davesite.app.common import inject_header_link

jlp = Blueprint('jlp', __name__,
                        template_folder='templates',
                        static_folder = 'static')
inject_header_link(jlp)

@jlp.route('/')
def index():
    return render_template('jlp/index.html')
