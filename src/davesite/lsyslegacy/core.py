'''
Created on Sep 26, 2011

@author: david
'''

import cStringIO as StringIO

class LSystem(object):
    
    def __init__(self, rules, start):
        
        self.rules = dict()
        for key, rule in rules.items():
            self.rules[key.upper()] = rule.upper()
        self.start  = start.upper()
        
    def expand(self, level, start=None):
        return "".join( self.expand_iter(level, start) )
        
        
    def expand_iter(self, level, start=None):
        start = self.start if start is None else start
        for i in self._expand(level, start.upper()):
            yield i
        
    def _expand(self, level, the_string):
        
        if level == 0:
            for i in the_string: yield i
            return

        for l in the_string:
            if l in self.rules:
                for i in self._expand(level - 1, self.rules[l]): yield i
            else:
                yield l

        