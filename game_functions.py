'''
Writers: Kenrick Zhang, Dickson Zhao
Date: 21/01/2023
Description: A Pygame which features an Orange and Blue player who battle each other with magic blasts and portals.
'''

# import required packages, libraries and modules
import pygame
import anim_frames
import player_sprites
import sprites


def game_over_screen(loser, screen):
  ''' takes string loser and pygame surface object screen as parameters - blits an image message to the screen specifying the winner of the round '''

  # initialize orange and blue wins as their respective pygame images
  orange_wins = pygame.image.load("images/o_wins.png")
  blue_wins = pygame.image.load("images/b_wins.png")

  # if orange lost
  if loser == 'o':

    # blit the blue_wins message to the screen
    screen.blit(blue_wins, (238, 192))

  # if blue lost
  else:

    # blit the orange_wins message to the screen
    screen.blit(orange_wins, (175, 192))


def main_game(environment_settings, player_settings):
  ''' takes list environment_settings and list player_settings as parameters - runs through a main game loop with the specified settings effecting the gameplay '''

  # below details the parameters of player and environment settings
  # player_settings = [starting_health, running_speed, blast_damage, gravity, portal_spawning, infinite_jumping]
  # environment_settings = [background_music, background_image, platform1_image, platform2_image, platform3_image, platform4_image]

  # initialize the screen width and height separately for later clarity
  screen_width = 1000
  screen_height = 700

  # unpack and assign player_settings into game-specific variables
  starting_health = int(player_settings[0])
  running_speed = int(player_settings[1])
  blast_damage = int(player_settings[2])
  gravity = int(player_settings[3]) / 10
  portal_spawning = player_settings[4]
  infinite_jumping = player_settings[5]

  # unpack and assign environment_settings into game-specific variables
  background_music = environment_settings[0]
  background_music.set_volume(0.1)
  background_image = environment_settings[1]
  platform1_image = environment_settings[2]
  platform2_image = environment_settings[3]

  # sets the resolution of a pygame display named screen to screen_width and screen_height
  screen = pygame.display.set_mode((screen_width, screen_height))

  # load the initial frames of the orange and blue players into their respective objects
  o_player = pygame.image.load("player_anims/o_right2gun.png")
  b_player = pygame.image.load("player_anims/b_left2gun.png")

  # load a single invisible pixel for invisible sprites (roof and floor)
  invisible_pixel = pygame.image.load("images/pixel.png")

  # load and set the volume of the winning fanfare
  winning_sound = pygame.mixer.Sound("sounds/winning_sound.mp3")
  winning_sound.set_volume(0.2)

  # load the health bar overlay displayed at the top of the screen
  health_overlay = pygame.image.load("images/health_overlay.png")

  # instantitate empty all_sprites and explosions sprite groups to group projectile and explosion sprites for collision checks
  all_sprites = pygame.sprite.Group()
  explosions = pygame.sprite.Group()

  # calls anim_frames module's get_frames() function to get and store orange's and blue's left and right facing frames into their respective lists
  o_left_anims, o_right_anims = anim_frames.get_frames("o")
  b_left_anims, b_right_anims = anim_frames.get_frames("b")

  # instantiate an orange and blue player objects with some fixed and some variable values of player_settings
  o_player = player_sprites.Player(0, 0, 120, 120, "o", screen_width,
                                   screen_height, 15, o_left_anims,
                                   o_right_anims, "right", starting_health,
                                   running_speed)
  b_player = player_sprites.Player(screen_width - 120, 0, 120, 120, "b",
                                   screen_width, screen_height, 15,
                                   b_left_anims, b_right_anims, "left",
                                   starting_health, running_speed)

  # create a list player_list with two elements, the players
  player_list = [o_player, b_player]

  # create a list platforms with collisions for players
  platforms = [
    # invisible roof and floor, respectively
    sprites.Platform(0, screen_height, screen_width, 50, invisible_pixel,
                     True),
    sprites.Platform(0, -50, screen_width, 50, invisible_pixel, True),

    # left and right starting platforms respectively
    sprites.Platform(0, screen_height - 200, platform1_image.get_width(),
                     platform1_image.get_height(), platform1_image, False),
    sprites.Platform(screen_width - 200, screen_height - 200,
                     platform1_image.get_width(), platform1_image.get_height(),
                     platform1_image, False),
    sprites.Platform(screen_width / 2 - platform2_image.get_width() / 2, 300,
                     platform2_image.get_width(), platform2_image.get_height(),
                     platform2_image, False)
  ]

  # initialize clock as a pygame clock object
  clock = pygame.time.Clock()

  # assign a boolean sentinel running a True value
  running = True

  # play the menu music indefinitely
  background_music.play(-1)

  # create a ScoreKeeper object
  score_board = sprites.ScoreKeeper(456, 60, 504, 60)

  # while the boolean running sentinel remains True
  while running:

    # for every input event (mouse/key presses) in the array returned using the pygame.event.get() function
    for event in pygame.event.get():

      # if the user quit
      if event.type == pygame.QUIT:

        # set the boolean running sentinel to False to close the main game loop
        running = False

        # stop all audio
        pygame.mixer.stop()

      # if the user presses a key
      elif event.type == pygame.KEYDOWN:

        # perform various actions dependent on the respective movement controls of each player object
        if event.key == pygame.K_UP and not o_player.get_dead():
          o_player.jump(infinite_jumping)

        elif event.key == pygame.K_LEFT:
          o_player.set_direction("left")
          o_player.set_last_direction("left")

        elif event.key == pygame.K_RIGHT:
          o_player.set_direction("right")
          o_player.set_last_direction("right")

        elif event.key == pygame.K_w and not b_player.get_dead():
          b_player.jump(infinite_jumping)

        elif event.key == pygame.K_a:
          b_player.set_direction("left")
          b_player.set_last_direction("left")

        elif event.key == pygame.K_d:
          b_player.set_direction("right")
          b_player.set_last_direction("right")

        # if a right control input is received and the orange player is not dead
        elif event.key == pygame.K_RCTRL and not o_player.get_dead():

          # if the orange player has fired 9 or more blasts
          if o_player.get_blast_count() >= 9:

            # create a special orange blast with variable and non-variable attributes like damage specified and standard/state-dependent variables such as player direction and player width, but with the ability to spawn portals upon hitting a wall
            orange_blast = player_sprites.Blast(o_player.get_pos()[0],
                                                o_player.get_pos()[1], 30,
                                                o_player.get_last_direction(),
                                                screen_width, 'o', screen,
                                                blast_damage * 3,
                                                o_player.get_size()[0], True,
                                                portal_spawning,
                                                starting_health)

            # reset the orange player's blast count to 0
            o_player.set_blast_count(0)

          # if the orange player has fired 8 or less blasts
          else:

            # create a regular orange blast with variable and non-variable attributes like damage specified and standard/state-dependent variables such as player direction and player width
            orange_blast = player_sprites.Blast(o_player.get_pos()[0],
                                                o_player.get_pos()[1], 15,
                                                o_player.get_last_direction(),
                                                screen_width, 'o', screen,
                                                blast_damage,
                                                o_player.get_size()[0], False,
                                                portal_spawning,
                                                starting_health)

            # increment the orange player's blast count by 1
            o_player.set_blast_count(o_player.get_blast_count() + 1)

          # add the new orange blast to the list all_sprites
          all_sprites.add(orange_blast)

        # if a g input is received and the blue player is not dead
        elif event.key == pygame.K_g and not b_player.get_dead():

          # if the blue player has fired 9 or more blasts
          if b_player.get_blast_count() >= 9:

            # create a special blue blast with variable and non-variable attributes like damage specified and standard/state-dependent variables such as player direction and player width, but with the ability to spawn portals upon hitting a wall
            blue_blast = player_sprites.Blast(b_player.get_pos()[0],
                                              b_player.get_pos()[1], 30,
                                              b_player.get_last_direction(),
                                              screen_width, 'b', screen,
                                              blast_damage * 3,
                                              b_player.get_size()[0], True,
                                              portal_spawning, starting_health)

            # reset the blue player's blast count to 0
            b_player.set_blast_count(0)

          # if the orange player has fired 8 or less blasts
          else:

            # create a regular blue blast with variable and non-variable attributes like damage specified and standard/state-dependent variables such as player direction and player width
            blue_blast = player_sprites.Blast(b_player.get_pos()[0],
                                              b_player.get_pos()[1], 15,
                                              b_player.get_last_direction(),
                                              screen_width, 'b', screen,
                                              blast_damage,
                                              b_player.get_size()[0], False,
                                              portal_spawning, starting_health)

            # increment the blue player's blast count by 1
            b_player.set_blast_count(b_player.get_blast_count() + 1)

          # add the new blue blast to the list all_sprites
          all_sprites.add(blue_blast)

        # if a p input is received
        elif event.key == pygame.K_p:

          # set the boolean running sentinel to False to close the main game loop
          running = False

          # stop all audio
          pygame.mixer.stop()

          # continue the main game loop so that it stops immediately without needing to break
          continue

      # if an up arrow or w input is received
      elif event.type == pygame.KEYUP:

        # if a left or right arrow input is received
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

          # set the orange player's direction to none
          o_player.set_direction("")

        # if an a key or d key input is received
        if event.key == pygame.K_a or event.key == pygame.K_d:

          # set the blue player's direction to none
          b_player.set_direction("")

    # if the orange player is currently running left
    if o_player.get_direction() == "left":

      # subtract runspeed from the orange player's current x position, moving them to the left
      o_player.set_x(o_player.get_pos()[0] - o_player.get_runspeed())

    # if the orange player is currently running right
    elif o_player.get_direction() == "right":

      # add runspeed to the orange player's current x position, moving them to the right
      o_player.set_x(o_player.get_pos()[0] + o_player.get_runspeed())

    # if the blue player is currently running left
    if b_player.get_direction() == "left":

      # subtract runspeed from the blue player's current x position, moving them to the left
      b_player.set_x(b_player.get_pos()[0] - b_player.get_runspeed())

    # if the blue player is currently running right
    elif b_player.get_direction() == "right":

      # add runspeed to the blue player's current x position, moving them to the right
      b_player.set_x(b_player.get_pos()[0] + b_player.get_runspeed())

    # update the player, platforms and explosions with some necessary arguments such as current gravity and sprite lists for collisions
    o_player.update(platforms, gravity)
    b_player.update(platforms, gravity)
    explosions.update(player_list, screen, all_sprites, screen_width)

    # draw the background image first
    screen.blit(background_image, (0, 0))

    # draw the players at their position attributes
    screen.blit(o_player.get_image(),
                (o_player.get_pos()[0], o_player.get_pos()[1]))
    screen.blit(b_player.get_image(),
                (b_player.get_pos()[0], b_player.get_pos()[1]))

    # for the platform objects in the list platforms
    for platform in platforms:

      # draw the platforms at its position attributes
      screen.blit(platform.get_image(),
                  (platform.get_pos()[0], platform.get_pos()[1]))

    # for the explosion objects in the list explosions
    for explosion in explosions:

      # draw the explosion at its position attributes
      screen.blit(explosion.get_image(),
                  (explosion.get_pos()[0], explosion.get_pos()[1]))

    # for the player objects in the list player_list
    for player in player_list:

      # if the player's health is 0 or less and the player isn't dead yet
      if player.get_health() < 1 and not player.get_dead():

        # create an explosion object at the position they died in
        explosions.add(
          sprites.Explosion(player.get_pos()[0],
                            player.get_pos()[1], screen))

        # set the player's dead attribute to True
        player.set_dead(True)

        # delete the dead player object
        del (player)

        # stop all audio
        pygame.mixer.stop()

        # play the winning fanfare once
        winning_sound.play()

        # for the remaining alive player in the list player_list
        for player in player_list:

          # if the player is not dead
          if not player.get_dead():

            # set the alive player's health by a multiple of the starting health that it becomes practically impossible for the winning player to die
            player.set_health(starting_health * 100)

    # for the player objects in the list player_list
    for player in player_list:

      # update the score board object to render the current scores for both players
      score_board.update(player.get_colour(), screen)

      # if the player is dead
      if player.get_dead():

        # call the game_over_screen() function with the dead player's colour as the loser argument and the screen to blit the winning message to
        game_over_screen(player.get_colour(), screen)

    # draw the collision boxes on top of the player and platforms (do not include this in final game)
    '''
    for player in player_list:
      pygame.draw.rect(screen, (255, 0, 0), player.get_collision_box().get_rect(), 1)
    for platform in platforms:
      pygame.draw.rect(screen, (255, 0, 0), platform.get_collision_box().get_rect(), 1)
    '''

    # call the update methods of sprites in the all_sprites sprite group to update positions and check for collisions
    all_sprites.update(player_list, screen, all_sprites, screen_width,
                       score_board)

    # draw all sprites in the all_sprites sprite group to the screen
    all_sprites.draw(screen)

    # blit the health bar overlay to the screen
    screen.blit(health_overlay, (168, 0))

    # for each player in the list player_list
    for player in player_list:

      # draw the player's respective health bar
      sprites.draw_health(screen, player.get_colour(), player.get_health(),
                          starting_health)

    # flips the necessary portion of the display
    pygame.display.flip()

    # updates the frames of the game
    pygame.display.update()

    # sets the tickrate of the active screen to 60 ticks, or refreshes, per second
    clock.tick(60)
