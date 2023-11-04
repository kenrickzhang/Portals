'''
Writers: Kenrick Zhang, Dickson Zhao
Date: 21/01/2023
Description: A Pygame which features an Orange and Blue player who battle each other with magic blasts and portals.
'''

# import required packages, libraries and modules
import pygame
import sprites


class Player(pygame.sprite.Sprite):
  ''' instantiates a pygame sprite object with custom sprites and attributes, a player character, with private attributes typical of a player character '''

  def __init__(self, x, y, width, height, colour, screen_width, screen_height,
               jump_power, frames_tuple_left, frames_tuple_right, direction,
               health, runspeed):
    ''' takes multiple player parameters and initializes them into their respective attributes of the object '''

    # initialize size and position of player
    self.__x = x
    self.__y = y
    self.__width = width
    self.__height = height

    # store all the left and right facing sprite frames
    self.__left_frames = frames_tuple_left
    self.__right_frames = frames_tuple_right

    # store the screen dimensions
    self.__screen_width = screen_width
    self.__screen_height = screen_height

    # assigns the object a rectangular collision box with its size and position
    self.__collision_box = sprites.CollisionBox(x, y, width, height)

    # sets the downwards velocity of the player to 0
    self.__velocity_y = 0

    # initializes the direction of the player to an empty string
    self.__direction = ""

    # sets how fast the player runs and how high the player jumps
    self.__runspeed = runspeed
    self.__jump_power = jump_power

    # sets the colour of the player
    self.__colour = colour

    # sets the sprite animation of the player to the first frame
    self.__anim_cycle = 0

    # initializes the footstep sound into the pygame mixer and sets the volume
    self.__footstep = pygame.mixer.Sound("sounds/footstep.mp3")
    self.__footstep.set_volume(0.2)

    # if this is the orange player
    if colour == "o":
      # load and store the death frame of the orange character
      self.__death_frame = pygame.image.load("player_anims/o_dead.png")
    elif colour == "b":
      self.__death_frame = pygame.image.load("player_anims/b_dead.png")

    # initializes the health of the player as the integer parameter health
    self.__health = health

    # initializes the player being alive
    self.__dead = False

    # initialize the number of blasts the player has fired
    self.__blast_count = 0

    # if the player is currently travelling in the left direction
    if direction == "left":

      # set the image for the player object to a left-facing idle stance
      self.__image = frames_tuple_left[16]

      # set the last direction travelled attribute for the player to left
      self.__last_direction = "left"

    # if the player is not currently travelling the left direction, but to the right
    else:

      # set the image for the player object to a right-facing idle stance
      self.__image = frames_tuple_right[16]

      # set the last direction travelled attribute for the player to right
      self.__last_direction = "right"

  def update(self, platform_list, gravity):
    ''' takes list platform_list and gravity as parameters - performs player functions such as collision checks, sprite image updates, applies velocity '''

    # simulate gravitational acceleration by adding it to the player's y velocity
    self.__velocity_y += gravity

    # set the player's y position based on their y velocity velocity
    self.__y += self.__velocity_y

    # if the player is currently travelling left or right and the player has a verticaly velocity of less than 1.1
    if self.__direction and self.__velocity_y < 1.1:

      # if the player is travelling to the left
      if self.__direction == "left":

        # set the image of the player to the next left facing sprite in order (multiples of 20 because each loop of the animation lasts 20 frames)
        self.__image = self.__left_frames[self.__anim_cycle % 20]

      # if the player is travelling to the right
      elif self.__direction == "right":

        # set the image of the player to the next right facing sprite in order (multiples of 20 because each loop of the animation lasts 20 frames)
        self.__image = self.__right_frames[self.__anim_cycle % 20]

      # add 1 to the order of the animation cycle
      self.__anim_cycle += 1

      # on every 20th animation cycle while the player is alive
      if self.__anim_cycle % 20 == 0 and not self.__dead:

        # play the footstep sound
        self.__footstep.play()

    # if the player is not currently travelling left or right and the player has a verticaly velocity of less than 1.1
    elif not self.__direction and self.__velocity_y < 1.1:

      # if the player last travelled left
      if self.__last_direction == "left":

        # set the image for the player object to a left-facing idle stance
        self.__image = self.__left_frames[16]

      # if the player last travelled right
      elif self.__last_direction == "right":

        # set the image for the player object to a right-facing idle stance
        self.__image = self.__right_frames[16]

    # for all the platforms on the level, stored in the list  platform_list
    for platforms in platform_list:

      # if the player's collision box collides with a platform's collision box, determined with the collides_with() method of the collision_box class with the current platform's own collision_box object as the argument
      if self.__collision_box.collides_with(platforms.get_collision_box()):

        # if the player is currently falling
        if self.__velocity_y > 0.1:

          # set the y position of the player so that they stand atop of the platform
          self.__y = platforms.get_pos()[1] - self.__height

          # set the y velocity of the player to 0 so they dont continuously gain y velocity while standing on a platform
          self.__velocity_y = 0

        # if the current platform's collides_bottom attribute is true
        if platforms.get_collides_bottom():

          # if the player is jumping and they are below the platform
          if self.__velocity_y < 0.1 and self.__y > platforms.get_pos()[1]:

            # set the player's y position to just below the platform
            self.__y = platforms.get_pos()[1] + platforms.get_size()[1]

            # set the y velocity of the player to 0 so they dont continue gaining y velocity while hitting the bottom of a platform
            self.__velocity_y = 0

    # if the middle of the player is past the left side of the screen
    if self.__x < -(self.__width / 2):

      # set the position of the middle of the player to the right side of the screen
      self.__x = self.__screen_width - (self.__width / 2)

    # if the middle of the player is past the right side of the screen
    elif self.__x > self.__screen_width - (self.__width / 2):

      # set the position of the middle of the player to the left side of the screen
      self.__x = -(self.__width / 2)

    # set the position of the player's collision box to the position of the player themself
    self.__collision_box.get_rect().x = self.__x
    self.__collision_box.get_rect().y = self.__y

    # if the player is above or below the viewable area
    if self.__y < -120 or self.__y > self.__screen_height:

      # set the player's y position to half the screen's height, or the middle of the screen
      self.__y = self.__screen_height / 2

    # if the player is dead
    if self.__dead:

      # set the sprite image of the player to its death frame
      self.__image = self.__death_frame

      # disallow the player from moving horizontally by setting their running speed to 0
      self.__runspeed = 0

  def jump(self, infinite_jumping):
    ''' takes boolean infinite_jumping as a parameter - make the player jump if the player is below a certain y velocity or at any y velocity if the infinite_jumping parameter is true '''

    # if the absolute value of the player's velocity is below 1 or the boolean parameter infinite_jumping is true (this can allow for timing-based double jumping)
    if abs(self.__velocity_y) < 1 or infinite_jumping:

      # set y velocity to negative of jump_power so the player travels up the screen
      self.__velocity_y = -self.__jump_power

  # get and set methods below for their respective attributes
  def get_direction(self):
    return self.__direction

  def get_pos(self):
    return self.__x, self.__y

  def get_image(self):
    return self.__image

  def get_health(self):
    return self.__health

  def get_dead(self):
    return self.__dead

  def get_colour(self):
    return self.__colour

  def get_collision_box(self):
    return self.__collision_box

  def get_runspeed(self):
    return self.__runspeed

  def get_blast_count(self):
    return self.__blast_count

  def get_size(self):
    return self.__width, self.__height

  def get_last_direction(self):
    return self.__last_direction

  def set_direction(self, direction):
    self.__direction = direction

  def set_last_direction(self, last_direction):
    self.__last_direction = last_direction

  def set_x(self, x):
    self.__x = x

  def set_y(self, y):
    self.__y = y

  def set_blast_count(self, blast_count):
    self.__blast_count = blast_count

  def set_health(self, health):
    self.__health = health

  def set_dead(self, dead):
    self.__dead = dead


