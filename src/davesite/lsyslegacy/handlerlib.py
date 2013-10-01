import HTMLParser
import cStringIO as StringIO

import davesite.lsyslegacy.draw as drawlib
import davesite.lsyslegacy.core as core

def parse_form_input(request):
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
        print key, var, type(var) 
        if len(var.strip()) == 0:
            messages.append("Fill out {0}".format(field_name))
        validated_items[key] = validation_func(var)

    return validated_items, messages

def get_lsystem_drawing(start, productions, angle, step, iterations):
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
    expansion = lsys.expand(iterations)
    color_map = dict(R="red", O="orange", Y="yellow", G="green", B="blue", P="purple", L="black", N="brown")
    ds = drawlib.DrawImage(draw = 'abf', forward='m', left="+", right="-", color_escape='c', color_map=color_map)
    
    f = StringIO.StringIO()
    ds.step = step
    ds.angle = angle
    status = ds.draw(expansion, timeout=0.5)        
    ds.save(f, "PNG")
    
    unrecognized = status['unrecognized']
    messages.extend(status['messages'])
    if len(unrecognized) > 0:
        unrecognized = [ c.encode('ascii', 'xmlcharrefreplace') for c in unrecognized ]
        messages.append("The following commands were not recognized: {0}" .format(  ','.join(unrecognized)  ))
    
    return f.getvalue(), messages



