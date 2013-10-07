"""
Request handling library
"""

import HTMLParser
import cStringIO as StringIO

import davesite.lsyslegacy.draw as drawlib
import davesite.lsyslegacy.core as core

def parse_form_input(request):
    """Method to validate the wsgi request object that came from the client.
    
    request: wsgi request object that should have an 'args' dictionary.
    
    returns a tuple of a dictionary with the validated items and a list of generated messages.
    
    """
    h = HTMLParser.HTMLParser()

    validators = dict(start = ("start", h.unescape),
                     productions =  ("productions", lambda s: h.unescape(s).splitlines()),
                     angle       =  ("angle", int),
                     step        =  ("step", int),
                     iterations  =  ("iterations", int)
                    )
    validated_items = {}
    messages = []
    for key, (field_name, validation_func) in validators.items():
        var = request.args.get(key, None)
        if not var:
            messages.append("Did not receive parameter: {0}".format(field_name))
            continue
        if len(var.strip()) == 0:
            messages.append("Fill out {0}".format(field_name))
            continue
        try:
            validated_items[key] = validation_func(var)
        except:
            messages.append("Invalid {0} value: {1}".format(field_name, var))

    return validated_items, messages

def get_lsystem_drawing(start, productions, angle, step, iterations):
    """Take all information given by the client and return a PIL image and a list of messages
    
    start:       string representing the start string.
    productions: dictionary of rules representing the LSystem.
    angle:       angle to rotate (in degrees) when rotating left or right.
    iterations:  number of iterations to run through.
    
    """
    production_rules = dict()
    messages = []
    
    for raw_rule in productions:
        raw_rule = raw_rule.strip()
        try:
            if raw_rule.startswith('#') or len(raw_rule) == 0: continue
            key, rule = raw_rule.split('=')
            production_rules[key] = rule
            if not key.isalnum():
                messages.append("Warning: Rule is '{0}'.  All rules should be letters.".format(key))
        except Exception:
            messages.append( "Error parsing rule: {0}".format(raw_rule) )

    lsys = core.LSystem(production_rules, 
                        start=start)
    expansion = lsys.expand_iter(iterations)
    color_map = dict(R="red", O="orange", Y="yellow", G="green", B="blue", P="purple", L="black", N="brown")
    ds = drawlib.DrawImage(draw = 'abf', forward='m', left="+", right="-", color_escape='c', color_map=color_map)
    
    f = StringIO.StringIO()
    ds.step = step
    ds.angle = angle
    status = ds.draw(expansion, timeout=2)        
    ds.save(f, "PNG")
    
    unrecognized = status['unrecognized']
    messages.extend(status['messages'])
    if len(unrecognized) > 0:
        unrecognized = [ c.encode('ascii', 'xmlcharrefreplace') for c in unrecognized ]
        messages.append("The following commands were not recognized: {0}" .format(  ','.join(unrecognized)  ))
    
    return f.getvalue(), messages



