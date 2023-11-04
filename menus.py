'''
Writers: Kenrick Zhang, Dickson Zhao
Date: 21/01/2023
Description: A Pygame which features an Orange and Blue player who battle each other with magic blasts and portals.
'''

# import required packages, libraries and modules
import pygame
import map_presets


def check_button(button_x, button_y, button_width, button_height, mouse):
  ''' takes an x and y coordinate, button size, and mouse position as input - returns a boolean value representing whether the coordinates of the mouse are located within the button '''

  # if the mouse coordinates are within the given button coordinates
  if (button_x <= mouse[0] <= button_x + button_width) and (
      button_y <= mouse[1] <= button_y + button_height):

    # return True to the caller
    return True


class TextField(pygame.sprite.Sprite):
  ''' instantiates a pygame sprite with a position, name and starting value, and a boolean clicked attribute that signifies if it currently selected by the user '''

  def __init__(self, name, starting_value, x, y):
    ''' takes name, starting_value, and position as parameters - initializes said parameter values into their respective attributes, as well as a clicked attribute for storing the selected state of the TextField object'''

    # the TextField object should be unclicked by default
    self.__clicked = False

    # initialize name, starting value and position
    self.__name = name
    self.__value = starting_value
    self.__x = x
    self.__y = y

  # get and set methods below for their respective attributes
  def get_clicked(self):
    return self.__clicked

  def get_value(self):
    return self.__value

  def get_pos(self):
    return self.__x, self.__y

  def get_name(self):
    return self.__name

  def set_clicked(self, clicked):
    self.__clicked = clicked

  def set_value(self, value):
    self.__value = value


class ToggleSwitch(pygame.sprite.Sprite):
  ''' instantiates a pygame sprite with a position, image, name, starting value, and second position, which the image can also be blitted to if a certain criteria is met '''

  def __init__(self, name, starting_value, x, y, x2, y2, image_path):
    ''' takes name, starting_value, and position as parameters - initializes said parameter values into their respective attributes, as well as a clicked attribute for storing the selected state of the TextField object'''

    # initialize name, starting value and positions
    self.__name = name
    self.__value = starting_value
    self.__x = x
    self.__y = y
    self.__x2 = x2
    self.__y2 = y2

    # load the image defined in the image_path parameter
    self.__image = pygame.image.load(image_path)

  # get and set methods below for their respective attributes
  def get_value(self):
    return self.__value

  def get_pos(self):
    return self.__x, self.__y

  def get_second_pos(self):
    return self.__x2, self.__y2

  def get_image(self):
    return self.__image

  def get_name(self):
    return self.__name

  def set_value(self, value):
    self.__value = value


