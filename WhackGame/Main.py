import pygame
import GameCore

######### INIT #################### 

pygame.init()
pygame.mixer.init()
g_end_game = False

GameCore.initGame()

clock = pygame.time.Clock()
GameCore.testfunc()

######## MAIN LOOP ################

#sounda= pygame.mixer.Sound("Resource/explosion.flac")

while not g_end_game:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            g_end_game = True # Flag that we are done so we exit this loop
        if (event.type == pygame.KEYDOWN):
            #sounda.play()
            m = 1
            
        if (event.type == pygame.MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            GameCore.click(pos)
    # --- Game logic should go here
 
    # --- Drawing code should go here
    
    GameCore.render()

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    
    

    # --- Limit to 60 frames per second
    clock.tick(60)

