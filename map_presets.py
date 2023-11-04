'''
Writers: Kenrick Zhang, Dickson Zhao
Date: 21/01/2023
Description: A Pygame which features an Orange and Blue player who battle each other with magic blasts and portals.
'''

# import pygame to load the sounds and images
import pygame


def load_map(map):
  ''' takes string map as parameter - a series of if blocks that, if the map parameter matches one of the names of the maps, returns the environment-specific music, background images and platform images in the form of pygame image loads '''

  # environment_variables = [background_music, background_image, platform1_image, platform2_image, platform3_image, platform4_image]

  # if the lab map was selected
  if map == "lab":

    # return the lab-specific assets
    return [
      pygame.mixer.Sound("sounds/lab_music.mp3"),
      pygame.image.load("environment/lab_image.jpg"),
      pygame.image.load("environment/lab_platform1.png"),
      pygame.image.load("environment/lab_platform2.png")
    ]

  # if the cave map was selected
  elif map == "cave":
    return [
      pygame.mixer.Sound("sounds/cave_music.mp3"),
      pygame.image.load("environment/cave_image.jpg"),
      pygame.image.load("environment/cave_platform1.png"),
      pygame.image.load("environment/cave_platform2.png")
    ]

  # if the cosmic map was selected
  elif map == "cosmic":

    # return the cosmic-specific assets
    return [
      pygame.mixer.Sound("sounds/cosmic_music.mp3"),
      pygame.image.load("environment/cosmic_image.jpg"),
      pygame.image.load("environment/cosmic_platform1.png"),
      pygame.image.load("environment/cosmic_platform2.png")
    ]

  # if the desert map was selected
  elif map == "desert":

    # return the desert-specific assets
    return [
      pygame.mixer.Sound("sounds/desert_music.mp3"),
      pygame.image.load("environment/desert_image.jpg"),
      pygame.image.load("environment/desert_platform1.png"),
      pygame.image.load("environment/desert_platform2.png")
    ]

  # if the ocean map was selected
  elif map == "ocean":

    # return the ocean-specific assets
    return [
      pygame.mixer.Sound("sounds/ocean_music.mp3"),
      pygame.image.load("environment/ocean_image.jpg"),
      pygame.image.load("environment/ocean_platform1.png"),
      pygame.image.load("environment/ocean_platform2.png")
    ]

  # if the sky map was selected
  elif map == "sky":

    # return the sky-specific assets
    return [
      pygame.mixer.Sound("sounds/sky_music.mp3"),
      pygame.image.load("environment/sky_image.jpg"),
      pygame.image.load("environment/sky_platform1.png"),
      pygame.image.load("environment/sky_platform2.png")
    ]
