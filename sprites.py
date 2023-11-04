'''
Writers: Kenrick Zhang, Dickson Zhao
Date: 21/01/2023
Description: A Pygame which features an Orange and Blue player who battle each other with magic blasts and portals.
'''

# import required packages, libraries and modules
import pygame
import random


# create the collision box class
class CollisionBox(pygame.sprite.Sprite):
  ''' instantiates a pygame sprite object as a rectangular box sprite with the size and around the position of the sprite '''

  def __init__(self, x, y, width, height):
    ''' takes integer x, integer y, integer width, and integer height as parameters - creates a rectangular sprite collision box with the size and position of the respective parameters '''

    # creates a pygame rect with the size and position of the respective parameters
    self.__rect = pygame.Rect(x, y, width, height)

  def collides_with(self, other):
    ''' takes pygame rect other as parameter - returns a boolean value based on whether the object's and the other rect intersect each other at some point '''

    # return whether the rects of both objects collide
    return self.__rect.colliderect(other.get_rect())

  # get method below the rects of the collision box objects
  def get_rect(self):
    return self.__rect


class Platform(pygame.sprite.Sprite):
  ''' instantiates a pygame sprite object with a position, size, image, a boolean collides_bottom attrbibute determining whether the player can jump through it, and its own collision_box object '''

  def __init__(self, x, y, width, height, image, collides_bottom):
    ''' initializes position, size, image, and collides_bottom attributes of the platform '''

    # initialize position and size of platform
    self.__x = x
    self.__y = y
    self.__width = width
    self.__height = height

    # load image of platform
    self.__image = image

    # create platform's own collision_box object with platform's position and size as arguments
    self.__collision_box = CollisionBox(x, y, width, height)

    # set the platform's collides_bottom attribute depending on whether players should be able to jump through
    self.__collides_bottom = collides_bottom

  # get methods below for their respective attributes
  def get_collision_box(self):
    return self.__collision_box

  def get_pos(self):
    return self.__x, self.__y

  def get_image(self):
    return self.__image

  def get_collides_bottom(self):
    return self.__collides_bottom

  def get_size(self):
    return self.__width, self.__height


class Explosion(pygame.sprite.Sprite):
  ''' instantiates an explosion pygame sprite object with a position and list of images to form a complete pixelated explosion animation '''

  def __init__(self, x, y, screen):
    ''' initialize explosion object with parameters x, y, and the screen '''

    # adding explosions will not work without the below statement, or unless explicitly specifying Player().__init__() subclass method instead of Explosion.__init__()
    super().__init__()

    # load and set the volume of the explosion sound
    self.__explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")
    self.__explosion_sound.set_volume(0.5)

    # load the first frame of the explosion sprite
    self.__image = pygame.image.load("explosion_anims/explosion1.png")

    # set the rect attribute to the size of the image
    self.__rect = self.__image.get_rect()

    # set some variables offset by the size of the explosion relative to the player
    self.__x = x - 390
    self.__y = y - 280

    # initialize the animation of the explosion to the first frame
    self.__anim_cycle = 0

  def update(self, player_list, screen, all_sprites, screen_width):
    ''' takes player_list, screen, all_sprites and screen_width parameters - cycles through each frame of the explosion and plays an explosion sound'''

    # set the collision box of the explosion to the collision box of the explosion image
    self.__hitbox = pygame.Rect(self.__rect.x, self.__rect.y,
                                self.__rect.width, self.__rect.height)

    # draw the explosion's hitbox (should only be enabled for debugging)
    pygame.draw.rect(screen, (255, 0, 0), self.__hitbox)

    # stores the names of all the explosion sprite images in the /images/ directory into an explosion_sprites tuple
    explosion_sprites = (
      "explosion_anims/explosion1.png",
      "explosion_anims/explosion1.png",
      "explosion_anims/explosion2.png",
      "explosion_anims/explosion2.png",
      "explosion_anims/explosion3.png",
      "explosion_anims/explosion3.png",
      "explosion_anims/explosion4.png",
      "explosion_anims/explosion4.png",
      "explosion_anims/explosion5.png",
      "explosion_anims/explosion5.png",
      "explosion_anims/explosion6.png",
      "explosion_anims/explosion6.png",
      "explosion_anims/explosion7.png",
      "explosion_anims/explosion7.png",
      "explosion_anims/explosion8.png",
      "explosion_anims/explosion8.png",
      "explosion_anims/explosion9.png",
      "explosion_anims/explosion9.png",
      "explosion_anims/explosion10.png",
      "explosion_anims/explosion10.png",
      "explosion_anims/explosion11.png",
      "explosion_anims/explosion11.png",
      "explosion_anims/explosion12.png",
      "explosion_anims/explosion12.png",
      "explosion_anims/explosion13.png",
      "explosion_anims/explosion13.png",
      "explosion_anims/explosion14.png",
      "explosion_anims/explosion14.png",
    )

    # each time update() is called, the explosion object's image is set to the next in the cycle
    self.__image = pygame.image.load(explosion_sprites[self.__anim_cycle])

    # set the explosion object's image to a transformed version of itself
    self.__image = pygame.transform.scale(self.__image, (900, 434))

    # if the animation cycle is at 0
    if not self.__anim_cycle:

      # play the explosion sound once when the explosion object is instantiated
      self.__explosion_sound.play()

    # increment the explosion object's animation cycle by 1
    self.__anim_cycle += 1

    # if the animation is over
    if self.__anim_cycle > 27:

      # kill the explosion object
      self.kill()

  # get methods below for their respective attributes
  def get_image(self):
    return self.__image

  def get_pos(self):
    return self.__x, self.__y