class Blast(pygame.sprite.Sprite):
  ''' instantiates a blast pygame sprite object with a position, size, image, damage, colour, speed, and direction of the blast that updates to collide with players, create special blasts, and spawn portals on walls '''

  def __init__(self, x, y, x_speed, direction, screen_width, colour, screen,
               damage, playerwidth, special_blast, portal_spawning,
               starting_health):
    ''' instantiates a blast pygame sprite object with a position, size, image, damage, colour, speed, and direction of the blast '''

    # adding blasts will not work without the below statement, or unless explicitly specifying Player().__init__() subclass method instead of Blast.__init__()
    super().__init__()

    # initialize and set volumes of orange and blue blast sound effects
    orange_blast_sound = pygame.mixer.Sound("sounds/o_blast.mp3")
    blue_blast_sound = pygame.mixer.Sound("sounds/b_blast.mp3")
    orange_blast_sound.set_volume(0.1)
    blue_blast_sound.set_volume(0.1)

    # initialize and set the volume of the sound effect upon hitting a player
    self.__hit_sound = pygame.mixer.Sound("sounds/blast_hit.mp3")
    self.__hit_sound.set_volume(0.1)

    # if the player is orange
    if colour == 'o':

      # play the orange player's firing sound
      orange_blast_sound.play()

      # if the player is facing left
      if direction == "left":

        # set the image of the blast to the left-facing orange blast
        self.image = pygame.image.load("images/o_leftblast.png")

      # if the player is not facing left (right)
      else:

        # set the image of the blast to the right-facing orange blast
        self.image = pygame.image.load("images/o_rightblast.png")

    # if the player is not orange (blue)
    else:

      # play the blue player's firing sound
      blue_blast_sound.play()

      # if the player is facing left
      if direction == "left":

        # set the image of the blast to the left-facing blue blast
        self.image = pygame.image.load("images/b_leftblast.png")

      # if the player is not facing left (right)
      else:

        # set the image of the blast to the right-facing blue blast
        self.image = pygame.image.load("images/b_rightblast.png")

    # create and store a rect attribute as the size of the blast's image
    self.rect = self.image.get_rect()

    # set the initial position of the blast
    self.rect.x = x + playerwidth / 2
    self.rect.y = y

    # set the speed of the blast
    self.__x_speed = x_speed

    # set the direction of the blast to the direction the player is facing
    self.__direction = direction

    # store the integer vlue of the screen's pixel width
    self.__screen_width = screen_width

    # store the integer value of the blast's colour
    self.__colour = colour

    # store the integer value of the blast's damage
    self.__damage = damage

    # store a boolean value representing whether the blast is a special blast; faster speed, higher damage, and spawns a portal whenever it collides with a wall
    self.__special_blast = special_blast

    self.__starting_health = starting_health

    # store a boolean value of whether the blast is able to spawn a portal
    self.__portal_spawning = portal_spawning

  def update(self, player_list, screen, all_sprites, screen_width,
             score_board):
    ''' takes player_list, screen, all_sprites, and screen_width as parameters - checks for collisions with walls and other players, and despawns/spawns a portal or damage the player respectively '''

    # if the blast is travelling to the left
    if self.__direction == "left":

      # subtract the value of the blast's x_speed attribute, as moving left would mean moving towards x = 0 on the screen
      self.rect.x -= self.__x_speed

    # if the blast is travelling to the right
    else:

      # add the value of the blast's x_speed attribute, as moving right would mean moving away from x = 0 on the screen
      self.rect.x += self.__x_speed

    # if the blast object reaches the edge of the screen
    if self.rect.x < 0 or self.rect.x > self.__screen_width:

      # if the blast is a portal-spawning blast and portal_spawning was enabled by the user
      if self.__special_blast and self.__portal_spawning:

        # instantiate an object named new_portal with necessary arguments such as direction, colour and the player's current position
        new_portal = sprites.Portal(self.rect.x, self.rect.y, self.__colour,
                                    self.__direction, 93, 200, screen_width,
                                    self.__starting_health)

        # add the new_portal object to the list of all_sprites
        all_sprites.add(new_portal)

      # kill the blast object
      self.kill()

    # for the player objects in the player_list parameter
    for player in player_list:
      # if the blast's collision box is within range to hit the player's collision box both vertically and horizontally
      if (self.rect.y >= player.get_pos()[1]
          and self.rect.y <= player.get_pos()[1] + player.get_size()[1]) and (
            self.rect.x < player.get_pos()[0] + player.get_size()[0]
            and self.rect.x > player.get_pos()[0]):
        # if the blast was not fired by the player of the same colour (no friendly-fire)
        if self.__colour != player.get_colour():

          # subtract 1 from the player's health attribute
          player.set_health(player.get_health() - self.__damage)

          # kill the blast object
          self.kill()

          # play the blast hit sound
          self.__hit_sound.play()

          # add 1 score for the player who successfully hit the enemy player
          score_board.add_score(self.__colour, screen)
