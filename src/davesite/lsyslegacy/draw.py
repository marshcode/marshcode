'''
Created on Sep 26, 2011

@author: david
'''
import itertools
import math
import time

import Image, ImageDraw

class DrawingSystemException(Exception): pass

class DrawingSystem(object):
    
    def __init__(self, draw, forward, left, right, color_escape):
        self.forward_chr = forward.upper() #move forward
        self.left_chr = left.upper()       #turn left
        self.right_chr = right.upper()     #turn right
        self.draw_chr = draw.upper()       #draw forward
        self.push_chr= '['
        self.pop_chr = ']'
        self.color_escape = color_escape.upper()
        
    def set_color_index(self, idx):
        raise NotImplementedError("To Be Implemented in Subclass")
        
    def start(self):
        raise NotImplementedError("To Be Implemented in Subclass")
    def end(self):
        raise NotImplementedError("To Be Implemented in Subclass")
    def error(self):
        raise NotImplementedError("To Be Implemented in Subclass")
    
    def forward(self):
        raise NotImplementedError("To Be Implemented in Subclass")
    def draw_line(self):
        raise NotImplementedError("To Be Implemented in Subclass")
    
    def push(self):
        raise NotImplementedError("To Be Implemented in Subclass")
    def pop(self):
        raise NotImplementedError("To Be Implemented in Subclass")
    
    
    def turn_left(self):
        raise NotImplementedError("To Be Implemented in Subclass")
    def turn_right(self):
        raise NotImplementedError("To Be Implemented in Subclass")
        
    def draw(self, expansion, timeout=None):
        
        unrecognized = set()
        messages = []
        
        start_time = time.time()
        
        self.start()
        expansion = (l for l in expansion)
        for l in expansion:
            l = l.upper()
            if l in self.forward_chr:
                self.forward()
            elif l in self.left_chr:
                self.turn_left()
            elif l in self.right_chr:
                self.turn_right()
            elif l in self.draw_chr:
                self.draw_line()
            elif l in self.push_chr:
                self.push()
            elif l in self.pop_chr:
                self.pop()
            elif l in self.color_escape:
                try:
                    self.set_color_index(expansion.next())
                except StopIteration:
                    messages.append("Bad color specification at the end of the expansion")
                
            elif not l.isalnum():
                unrecognized.add( l )
                
            if timeout is not None and time.time() - start_time > timeout:
                messages.append("Drawing reached timeout at {0:.2} seconds".format(timeout))
                break
                
        self.end()
            
        return dict(unrecognized = unrecognized,
                    messages     = messages)
            
#basis for drawing system (simple turtle graphics position manipulator)
class TurtlePT(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0

        self._stack = []

    def push(self):
        self._stack.append( (self.x, self.y, self.angle)  )
    def pop(self):
        self.x, self.y, self.angle = self._stack.pop()

    def turn_left(self, by):
        self.angle = (self.angle - by) % 360
    def turn_right(self, by):
        self.angle = (self.angle + by) % 360
    def forward(self, by):
        
                
        #effectively translate the coordinate system origin to the reference point by only using
        #the 'by' as the polar radius.  This creates offsets that we apply to the original points.
        #otherwise, changes in orientation swing us wildly from quadrant to quadrant

        c_angle = math.radians( float(self.angle) )
        self.x += by * math.cos(c_angle)
        self.y += by * math.sin(c_angle)
        
class DrawImage(DrawingSystem):
    def __init__(self, draw, forward, left, right, color_escape, color_map):
        DrawingSystem.__init__(self, draw, forward, left, right, color_escape)
        self._im = None
        self.step = 0
        self.angle = 0
        self._turtlePT = TurtlePT(0, 0)
        self._color_map = color_map
        
        self.start()
    def reset(self):
        
        self._lines = []
        self._turtlePT.x = self._min_x = self._max_x = 0
        self._turtlePT.y = self._min_y = self._max_y = 0
        self._turtlePT.angle = 0
        
        self._append_point(new=True) 

    def _append_point(self, new=False):
        if new == True:
            self._lines.append([])
        self._lines[-1].append( ('point', self._turtlePT.x, self._turtlePT.y) )
        
        self._min_x = min(self._min_x, self._turtlePT.x)
        self._max_x = max(self._max_x, self._turtlePT.x)
        
        self._min_y = min(self._min_y, self._turtlePT.y)
        self._max_y = max(self._max_y, self._turtlePT.y)
        
        
    def size(self):
        return self._im.size
    def save(self, filename, filetype='PNG'):
        self._im.save(filename, filetype)
    def show(self):
        self._im.show()
    
    def set_color_index(self, idx):
        self._lines[-1].append( ('color', idx) )
    
    def start(self):
        self.reset()
    def end(self):
        padding = 0.05 #5%
                
        offset_x = math.fabs(self._min_x)
        offset_y = math.fabs(self._min_y)
        
        size_x  = max(self._max_x + offset_x, 1)
        size_y  = max(self._max_y + offset_y, 1)
        
        padding_x = int(size_x * padding)
        padding_y = int(size_y * padding)
        
        size_x += padding_x * 2
        size_y += padding_y * 2
        
        self._im = Image.new("RGB", (int(size_x), int(size_y)), color = "#FFFFFF")
        d = ImageDraw.Draw(self._im)
        
        color = 'black'
        for line in self._lines:
            line_segment = []
            for line_data in line:
                if line_data[0] == 'color':
                    d.line(line_segment, fill=color) 
                    line_segment = [line_segment[-1]]
                    color = self._color_map.get( line_data[1], 'black')
                elif line_data[0] == 'point':
                    line_segment.append( (line_data[1]+offset_x+padding_x, line_data[2]+offset_y+padding_y) )
            d.line(line_segment, fill=color)        
    def error(self): pass
        
    def forward(self):
        self._turtlePT.forward(self.step)
        self._lines.append([])
        
    def draw_line(self):
        self._turtlePT.forward(self.step)
        self._append_point(new=False) 
    
    def turn_left(self):
        self._turtlePT.turn_left(self.angle)
    def turn_right(self):
        self._turtlePT.turn_right(self.angle)

        
    def push(self):
        try:
            self._turtlePT.push()
        except Exception:
            pass
        
    def pop(self):
        try:
            self._turtlePT.pop()
            self._append_point(new=True) 
        except Exception:
            pass