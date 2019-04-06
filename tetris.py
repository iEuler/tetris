# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 21:47:50 2019

@author: yanbo
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 16:32:41 2019

@author: yanbo
"""

import pygame
from settings import Settings
import game_functions as gf
import tetris_classes as tc


def run_game():
    # initialize game and create a display object
    pygame.init() 
    pygame.display.set_caption("Tetris") 
    
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    stats = tc.GameStats(game_settings)
    sb = tc.Scoreboard(game_settings, screen, stats)
    # create a play button
    play_button = tc.Button(game_settings, screen, "Play")

    tetris_shape = tc.TetrisShape(game_settings, screen)
    settled = tc.Settled(game_settings, screen)
    
    # game loop     
    while True: 
        # supervise keyboard and mouse item 
        gf.check_events(game_settings, screen, stats, sb, tetris_shape, settled, play_button)
        
        if stats.game_active:        
            gf.update_shape(game_settings, screen,sb,tetris_shape, settled)        

        gf.update_screen(game_settings,screen,stats,sb,tetris_shape,settled,play_button)
        
        
run_game()
