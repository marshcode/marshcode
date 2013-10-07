'''
Created on Sept 30, 2013

Legacy LSystem code.  THis code started off as me hacking around one afternoon and it shows.  This code will be updated for security and massive usability 
issues only.  A re-write is planned but there is no timeline.  However, it provides enough functionality to be worth displaying.

Input is taken from the client and handed to the handlerlib where the LSystem is expanded to the desired iteration and drawn using PIL.  Timeouts in the 
drawing handler exist to prevent excessive memory usage. 

The image is base64 encoded and returned to the user along with the list of messages.  Otherwise, the image would have to be cached where it could be loaded
from the client dynamically.  

@author: david
'''
import base64

import davesite.lsyslegacy.handlerlib as handlerlib

from flask import Blueprint, render_template, request


lsyslegacy = Blueprint('lsyslegacy', __name__,
                        template_folder='templates',
                        static_folder = 'static')

######################
#Index
######################

examples = dict(empty  = dict(start='', productions='', angle=90, step=5, iterations=5),
                dragon = dict(start='FX', productions = "X=X+YF\nY=FX-Y", angle=90, step=10, iterations=5),
                plant  = dict(start='++X', productions = "X=F-[[X]+X]+F[+FX]-X\nF=FF", angle=25, step=10, iterations=3),
                plant2 = dict(start='++++F', productions = "F=CGFF-[CN-F+F+F]+[CG+F-F-F]", angle=22, step=10, iterations=3),
                sierpinski = dict(start='A', productions='A=B-A-B\nB=A+B+A', angle=60, step=5, iterations=5),
                koch = dict(start='F', productions='F=F+F-F-F+F', angle=90, step=5, iterations=3),
                snowflake = dict(start='F--F--F', productions="F=F+F--F+F", angle=60, step=5, iterations=3),)


@lsyslegacy.route('/')
def index():
    """Renders the main user interface and pre-populate it with the given example"""
    
    example = examples.get(request.args.get('example'), examples['empty'])
    return render_template('lsyslegacy/index.html', values = example)

#########################
#handler
#########################

@lsyslegacy.route('/handler')
def handler():
    """Handles. validates and returns the image or a list of problems encountered and ways to avoid them."""

    validated_keys, messages = handlerlib.parse_form_input(request)
    img_data = None
    if len(messages) == 0: #do not try to do anything if we got parse errors
        img_data, draw_messages = handlerlib.get_lsystem_drawing(validated_keys["start"], 
                                                                 validated_keys["productions"], 
                                                                 validated_keys["angle"], 
                                                                 validated_keys["step"], 
                                                                 validated_keys["iterations"])
        messages.extend(draw_messages)


    if img_data is not None:
        img_data = base64.encodestring(img_data)
    else:
        img_data = ''   
    return render_template('lsyslegacy/image.html', messages = messages, img = img_data)
    