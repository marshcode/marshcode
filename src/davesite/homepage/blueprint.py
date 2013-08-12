'''
Created on Aug 11, 2013

@author: david
'''
from flask import Blueprint, render_template


home_page = Blueprint('home', __name__,
                        template_folder='templates')


@home_page.route('/')
def index():
    return render_template('home/index.html')
