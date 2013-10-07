'''
Created on Sep 26, 2011

Core LSystem code.  Responsible for turning production rules into fully realized expansions.

@author: david
'''

import cStringIO as StringIO

class LSystem(object):
    """
    Overview: Represents an LSystem in the form of a set of production rules and the default starting string.
    
    Parameters:
        Rules: dictionary-like object that has a single letter for the key and a string for the rule.  
        Start: default starting string
    """
    def __init__(self, rules, start):
        
        self.rules = dict()
        for key, rule in rules.items():
            self.rules[key.upper()] = rule.upper()
        self.start  = start.upper()
        
    def expand(self, level, start=None):
        """
        Overview: Returns a string representation of the LSystem expanded to the given level.  This could be quite memory intensive and should be used carefully.
        
        Parameters:
            Level: level of iteration to expand the LSystem to.
            Start: starting string to overwrite the one given in the constructor.
        
        Returns: String representing the entire expansion
        
        """
        return "".join( self.expand_iter(level, start) )
        
        
    def expand_iter(self, level, start=None):
        """
        Overview: Returns an iterator that represents the expansion.  Letters are returned one at a time until StopIteration is reached.
        
        Parameters:
            Level: level of iteration to expand the LSystem to.
            Start: starting string to overwrite the one given in the constructor.
        
        Returns: Generator that yields one character of the expansion at a time
        """
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

        