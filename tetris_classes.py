# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 14:22:30 2019

@author: yanbo
"""


import pygame 
#from pygame.sprite import Sprite
import pygame.font
import game_functions as gf
from random import randint



class TetrisShape(): 
    
    def __init__(self,game_settings,screen): 
        self.screen = screen 
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings        
        # configure the size of one elementary block
        self.width = game_settings.block_width
        self.face_color = (255,0,0)
        
        #initialize spaceship and its location 
        self.reset()

    def update(self, game_settings, settled):
        if self.moving_right and not self.reach_right(settled):
            self.left += game_settings.block_speed
        if self.moving_left and not self.reach_left(settled):
            self.left -= game_settings.block_speed        
        if not self.reach_bottom(settled):
            if self.fast_drop:
                self.top += game_settings.drop_speed * 10
            else:
                self.top += game_settings.drop_speed
        
                
            
        self.rect.left = -self.width*(-self.left//self.width)
        self.rect.top  = self.width*(self.top//self.width)
        # print([self.left, self.rect.left, self.bottom, self.rect.bottom])
        
    def reset(self):
        self.rect = pygame.Rect(0,0,self.width, self.width)
        self.shape_code = randint(0,6)
        self.shape_rel_position = gf.shape_coordinates(self.shape_code)  
        self.rect.top = 0
        self.rect.left = self.game_settings.screen_width//2
        self.fast_drop = False
        self.moving_left = False
        self.moving_right = False
        self.top = self.rect.top
        self.left = self.rect.left
        
    
    def draw_shape(self):
        # draw a button filled with color, then draw text
        #self.screen.fill(self.face_color, self.rect)
        edge_width = self.game_settings.block_edge_width
        block_width = self.game_settings.block_width
        block_width_inner = self.game_settings.block_width - 2*edge_width
        for dxdy in self.shape_rel_position:
            shape_left = self.rect.left + block_width*dxdy[0] + edge_width   
            shape_top  = self.rect.top  + block_width*dxdy[1] + edge_width   
            pygame.draw.rect(self.screen, self.face_color,
                             [shape_left, shape_top, block_width_inner, block_width_inner])                              

    def rotate(self,settled):        
        new_rel_position = [list(self.game_settings.rotate_rule[tuple(kxky)]) for kxky in self.shape_rel_position]
        kx0 = round(self.rect.left/self.game_settings.block_width)
        ky0 = round(self.rect.top /self.game_settings.block_width)
        for dxdy in new_rel_position:
            kx, ky = kx0+dxdy[0], ky0+dxdy[1]
            if kx<0 or kx>=settled.bin_num:
                return 
            elif settled.bin[kx][ky] == 1:
                return
        self.shape_rel_position = new_rel_position
    
    def reach_left(self, settled):
        kx0 = round(self.rect.left/self.game_settings.block_width)
        ky0 = round(self.rect.top /self.game_settings.block_width)
        for dxdy in self.shape_rel_position:
            kx, ky = kx0+dxdy[0], ky0+dxdy[1]
            if kx <= 0:
                return True
            elif settled.bin[kx-1][ky] == 1:
                return True
        return False
    
    def reach_right(self, settled):
        kx0 = round(self.rect.left/self.game_settings.block_width)
        ky0 = round(self.rect.top /self.game_settings.block_width)
        for dxdy in self.shape_rel_position:
            kx, ky = kx0+dxdy[0], ky0+dxdy[1]
            if kx >= settled.bin_num-1:
                return True
            elif settled.bin[kx+1][ky] == 1:
                return True
        return False
    
    def reach_bottom(self, settled):
        kx0 = round(self.rect.left/self.game_settings.block_width)
        ky0 = round(self.rect.top /self.game_settings.block_width)
        for dxdy in self.shape_rel_position:
            kx, ky = kx0+dxdy[0], ky0+dxdy[1]        
            if ky >= settled.bin_cap-1:
                return True
            elif settled.bin[kx][ky+1] == 1:
                return True
        return False
        
class Settled():
    
    def __init__(self, game_settings, screen):
        self.game_settings = game_settings  
        self.screen = screen 
        self.face_color = (0,0,255)
        
        block_width = self.game_settings.block_width        
        self.bin_num = self.game_settings.screen_width // block_width
        self.bin_cap = self.game_settings.screen_height // block_width
        self.bin = [[0]*self.bin_cap for _ in range(self.bin_num)]
        
#        self.bin[0][0] = 1
#        self.bin[self.bin_num-1][0] = 1
#        self.bin[0][self.bin_cap-1] = 1
#        self.bin[self.bin_num-1][self.bin_cap-1] = 1
        
        
        self.left = [k*block_width for k in range(self.bin_num)]
        self.top  = [k*block_width for k in range(self.bin_cap)]
        
        #self.draw_settled()
    
    def draw_settled(self):
        edge_width = self.game_settings.block_edge_width
        block_width_inner = self.game_settings.block_width - 2*edge_width
        for kx,col in enumerate(self.bin):
            for ky,element in enumerate(col):
                if element == 1:
                    pygame.draw.rect(self.screen, self.face_color,
                                     [self.left[kx] + edge_width, self.top[ky]+edge_width,
                                      block_width_inner, block_width_inner])
    
    
    def update(self, tetris_shape):
        """merge the tetris_shape to settled"""
        kx0 = round(tetris_shape.rect.left/self.game_settings.block_width)
        ky0 = round(tetris_shape.rect.top /self.game_settings.block_width)
        for dxdy in tetris_shape.shape_rel_position:
            kx, ky = kx0+dxdy[0], ky0+dxdy[1]
            self.bin[kx][ky] = 1
    
    def reset(self):
        self.bin = [[0]*self.bin_cap for _ in range(self.bin_num)]
    
    def wipe_lines(self,sb):
        sums = [ sum([self.bin[l][k] for l in range(self.bin_num)] ) for k in range(self.bin_cap)]
        filled = []
        for k, ele in enumerate(sums):
            if ele == self.bin_num:
                filled.append(k)
        for k in filled:
            for l in range(self.bin_num):                    
                self.bin[l][1:k+1] = self.bin[l][:k]
                self.bin[l][0] = 0                                
        if filled:
            sb.stats.score += self.game_settings.points_multiplier[len(filled)-1] * self.game_settings.points
            sb.prep_score()

class Button():
    
    def __init__(self, game_settings, screen, msg):
        """initialize the property of button"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # configure the size and other properties of button
        self.width, self.height = 200, 50
        self.button_color = (0,255,0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # create rect object of button, put it in the center
        self.rect = pygame.Rect(0,0,self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        self.prep_msg(msg)
        
    def prep_msg(self,msg):
        """ render msg as a figure, and show it in the center of button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        # draw a button filled with color, then draw text
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class GameStats():
    """track the stats of game"""
    
    def __init__(self, game_settings):
        """initialize stats"""
        self.game_active = False
        self.game_settings = game_settings
        with open("highscore.txt","r") as file:
            self.high_score = int(file.read())
        self.reset_stats()
    
    def reset_stats(self):
        """initialize the stats those might change during game"""
        self.score = 0
        self.level = 1  

class Scoreboard():
    """a class to show scoreboard"""
    
    def __init__(self, game_settings, screen, stats):
        """initialize the properties of score"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        self.stats = stats
        
        # set up font
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,32)
        
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        
        # render figure
    
    def prep_score(self):
        rounded_score = int(round(self.stats.score,-1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.game_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def show_score(self):
        # show score on screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        
    def prep_high_score(self):
        high_score = int(round(self.stats.high_score,-1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.game_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.score_rect.right
        self.high_score_rect.top = self.score_rect.bottom + 10
    
    def prep_level(self):
        self.level_image = self.font.render("Level "+str(self.stats.level), True, self.text_color, self.game_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 20
        self.level_rect.top = 20
    
    