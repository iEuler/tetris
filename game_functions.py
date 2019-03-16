# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 22:22:47 2019

@author: yanbo
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 16:59:51 2019

@author: yanbo
"""
import sys
import pygame

def check_keydown_events(game_settings, screen, stats, event, tetris_shape, settled):
    if event.key == pygame.K_RIGHT: 
        #move right 
        tetris_shape.moving_right = True
    elif event.key == pygame.K_LEFT: 
        #move left 
        tetris_shape.moving_left = True
    elif event.key == pygame.K_DOWN: 
        tetris_shape.fast_drop = True
    elif event.key == pygame.K_SPACE:
        #rotate
        tetris_shape.rotate(settled)        
    elif event.key == pygame.K_q:
        #quit game
        write_highscore_to_file(stats)
        sys.exit()
    elif event.key == pygame.K_p:
        #start a new game
        #start_game(game_settings,screen,stats, blocks, settled)
        pass

def check_keyup_events(game_settings, screen, event, tetris_shape):
    if event.key == pygame.K_RIGHT:
        tetris_shape.moving_right = False
    elif event.key == pygame.K_LEFT:
        tetris_shape.moving_left = False
    elif event.key == pygame.K_DOWN:
        tetris_shape.fast_drop = False
                
def check_events(game_settings,screen,stats,sb,tetris_shape, settled,play_button): 
    #respond to  keyboard and mouse item 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            sys.exit()        
        elif event.type == pygame.KEYDOWN: 
            check_keydown_events(game_settings, screen, stats, event, tetris_shape, settled)            
        elif event.type == pygame.KEYUP:
            check_keyup_events(game_settings, screen, event, tetris_shape)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #print([mouse_x, mouse_y])
            check_play_button(game_settings,screen,stats,sb, tetris_shape, settled, play_button, mouse_x, mouse_y)

def check_play_button(game_settings,screen,stats, sb, tetris_shape, settled, play_button, mouse_x, mouse_y):
    """start a new game when player clicks the play button"""
    # button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        start_game(game_settings,screen,stats,sb, tetris_shape, settled)
            
def start_game(game_settings,screen,stats,sb, tetris_shape, settled):
    """Start a new game"""
    if not stats.game_active:
        # reset settings
        # game_settings.initialize_dynamic_settings()
        # reset stats
        stats.reset_stats()
        stats.game_active = True
        
        settled.reset() 
        tetris_shape.reset()
        
        # reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()        
#        
        
        # hide the mouse
        pygame.mouse.set_visible(False)
        
def shape_coordinates(shape_code):
    # shape_code =0 for square, = 1 for L shape, =2 for reverse L shape, =3 for T shape
    # = 4 for z shape, =5 for s shape, =6 for line shape
    if shape_code == 0:
        return [[0,0],[0,1],[1,0],[1,1]]
    elif shape_code == 1:
        return [[0,0],[0,1],[1,0],[2,0]]
    elif shape_code == 2:
        return [[0,0],[0,1],[-1,0],[-2,0]]
    elif shape_code == 3:
        return [[0,0],[0,1],[1,0],[-1,0]]
    elif shape_code == 4:
        return [[0,0],[0,1],[-1,0],[1,1]]
    elif shape_code == 5:
        return [[0,0],[0,1],[1,0],[-1,1]]
    elif shape_code == 6:
        return [[0,0],[0,1],[0,2],[0,3]]



def update_shape(game_settings,screen,sb,tetris_shape,settled):
    tetris_shape.update(game_settings, settled)    
    event_reach_bottom(game_settings, screen,sb,tetris_shape, settled)
        
    
            
def update_screen(game_settings,screen,stats, sb, tetris_shape,settled,play_button): 
    # fill color 
    
    screen.fill(game_settings.bg_color) 
    tetris_shape.draw_shape()
    settled.draw_settled()
    sb.show_score()
    
    if not stats.game_active:
        play_button.draw_button()    
    pygame.display.flip()
    

def event_reach_bottom(game_settings, screen,sb,tetris_shape, settled):
    """carry out an action if the shape reach bottom"""    
    if tetris_shape.reach_bottom(settled):
        if settled_buffer_done(game_settings):            
            settle_shape(sb,tetris_shape, settled)
            
            

def settle_shape(sb,tetris_shape, settled):
    settled.update(tetris_shape) 
    settled.wipe_lines(sb)    
    tetris_shape.reset()

def settled_buffer_done(game_settings):
    if game_settings.settled_buffer >= game_settings.settled_buffer_max:
        game_settings.settled_buffer = 0
        return True
    else:
        game_settings.settled_buffer += 1
        return False

def write_highscore_to_file(stats):
    if stats.score==stats.high_score:
        with open("highscore.txt","w") as file:
            file.write(str(stats.high_score))