'''
Writers: Kenrick Zhang, Dickson Zhao
Date: 21/01/2023
Description: A Pygame which features an Orange and Blue player who battle each other with magic blasts and portals.
'''

# import required packages, libraries and modules
import pygame
import map_presets
import game_functions
import menus


def main():
  ''' no parameters - mainline logic for the game, initializes pygame/mixer and sets resolution, initializes the main menu assets, creates a screen, and creates then stores player and environment settings '''

  # initialize pygame and pygame mixer
  pygame.init()
  pygame.mixer.init()

  # initialize the screen width and height separately for later clarity
  screen_width = 1000
  screen_height = 700

  # sets the resolution of a pygame display named screen to screen_width and screen_height
  screen = pygame.display.set_mode((screen_width, screen_height))

  # sets the caption of the game window to the game title
  pygame.display.set_caption("Portals: Orange and Blue")

  # load main menu text image assets
  text_play = pygame.image.load("images/text_play.png")
  text_settings = pygame.image.load("images/text_settings.png")
  text_quit = pygame.image.load("images/text_quit.png")
  text_help = pygame.image.load("images/text_help.png")

  # load main menu image and music assets
  menu_image = pygame.image.load("images/menu_image.jpg").convert()
  menu_music = pygame.mixer.Sound("sounds/menu_background_music.mp3")
  menu_music.set_volume(0.1)

  # load 100x40 main menu lit and unlit button type images
  unlit100x40 = pygame.image.load("images/unlit100x40.png")
  lit100x40 = pygame.image.load("images/lit100x40.png")

  # load 150x40 main menu lit and unlit button type images
  unlit150x40 = pygame.image.load("images/unlit150x40.png")
  lit150x40 = pygame.image.load("images/lit150x40.png")

  # initialize a list text_fields with the names, values and positions of four TextField objects
  text_fields = [
    menus.TextField("starting_health", "20", 84, 169),
    menus.TextField("running_speed", "10", 84, 289),
    menus.TextField("blast_damage", "1", 84, 409),
    menus.TextField("gravity", "5", 84, 529)
  ]

  # initialize a list toggle_switches with the names, values, image, and first and second positions of four ToggleSwitch objects
  toggle_switches = [
    menus.ToggleSwitch("portal_spawning", True, 639, 174, 785, 174,
                       "images/pixel.png"),
    menus.ToggleSwitch("invincibility", False, 639, 294, 785, 294,
                       "images/pixel.png"),
    menus.ToggleSwitch("gravity", True, 639, 414, 785, 414,
                       "images/pixel.png"),
    menus.ToggleSwitch("infinite_jumping", False, 639, 534, 785, 535,
                       "images/pixel.png")
  ]

  # initialize a list map_toggles with the names, values, image, and first and second positions of four ToggleSwitch objects
  map_toggles = [
    menus.ToggleSwitch("lab", True, 378, 169, 382, 173,
                       "environment/lab_image_mini.png"),
    menus.ToggleSwitch("cave", False, 462, 169, 466, 173,
                       "environment/cave_image_mini.png"),
    menus.ToggleSwitch("cosmic", False, 546, 169, 550, 173,
                       "environment/cosmic_image_mini.png"),
    menus.ToggleSwitch("desert", False, 378, 253, 382, 257,
                       "environment/desert_image_mini.png"),
    menus.ToggleSwitch("ocean", False, 462, 253, 466, 257,
                       "environment/ocean_image_mini.png"),
    menus.ToggleSwitch("sky", False, 546, 253, 550, 257,
                       "environment/sky_image_mini.png")
  ]

  # play the menu music indefinitely
  menu_music.play(-1)

  # assign the default player_settings
  player_settings = ["20", "10", "1", "5", True, False]

  # assign the default environment_settings as those of the lab map
  environment_settings = map_presets.load_map("lab")

  # below details the parameters of player and environment settings
  # player_settings = [starting_health, running_speed, blast_damage, gravity, portal_spawning, infinite_jumping]
  # environment_settings = [background_music, background_image, platform1_image, platform2_image, platform3_image, platform4_image]

  # initialize clock as a pygame clock object
  clock = pygame.time.Clock()

  # assign a boolean sentinel running a True value
  running = True

  # while the boolean running sentinel remains True
  while running:

    # uses the get_pos() function to store the (x, y) coordinates of the mouse into mouse
    mouse = pygame.mouse.get_pos()

    # blit the screen object with the background menu image
    screen.blit(menu_image, (0, 0))

    # for every input event (mouse/key presses) in the array returned using the pygame.event.get() function
    for event in pygame.event.get():

      # if the user quit
      if event.type == pygame.QUIT:

        # close pygame
        pygame.quit()

      # if the mouse is left, right, or middle clicked/scrolled
      if event.type == pygame.MOUSEBUTTONDOWN:

        # check if mouse's position is located within the play button
        if menus.check_button(350, 350, 100, 40, mouse):

          # stop the main menu music (technically stops all sounds, but should be the only sound playing at this point)
          pygame.mixer.stop()

          # call the game_functions module's main_game() function, with arguments environment_settings and player_settings, both determining game properties
          game_functions.main_game(environment_settings, player_settings)

          # after the main_game() function is finished executing, restart the main menu music (player should always go to the main menu before actually quitting)
          menu_music.play(-1)

        # check if mouse's position is located within the settings button
        elif menus.check_button(425, 400, 150, 40, mouse):

          # call the menu module's settings_menu() function, with arguments environment_settings, player_settings and other settings menu objects, both determining game properties, and store the two lists returned back into player_settings and environment_settings
          player_settings, environment_settings = menus.settings_menu(
            screen, text_fields, toggle_switches, map_toggles, player_settings,
            environment_settings)

        # check if mouse's position is located within the quit button
        elif menus.check_button(550, 350, 100, 40, mouse):

          # close pygame
          pygame.quit()

        # check if mouse's position is located within the help button
        elif menus.check_button(450, 450, 100, 40, mouse):

          # call the menu module's help_menu() function, displaying a new screen with everything the player should know about the game
          menus.help_menu(screen)

    # blit the screen with the unlit version of the play button
    screen.blit(unlit100x40, (350, 350))

    # blit the screen with the lit version of the settings button
    screen.blit(unlit150x40, (425, 400))

    # blit the screen with the unlit version of the quit button
    screen.blit(unlit100x40, (550, 350))

    # blit the screen with the unlit version of the help button
    screen.blit(unlit100x40, (450, 450))

    # if the mouse is hovered over the play button
    if menus.check_button(350, 350, 100, 40, mouse):

      # blit the screen with the lit version of the play button
      screen.blit(lit100x40, (350, 350))

    # if the mouse is hovered over the settings button
    elif menus.check_button(425, 400, 150, 40, mouse):

      # blit the screen with the lit version of the settings button
      screen.blit(lit150x40, (425, 400))

    # if the mouse is hovered over the quit button
    elif menus.check_button(550, 350, 100, 40, mouse):

      # blit the screen with the lit version of the quit button
      screen.blit(lit100x40, (550, 350))

    # if the mouse is hovered over the help button
    elif menus.check_button(450, 450, 100, 40, mouse):

      # blit the screen with the lit version of the help button
      screen.blit(lit100x40, (450, 450))

    # blit the screen with the play button's text
    screen.blit(text_play, (325, 350))

    # blit the screen with the settings button's text
    screen.blit(text_settings, (425, 400))

    # blit the screen with the quit button's text
    screen.blit(text_quit, (525, 350))

    # blit the screen with the help button's text
    screen.blit(text_help, (425, 450))

    # flips the necessary portion of the display
    pygame.display.flip()

    # updates the frames of the game
    pygame.display.update()

    # sets the tickrate of the main menu to 20 ticks, or refreshes, per second
    clock.tick(20)


# calls main()
main()
