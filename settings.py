# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 21:50:17 2019

@author: yanbo
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 16:37:01 2019

@author: yanbo
"""

class Settings(object): 
    """docstring for Settings""" 
    def __init__(self): 
        # initialize setting of game 
        
        # static settings
        
        # screen setting         
        self.screen_width = 400 
        self.screen_height = 800 
        self.bg_color = (230,230,230)
        
        # block setting 
        self.block_width = 20
        self.block_edge_width = 1
        self.block_speed = self.block_width/100.0
        
        # shape setting 
        self.settled_buffer = 0
        self.settled_buffer_max = 100
        
        
        # rotate rules
        self.rotate_rule = {(0,0):(0,0),
                            (1,0):(0,-1),(0,-1):(-1,0),(-1,0):(0,1),(0,1):(1,0),
                            (1,1):(1,-1),(1,-1):(-1,-1),(-1,-1):(-1,1),(-1,1):(1,1),
                            (2,0):(0,-2),(0,-2):(-2,0),(-2,0):(0,2),(0,2):(2,0),
                            (3,0):(0,-3),(0,-3):(-3,0),(-3,0):(0,3),(0,3):(3,0)}
       
        self.points_multiplier = [1, 3, 6, 10]
        
        # dynamic settins
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """ initialize settings changing with time"""        
        self.drop_speed = self.block_width /400.0     
        # fleet_direction = 1 for right moving, -1 for left moving
        self.points = 100
    
    def increase_speed(self):
        self.drop_speed *= self.speedup_scale
        self.points = int(self.points * self.score_scale)
        
        
        
        
