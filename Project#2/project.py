import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Test Windows")

done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#이미지, 사운드 인풋
background_image = pygame.image.load("space.jpg").convert()
player_image = pygame.image.load("skull.png").convert()
click_sound = pygame.mixer.Sound("laser5.ogg")

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()

    # --- Game logic should go here
    
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.blit(background_image, [0, 0])

    player_position = pygame.mouse.get_pos()
    x = player_position[0]
    y = player_position[1]
 
    # Copy image to screen:
    screen.blit(player_image, [x, y])
    player_image.set_colorkey(BLACK)

    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