class Portal(pygame.sprite.Sprite):
  ''' instantiates a portal pygame sprite object with a position, colour, direction, and size that teleports the player of the same colour whenever they collide with the portal object '''

  def __init__(self, x, y, colour, direction, width, height, screen_width,
               starting_health):

    # adding portals will not work without the below statement, or unless explicitly specifying Player().__init__() subclass method instead of Portal.__init__()
    super().__init__()

    # initialize and set volumes of orange and blue blast sounds
    orange_blast_sound = pygame.mixer.Sound("sounds/o_blast.mp3")
    blue_blast_sound = pygame.mixer.Sound("sounds/b_blast.mp3")
    orange_blast_sound.set_volume(0.1)
    blue_blast_sound.set_volume(0.1)

    # initialize and set the volume of the sound when a player travels through the portal
    self.__hit_sound = pygame.mixer.Sound("sounds/blast_hit.mp3")
    self.__hit_sound.set_volume(0.1)

    # if the portal is orange
    if colour == 'o':

      # set the portal's image to an orange portal
      self.image = pygame.image.load("images/o_portal.png")

      # play the orange portal's sound effect
      orange_blast_sound.play()

    # if the portal is not orange (blue)
    else:

      # set the portal's image to a blue portal
      self.image = pygame.image.load("images/b_portal.png")

      # play the blue portal's sound effect
      blue_blast_sound.play()

    # if the portal was shot to the left
    if direction == "left":

      # set the portal's position on the left wall
      x = 0

    # if the portal was not shot to the left (right)
    else:

      # set the portal's position on the right wall
      x = screen_width - width

    # get and store the size of the image
    self.rect = self.image.get_rect()

    # set the position of the portal
    self.rect.x = x
    self.rect.y = y

    # set the size of the portal
    self.__width = width
    self.__height = height

    # set the colour of the portal
    self.__colour = colour

    # set the direction of the portal
    self.__direction = direction

    # set the starting health reference of the players
    self.__starting_health = starting_health

  def update(self, player_list, screen, all_sprites, screen_width,
             score_board):
    ''' takes player_list, screen, all_sprites, and screen_width as parameters - checks for collisions with players and teleports same-coloured players as itself '''

    # for the players in the list of players, player_list
    for player in player_list:
      # if the blast's collision box is within range to hit the player's collision box both vertically and horizontally from the right side
      if self.__direction == "left":
        if (player.get_pos()[1] + player.get_size()[1] >= self.rect.y
            and player.get_pos()[1] <= self.rect.y + self.__height) and (
              player.get_pos()[0] <= self.__width):

          # if the portal was fired by the player of the same colour
          if self.__colour == player.get_colour():

            # teleport player to random coordinates on the map
            player.set_x(random.randint(0, screen_width))
            player.set_y(player.get_size()[1])

            # if adding 20% to the players health wouldnt make them exceed their starting_health
            if player.get_health() <= self.__starting_health * 0.95:

              # recover 10% of the players starting health
              player.set_health(player.get_health() +
                                self.__starting_health / 20)

            # kill the portal object
            self.kill()

            # play the portal hit sound
            self.__hit_sound.play()

      # if the blast's collision box is within range to hit the player's collision box both vertically and horizontally from the left side
      else:
        if (player.get_pos()[1] + player.get_size()[1] >= self.rect.y
            and player.get_pos()[1] <= self.rect.y + self.__height) and (
              player.get_pos()[0] + player.get_size()[0] >=
              screen_width - self.__width):

          # if the portal was fired by the player of the same colour
          if self.__colour == player.get_colour():

            # teleport player to random coordinates on the map
            player.set_x(random.randint(0, screen_width))
            player.set_y(player.get_size()[1])

            # if adding 20% to the players health wouldnt make them exceed their starting_health
            if player.get_health() <= self.__starting_health * 0.95:

              # recover 10% of the players starting health
              player.set_health(player.get_health() +
                                self.__starting_health / 20)

            # kill the portal object
            self.kill()

            # play the blast hit sound
            self.__hit_sound.play()