def settings_menu(screen, text_fields, toggle_switches, map_toggles,
                  player_settings, environment_settings):
  ''' takes screen, the lists of setting menu buttons, options, and player and environment settings as parameters - displays a settings menu that allows users to dictate how they want to game to function such as running speed, damage, health, and infinite jumping '''

  # load settings menu background
  settings_image = pygame.image.load("images/settings_image.jpg")

  # load lit "ready to go" orange and blue player logo
  player_merge = pygame.image.load("images/player_merge.png")

  # load the selected field type image for the text input boxes
  selected_field277x72 = pygame.image.load("images/selected_field277x72.png")

  # load the boolean setting images
  switch_on = pygame.image.load("images/switch_on.png")
  switch_off = pygame.image.load("images/switch_off.png")

  # load the map selection lit image
  selected_field64x64 = pygame.image.load("images/selected_field64x64.png")

  # initialize default player settings
  default_player_settings = ["20", "10", "1", "5", True, False]

  # assign a boolean settings_menu running a True value
  settings_menu = True

  # defining a font style and size
  small_font = pygame.font.Font("hippo.ttf", 35)

  # initialize clock as a pygame clock object
  clock = pygame.time.Clock()

  # while the boolean settings_menu sentinel remains True
  while settings_menu:

    # uses the get_pos() function to store the (x, y) coordinates of the mouse into mouse
    mouse = pygame.mouse.get_pos()

    # blit the screen object with the settings background menu image
    screen.blit(settings_image, (0, 0))

    # for every input event (mouse/key presses) in the array returned using the pygame.event.get() function
    for event in pygame.event.get():

      # if the user quit
      if event.type == pygame.QUIT:

        # close pygame
        pygame.quit()

      # if the mouse is left, right, or middle clicked/scrolled
      if event.type == pygame.MOUSEBUTTONDOWN:

        # for all of the field objects in the list text_fields
        for field in text_fields:

          # set each field object's clicked attribute to false
          field.set_clicked(False)

        # check if mouse's position is located within the "ready to go" button
        if check_button(378, 381, 240, 220, mouse):

          # set the boolean settings_menu sentinel to False to close the main game loop, taking the player back to the main menu
          settings_menu = False

          # for all of the field objects in the list text_fields
          for field in text_fields:

            # checks if the names of player settings match the names of the field, and sets those player settings to the respective field's value attribute
            if field.get_name() == "starting_health":
              player_settings[0] = str(field.get_value())
            elif field.get_name() == "running_speed":
              player_settings[1] = str(field.get_value())
            elif field.get_name() == "blast_damage":
              player_settings[2] = str(field.get_value())
            elif field.get_name() == "gravity":
              player_settings[3] = str(field.get_value())

          # for all of the switch objects in the list toggle_switches
          for switch in toggle_switches:

            # checks if the names of player settings match the names of the switch, and sets those player settings to the respective switch's value attribute
            if switch.get_name() == "portal_spawning":
              player_settings[4] = switch.get_value()
            elif switch.get_name() == "invincibility":
              if switch.get_value():
                player_settings[2] = "0"
            elif switch.get_name() == "gravity":
              if not switch.get_value():
                player_settings[3] = "1"
            elif switch.get_name() == "infinite_jumping":
              player_settings[5] = switch.get_value()

          # for all of the map objects in the list map_toggles
          for map in map_toggles:

            # if the map's value isn't 0 or empty
            if map.get_value():

              # call the map_preset module's load_map() function wih the name of the selected map and store the returned result into the enhvironment_settings list
              environment_settings = map_presets.load_map(map.get_name())

          # validate and return the player_settings and environment_settings lists to the caller (try-excepts for empty strings, the lone if for handling divisions by 0 for the healthbar)
          try:
            valid_int = int(player_settings[0])
          except:
            player_settings[0] = default_player_settings[0]

          if player_settings[0] == "0":
            player_settings[0] = default_player_settings[0]

          try:
            valid_int = int(player_settings[1])
          except:
            player_settings[1] = default_player_settings[1]

          if int(player_settings[1]) > 100:
            player_settings[1] = default_player_settings[1]

          try:
            valid_int = int(player_settings[2])
          except:
            player_settings[2] = default_player_settings[2]

          try:
            valid_int = int(player_settings[3])
          except:
            player_settings[3] = default_player_settings[3]

          if player_settings[3] == "0":
            player_settings[3] = default_player_settings[3]

          return (player_settings, environment_settings)

        # a long if chain that checks if the mouse is located on a text field, and selects the text field for key input when clicked
        elif check_button(84, 169, 277, 72, mouse):
          for fields in text_fields:
            if fields.get_name() == "starting_health":
              fields.set_clicked(True)

        elif check_button(84, 289, 277, 72, mouse):
          for fields in text_fields:
            if fields.get_name() == "running_speed":
              fields.set_clicked(True)

        elif check_button(84, 409, 277, 72, mouse):
          for fields in text_fields:
            if fields.get_name() == "blast_damage":
              fields.set_clicked(True)

        elif check_button(84, 529, 277, 72, mouse):
          for fields in text_fields:
            if fields.get_name() == "gravity":
              fields.set_clicked(True)

        # a long if chain that checks if the mouse is located on a toggle switch, and flips the value of the toggle switch when clicked
        elif check_button(634, 169, 277, 72, mouse):
          for switch in toggle_switches:
            if switch.get_name() == "portal_spawning":
              switch.set_value(not switch.get_value())

        elif check_button(634, 289, 277, 72, mouse):
          for switch in toggle_switches:
            if switch.get_name() == "invincibility":
              switch.set_value(not switch.get_value())

        elif check_button(634, 409, 277, 72, mouse):
          for switch in toggle_switches:
            if switch.get_name() == "gravity":
              switch.set_value(not switch.get_value())

        elif check_button(634, 529, 277, 72, mouse):
          for switch in toggle_switches:
            if switch.get_name() == "infinite_jumping":
              switch.set_value(not switch.get_value())

        # a long if chain that checks if the mouse is located on a map toggle, and selects only that specific map when clicked
        elif check_button(378, 169, 72, 72, mouse):
          for map in map_toggles:
            if map.get_name() == "lab":
              map.set_value(True)
              continue
            map.set_value(False)

        elif check_button(462, 169, 72, 72, mouse):
          for map in map_toggles:
            if map.get_name() == "cave":
              map.set_value(True)
              continue
            map.set_value(False)

        elif check_button(546, 169, 72, 72, mouse):
          for map in map_toggles:
            if map.get_name() == "cosmic":
              map.set_value(True)
              continue
            map.set_value(False)

        elif check_button(378, 253, 72, 72, mouse):
          for map in map_toggles:
            if map.get_name() == "desert":
              map.set_value(True)
              continue
            map.set_value(False)

        elif check_button(462, 253, 72, 72, mouse):
          for map in map_toggles:
            if map.get_name() == "ocean":
              map.set_value(True)
              continue
            map.set_value(False)

        elif check_button(546, 253, 72, 72, mouse):
          for map in map_toggles:
            if map.get_name() == "sky":
              map.set_value(True)
              continue
            map.set_value(False)

      # if a key input is received
      elif event.type == pygame.KEYDOWN:

        # a long if chain that stores the value of whatever key is pressed into the currently selected text field

        if event.key == pygame.K_0:
          for fields in text_fields:
            if fields.get_clicked():
              fields.set_value(fields.get_value() + "0")

        elif event.key == pygame.K_1:
          for fields in text_fields:
            if fields.get_clicked():
              fields.set_value(fields.get_value() + "1")

        elif event.key == pygame.K_2:
          for fields in text_fields:
            if fields.get_clicked():
              fields.set_value(fields.get_value() + "2")

        elif event.key == pygame.K_3:
          for fields in text_fields:
            if fields.get_clicked():
              fields.set_value(fields.get_value() + "3")

        elif event.key == pygame.K_4:
          for fields in text_fields:
            if fields.get_clicked():
              fields.set_value(fields.get_value() + "4")

        elif event.key == pygame.K_5:
          for fields in text_fields:
            if fields.get_clicked():
              fields.set_value(fields.get_value() + "5")

        elif event.key == pygame.K_6:
          for fields in text_fields:
            if fields.get_clicked():
              fields.set_value(fields.get_value() + "6")

        elif event.key == pygame.K_7:
          for fields in text_fields:
            if fields.get_clicked():
              fields.set_value(fields.get_value() + "7")

        elif event.key == pygame.K_8:
          for fields in text_fields:
            if fields.get_clicked():
              fields.set_value(fields.get_value() + "8")

        elif event.key == pygame.K_9:
          for fields in text_fields:
            if fields.get_clicked():
              fields.set_value(fields.get_value() + "9")

        # if a backspace or delete input is received
        elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:

          # for the fields in the list of text_fields
          for fields in text_fields:

            # if the current fields in selected and the field is not empty
            if fields.get_clicked() and len(fields.get_value()) > 0:

              # assign the fields the value of the fields minus the last character
              fields.set_value(fields.get_value()[:-1])

    # if the mouse's position is located within the "ready to go" button
    if check_button(378, 381, 240, 220, mouse):

      # blit the player_merge image ontop of the "ready to go" button
      screen.blit(player_merge, (410, 410))

    # for the fields in the list of text_fields
    for field in text_fields:

      # if the current field object is clicked
      if field.get_clicked():

        # blit the selected field image ontop of the background in the same position
        screen.blit(selected_field277x72,
                    (field.get_pos()[0], field.get_pos()[1]))

    # for the switches in the list of toggle_switches
    for switch in toggle_switches:

      # if the current switch object's value is True
      if switch.get_value():

        # blit the on_switch image to the right position of the switch
        screen.blit(switch_on,
                    (switch.get_second_pos()[0], switch.get_second_pos()[1]))

      # if the current switch object's value is False
      else:

        # blit the off_switch image to the left position of the switch
        screen.blit(switch_off, (switch.get_pos()[0], switch.get_pos()[1]))

    # for the map toggles in the list map_toggles
    for map in map_toggles:

      # if the map is selected
      if map.get_value():

        # blit the selected field image over the position of the map toggle
        screen.blit(selected_field64x64, (map.get_pos()[0], map.get_pos()[1]))

      # blit the mini image of the map
      screen.blit(map.get_image(),
                  (map.get_second_pos()[0], map.get_second_pos()[1]))

    # for the field objects in list text_fields
    for field in text_fields:

      # assign text a text label of the field's name and on a filled white small_font label
      text = small_font.render(str(field.get_value()), True, (255, 255, 255))

      # blit the screen with the text at the location of the field
      screen.blit(text, (field.get_pos()[0], field.get_pos()[1]))

    # flips the necessary portion of the display
    pygame.display.flip()

    # updates the frames of the game
    pygame.display.update()

    # sets the tickrate of the settings menu to 20 ticks, or refreshes, per second
    clock.tick(20)


