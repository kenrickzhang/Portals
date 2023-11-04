'''
Writers: Kenrick Zhang, Dickson Zhao
Date: 21/01/2023
Description: A Pygame which features an Orange and Blue player who battle each other with magic blasts and portals.
'''

# import pygame to load the images
import pygame


def get_frames(colour):
  ''' takes string colour as parameter - depending on the colour argument, returns two left and right facing tuples of orange or blue player sprites '''

  # if the colour argument is "o", for orange
  if colour == "o":

    # return the left and right facing orange player sprites
    return (
      pygame.image.load('player_anims/o_left1gun.png'),
      pygame.image.load('player_anims/o_left1gun.png'),
      pygame.image.load('player_anims/o_left1gun.png'),
      pygame.image.load('player_anims/o_left1gun.png'),
      pygame.image.load('player_anims/o_left2gun.png'),
      pygame.image.load('player_anims/o_left2gun.png'),
      pygame.image.load('player_anims/o_left2gun.png'),
      pygame.image.load('player_anims/o_left2gun.png'),
      pygame.image.load('player_anims/o_left3gun.png'),
      pygame.image.load('player_anims/o_left3gun.png'),
      pygame.image.load('player_anims/o_left3gun.png'),
      pygame.image.load('player_anims/o_left3gun.png'),
      pygame.image.load('player_anims/o_left4gun.png'),
      pygame.image.load('player_anims/o_left4gun.png'),
      pygame.image.load('player_anims/o_left4gun.png'),
      pygame.image.load('player_anims/o_left4gun.png'),
      pygame.image.load('player_anims/o_left5gun.png'),
      pygame.image.load('player_anims/o_left5gun.png'),
      pygame.image.load('player_anims/o_left5gun.png'),
      pygame.image.load('player_anims/o_left5gun.png'),
    ), (
      pygame.image.load('player_anims/o_right1gun.png'),
      pygame.image.load('player_anims/o_right1gun.png'),
      pygame.image.load('player_anims/o_right1gun.png'),
      pygame.image.load('player_anims/o_right1gun.png'),
      pygame.image.load('player_anims/o_right2gun.png'),
      pygame.image.load('player_anims/o_right2gun.png'),
      pygame.image.load('player_anims/o_right2gun.png'),
      pygame.image.load('player_anims/o_right2gun.png'),
      pygame.image.load('player_anims/o_right3gun.png'),
      pygame.image.load('player_anims/o_right3gun.png'),
      pygame.image.load('player_anims/o_right3gun.png'),
      pygame.image.load('player_anims/o_right3gun.png'),
      pygame.image.load('player_anims/o_right4gun.png'),
      pygame.image.load('player_anims/o_right4gun.png'),
      pygame.image.load('player_anims/o_right4gun.png'),
      pygame.image.load('player_anims/o_right4gun.png'),
      pygame.image.load('player_anims/o_right5gun.png'),
      pygame.image.load('player_anims/o_right5gun.png'),
      pygame.image.load('player_anims/o_right5gun.png'),
      pygame.image.load('player_anims/o_right5gun.png'),
    )

  # if the colour argument is "b", for blue
  elif colour == "b":

    # return the left and right facing blue player sprites
    return (
      pygame.image.load('player_anims/b_left1gun.png'),
      pygame.image.load('player_anims/b_left1gun.png'),
      pygame.image.load('player_anims/b_left1gun.png'),
      pygame.image.load('player_anims/b_left1gun.png'),
      pygame.image.load('player_anims/b_left2gun.png'),
      pygame.image.load('player_anims/b_left2gun.png'),
      pygame.image.load('player_anims/b_left2gun.png'),
      pygame.image.load('player_anims/b_left2gun.png'),
      pygame.image.load('player_anims/b_left3gun.png'),
      pygame.image.load('player_anims/b_left3gun.png'),
      pygame.image.load('player_anims/b_left3gun.png'),
      pygame.image.load('player_anims/b_left3gun.png'),
      pygame.image.load('player_anims/b_left4gun.png'),
      pygame.image.load('player_anims/b_left4gun.png'),
      pygame.image.load('player_anims/b_left4gun.png'),
      pygame.image.load('player_anims/b_left4gun.png'),
      pygame.image.load('player_anims/b_left5gun.png'),
      pygame.image.load('player_anims/b_left5gun.png'),
      pygame.image.load('player_anims/b_left5gun.png'),
      pygame.image.load('player_anims/b_left5gun.png'),
    ), (
      pygame.image.load('player_anims/b_right1gun.png'),
      pygame.image.load('player_anims/b_right1gun.png'),
      pygame.image.load('player_anims/b_right1gun.png'),
      pygame.image.load('player_anims/b_right1gun.png'),
      pygame.image.load('player_anims/b_right2gun.png'),
      pygame.image.load('player_anims/b_right2gun.png'),
      pygame.image.load('player_anims/b_right2gun.png'),
      pygame.image.load('player_anims/b_right2gun.png'),
      pygame.image.load('player_anims/b_right3gun.png'),
      pygame.image.load('player_anims/b_right3gun.png'),
      pygame.image.load('player_anims/b_right3gun.png'),
      pygame.image.load('player_anims/b_right3gun.png'),
      pygame.image.load('player_anims/b_right4gun.png'),
      pygame.image.load('player_anims/b_right4gun.png'),
      pygame.image.load('player_anims/b_right4gun.png'),
      pygame.image.load('player_anims/b_right4gun.png'),
      pygame.image.load('player_anims/b_right5gun.png'),
      pygame.image.load('player_anims/b_right5gun.png'),
      pygame.image.load('player_anims/b_right5gun.png'),
      pygame.image.load('player_anims/b_right5gun.png'),
    )