def draw_health(screen, colour, health, starting_health):
  ''' takes screen, a player's colour, a player's current health, and the starting health of the player as parameters - blits a colour-dependent rectangle indicating the current health of the character '''

  # the orange player
  if colour == "o":

    # if the player's health is in boundaries for the healthbar
    if health <= starting_health:

      # draw the orange player's healthbar with the length representing their remaining health
      pygame.draw.rect(
        screen, (255, 149, 0),
        pygame.Rect(247, 27, (health / starting_health) * 250, 25))

    # if the player's health is not in boundaries for the healthbar
    else:

      # draw just the full orange player's heathbar to avoid overrunning the healthbar, with a slightly lighter colour
      pygame.draw.rect(screen, (255, 181, 0), pygame.Rect(247, 27, 250, 25))

  # the blue player
  else:

    # if the player's health is in boundaries for the healthbar
    if health <= starting_health:

      # draw the blue player's healthbar with the length representing their remaining health
      pygame.draw.rect(
        screen, (0, 47, 255),
        pygame.Rect(753 - (health / starting_health) * 250, 27,
                    (health / starting_health) * 250, 25))

    # if the player's health is not in boundaries for the healthbar
    else:

      # draw just the full blue player's heathbar to avoid overrunning the healthbar, with a slightly lighter colour
      pygame.draw.rect(screen, (0, 79, 255), pygame.Rect(503, 27, 250, 25))


class ScoreKeeper(pygame.sprite.Sprite):
  ''' instantiates a scorekeeper pygame sprite object with score and positional attributes as well as methods to update and draw the scores whenever a blast hits a player '''

  def __init__(self, x, y, x2, y2):
    ''' initializes required score and positional variables for drawing the score text '''

    # initialize both scores at 0
    self.__o_score = 0
    self.__b_score = 0

    # initialize positions for orange and blue score text, respectively
    self.__x = x
    self.__y = y
    self.__x2 = x2
    self.__y2 = y2

  def update(self, colour, screen):
    ''' blits the screen with the respective coloured score text '''

    # set the custom font style and size
    small_font = pygame.font.Font("hippo.ttf", 35)

    # orange player
    if colour == "o":

      # render the text with the orange player's score with the custom font style and size
      text = small_font.render(str(self.__o_score), True, (255, 149, 0))

      # blit orange score text to screen
      screen.blit(text, (self.__x, self.__y))

    # blue player
    else:

      # render the text with the blue player's score with the custom font style and size
      text = small_font.render(str(self.__b_score), True, (0, 79, 255))

      # blit blue score text to screen
      screen.blit(text, (self.__x2, self.__y2))

  def add_score(self, colour, screen):
    ''' increments the appropriate colour parameter score by 1 '''

    # orange player
    if colour == "o":

      # increase orange player's score by 1
      self.__o_score += 1

    # blue player
    else:

      # increase blue player's score by 1
      self.__b_score += 1