def help_menu(screen):
  ''' no parameters - displays a help menu for the user to reference controls and learn the basics of the game '''

  # load help menu background
  help_image = pygame.image.load("images/help_image.jpg")

  # load lit "ready to go" orange and blue player logo
  player_merge = pygame.image.load("images/player_merge.png")

  # assign a boolean settings_menu running a True value
  help_menu = True

  # initialize clock as a pygame clock object
  clock = pygame.time.Clock()

  # while the boolean help_menu sentinel remains True
  while help_menu:

    # uses the get_pos() function to store the (x, y) coordinates of the mouse into mouse
    mouse = pygame.mouse.get_pos()

    # blit the screen object with the settings background menu image
    screen.blit(help_image, (0, 0))

    # for every input event (mouse/key presses) in the array returned using the pygame.event.get() function
    for event in pygame.event.get():

      # if the user quit
      if event.type == pygame.QUIT:

        # close pygame
        pygame.quit()

      # if the mouse is left, right, or middle clicked/scrolled
      if event.type == pygame.MOUSEBUTTONDOWN:

        # check if mouse's position is located within the "ready to go" button
        if check_button(378, 381, 240, 220, mouse):

          # set the boolean settings_menu sentinel to False to close the main game loop, taking the player back to the main menu
          help_menu = False

    # if the mouse's position is located within the "ready to go" button
    if check_button(378, 381, 240, 220, mouse):

      # blit the player_merge image ontop of the "ready to go" button
      screen.blit(player_merge, (410, 410))

    # flips the necessary portion of the display
    pygame.display.flip()

    # updates the frames of the game
    pygame.display.update()

    # sets the tickrate of the help menu to 20 ticks, or refreshes, per second
    clock.tick(20)
