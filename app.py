import pygame, sys, random
from pygame.locals import *
from sprite import Sprite
pygame.init()
 

# Colours
BACKGROUND = (255, 255, 255)

FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')

sailor_idle = Sprite("Assets/Sprites/Sailor.png")
sailor_anim1= Sprite("Assets/Sprites/Sailor1.png")

plater_sprites = [sailor_idle, sailor_anim1]

# The main function that controls the game
def main () :
  looping = True
  startpos = 550
  xpos = startpos
  movementAmount = 120

  currentanim_index = 0
  # The main game loop
  while looping :
    # Get inputs
    for event in pygame.event.get() :
      if event.type == pygame.QUIT :
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == K_a:
            if xpos > startpos - movementAmount:
                xpos -= movementAmount
        if event.key == K_d:
            if xpos < startpos + movementAmount:
                xpos += movementAmount
    #keys = pygame.key.get_pressed()
    # if keys[pygame.K_a]:
    #     xpos -= 80
    # if keys[pygame.K_d]:
    #     xpos += 80
    draw_window(xpos, currentanim_index)
   


def draw_window(xpos, currentanim_index):
    WINDOW.fill(BACKGROUND)
    WINDOW.blit(sailor_idle.get_sprite(), (xpos, 200))
    currentanim_index += 1
    if currentanim_index >= len(plater_sprites):
       currentanim_index = 0
    animate_sailor(xpos, plater_sprites[currentanim_index])
    pygame.display.update()
    fpsClock.tick(FPS)
 
def animate_sailor(xpos, currentSprite):
    print(currentSprite)
    WINDOW.blit(currentSprite.get_sprite(), (xpos, 200))


main()