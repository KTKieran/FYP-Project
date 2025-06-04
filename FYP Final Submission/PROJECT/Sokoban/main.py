import pygame
import sys
import time
from settings import *
from Levels import levels
from AIsolver import *

# ----------Create game class, this deals with the whole Sokoban game and its particular interactions----------
class SokobanGame:

    # -----------Initializing constructor for the game setup----------
    
    def __init__(self):
        """
        Initializes the Sokoban game by setting up the Pygame environment, loading the game assets,
        and preparing the initial game state.

        This method sets up the Pygame window and clock, initializes game control flags, 
        and prepares the level that the player will start with.
        It also finds the initial position of the player on the grid, initializes the AI solver,
        and loads the initial level setup including the positions of boxes and targets.
        """        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.current_level_key = 'Level 1'
        self.initial_boxes = None
        self.levels = levels
        self.player_x, self.player_y = self.find_player_start_position()
        self.mouse = pygame.mouse.get_pos()
        self.solve = AI(self)
        self.load_level()

    # ---------- Draw methods that inlcude display elements to the user and the level interactions ----------

    def draw_level(self):
        """
        Generates the current level's layout on the game screen.

        Iterates through the grid representation of the level, drawing each tile
        based on its type. The elements of walls, boxes, and targets are represented 
        by different colours. This method fills the entire screen first to reset the drawing 
        surface beforedrawing the level elements, ensuring a fresh render of the level state.
        """
        self.screen.fill(WHITE)  # Clear screen with white background
        for y, row in enumerate(self.level):
            for x, tile in enumerate(row):
                grid = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == 1:  # Wall
                    pygame.draw.rect(self.screen, BLACK, grid)
                elif tile == 2:  # Box
                    pygame.draw.rect(self.screen, BROWN, grid)
                elif tile == 3:  # Target
                    pygame.draw.rect(self.screen, SILVER, grid)

    def draw_player(self):
        """
        Draws the player on the game screen at their current position.
        This method uses Pygame to draw a rectangle representing the player with 
        different features like the colour and its position on the grid.
        """
        pygame.draw.rect(self.screen, BLUE, (self.player_x * TILE_SIZE, self.player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    def find_player_start_position(self):
        """
        Identifies and returns the initial position of the player in the current level.

        Scans the grid representation of the current level for the player's start tile,
        designated by a specific tile value. Returns the coordinates of this tile as the
        player's starting position.

        Returns:
            tuple: The (x, y) coordinates of the player's starting position. Returns a default
            position if the player's start tile is not found within the level data.
        """
        for y, row in enumerate(self.levels[self.current_level_key]):
            for x, tile in enumerate(row):
                if tile == 4:  # Player start tile
                    return x, y
        return 1, 1  # Default position if not found


    def printed_level(self):
        """
        A print feature that updates whenever an action on the level is taken place.
        """        
        for row in self.level:
            print(row)
        print("------")

    def load_level(self):
        """
        Loads the current level based on `current_level_key`, sets up the level grid, 
        and initializes the game state for the level.
    
        This method performs several key operations to set up the level:
        - Copies the created level layout from the `levels` dictionary to `self.level`, 
        ensuring a fresh start for each level load.
        - Finds and sets the initial player position on the grid.
        - A flag is used to indicate whether it is safe for the user to solve the current level whilst not modified. 

        This method is intended to be called whenever a new level is started or the current 
        level needs to be reset.
        """        
        self.level = [row[:] for row in self.levels[self.current_level_key]]
        self.player_x, self.player_y = self.find_player_start_position()
        self.level_change = False # Flag to indicate if the level had changed
        self.printed_level()
    
    def switch_level(self):
        """
        Switches to the next level or ends the game if all levels have been completed.

        This method determines the current level's index within the list of level keys and checks
        if there is an upcoming level to switch to. If there is another level, the game updates
        the current level key to that level and loads it with a print. If the current level is the last
        one in the list, it shows prints indicating that all levels have been completed and the
        game comes to an end.

        """        
        # Determine the current level index
        keys = list(self.levels.keys())
        current_level_index = keys.index(self.current_level_key)
        keys_length = len(keys)
        print(f"Current Level Key: {self.current_level_key}")

        # Check if there's a next level
        if current_level_index < keys_length - 1:
            print(f"{self.current_level_key} Complete!")
            # Switch to the next level
            self.current_level_key = keys[current_level_index + 1]
            print(f"{self.current_level_key} Start!")
            self.load_level()
        else:
            # If there's no next level, end the game or perform any other actions
            print("All levels completed. Game over.")
            self.is_running = False

    def draw_reset_button(self):
        """
        Draws the reset button on the screen.

        This method creates a button labeled 'Reset' on the screen. When the mouse pointer is over the button,
        the button's appearance changes to indicate that it can be clicked. If the button is clicked, the game level
        is reset to its initial state by calling the `reset_level` method.

        The button's appearance, including its position, size, and colour, is defined within the method. The method
        also checks for mouse interaction to detect clicks on the button.
        """
        # Display the aesthetics of the button 
        button_rect = pygame.Rect(150, HEIGHT - 80, 100, 50)
        font = pygame.font.Font(None, 36)
        button_text = font.render(reset, True, BLACK)

        # Mouse handles the button
        if button_rect.collidepoint(self.mouse):
            pygame.draw.rect(self.screen, LIGHTER_SHADE, button_rect) # Overlay when interacted
            if pygame.mouse.get_pressed()[0]:  
                self.reset_level()
        else:
            pygame.draw.rect(self.screen, DARKER_SHADE, button_rect) # Overlay when not interacted with

        # Position of the button
        self.screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))
    
    def reset_level(self):
        """
        Resets the current game level to its initial state.

        The method does this by calling `load_level`, which reads the initial level data from the `levels` dictionary
        and sets up the level accordingly. It also prints a message indicating that the level has been
        reset in the log. There is a pygame feature that delays loops and controlling the speed constant loading.
        """
        print("Level reset")
        self.load_level()
        pygame.time.wait(100) # Add a small delay to prevent multiple triggers

    
    def draw_key(self):
        """
        Draws a key on the screen that illustrates what each colour represents in the game for user clarity.

        The key is positioned towards the right-hand side of the game window. It includes visual representations
        for walls, the player, boxes, and targets, each with a corresponding colour using the pygame font 
        and draw features .Next to each box, a text label describes what the box represents. The method 
        calculates the size of the key area based on the number of elements and draws a border around 
        the key for clarity.

        Attributes:
            x_start (int): The x-coordinate of the start position for the key on the screen.
            y_start (int): The y-coordinate of the start position for the key on the screen.
            key_elements (list of tuples): A list where each tuple contains a string label and a Pygame colour
                                            representing an element in the game.
            key_width (int): The width of the key area, determined by the longest text label.
            key_height (int): The height of the key area, calculated based on the number of elements.
            font (pygame.font.Font): The font used for rendering text labels next to the key symbols.
        """        
        x_start = WIDTH - 150
        y_start = 50
        
        # Define key elements and their colours
        key_elements = [
            ("Wall", BLACK),
            ("Player", BLUE),
            ("Box", BROWN),
            ("Target", SILVER),
        ]
        
        # Key visibilty
        font = pygame.font.Font(None, 24)  # Adjust size as needed
        key_width = 150  
        key_height = len(key_elements) * 30 + 10 

        # Border for the key
        border_rect = pygame.Rect(x_start - 5, y_start - 5, key_width, key_height)  # Border thickness
        pygame.draw.rect(self.screen, BLACK, border_rect, 2)  # Border colour

        for i, (element, colour) in enumerate(key_elements):
            # Draw the box representing the element
            box_rect = pygame.Rect(x_start, y_start + i * 30, 20, 20)  # Box sized : 20x20
            pygame.draw.rect(self.screen, colour, box_rect)

            # Render the text next to the box
            key_text = font.render(element, True, BLACK) 
            self.screen.blit(key_text, (x_start + 25, y_start + i * 30))
    
    def update(self):
        """
        Updates the game screen with the current game state.

        This method redraws the game screen by each frame. It clears the screen,
        then draws the current level, the player, and the UI elements such as the solve button,
        reset button, and the key. After all drawing operations are complete, it updates
        the display to reflect the changes using a pygame display feature. This method ensures that 
        the game visuals accurately represent the current state of the game, including any movements 
        or actions taken by the player since the previous frame.
        """
        # Clear the screen
        self.screen.fill(WHITE)
        # Draw the level and the player
        self.draw_level()
        self.draw_player()
        # Draw UI elements
        self.draw_solve_button()
        self.draw_reset_button()
        self.draw_key()
        # Update the display
        pygame.display.flip()
    
    # ---------- In game interaction methods for the game and the events that take place ----------

    def events(self):
        """
        A method that determines the observe software and peripheral events in Sokoban.

        The game is able to go into different states that is controlled by the user. 
        It can close when the user decides to stop running the programming, it can perform keyboard
        events and, it can perform mouse events

        """        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keyboard_events(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_events()
    
    def handle_keyboard_events(self, event):
        """
        Handles the keyboard events, specifically the player movements controlled by the user.

        This method updates the player's position based on arrow key inputs.
        It checks for the validity of the new position within the created game grid boundaries
        and calls `player_actions` to move the player and handle any interactions
        at the new position (e.g, pushing boxes).
        
        Args:
            event (pygame.event.Event): The event object representing a keyboard event. 
            This contains information about the specific key pressed.
        """    
         # Initialize new_x and new_y
        new_x, new_y = self.player_x, self.player_y

        # Update new_x and new_y based on the pressed key
        if event.key == pygame.K_UP:
            new_y = self.player_y - 1
        elif event.key == pygame.K_DOWN:
            new_y = self.player_y + 1
        elif event.key == pygame.K_RIGHT:
            new_x = self.player_x + 1
        elif event.key == pygame.K_LEFT:
            new_x = self.player_x - 1

        # Check if the new position is within the screen bounds
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            self.player_actions(new_x, new_y)
     
    def handle_mouse_events(self):
        """
        Used specifically for on click mouse events and indicate when the user performs a mouse action.
        """        
        # Reveals the position of the mouse
        self.mouse = pygame.mouse.get_pos()
    
    def player_actions(self, new_x, new_y):
        """
        Executes the actions that take place when moving the player to a new position on the grid.
    
        This method determines the type of tile at the requested new position and performs
        actions based on the tile type. If the tile is empty or contains a box, it attempts
        to move the player to that position. If the tile contains a box, it also tries to push
        the box to the next position in the same direction by calling the push_box method. 
        If the movement or push is successful, it updates the game state accordingly on the print statements. 
        This method flags the level as changed upon any successful action that alters the level's state.

        Args:
            new_x (int): The x-coordinate of the new position the player is attempting to move to.
            new_y (int): The y-coordinate of the new position the player is attempting to move to.

        """        
        self.level_change = True
        print(f"Current Position: ({self.player_x}, {self.player_y})")
        print(f"Requested Position: ({new_x}, {new_y})")
        print(f"Tile at New Position: {self.level[new_y][new_x]}")

        # If the new position is either empty or has a box, move the player
        if self.level[new_y][new_x] == 0 or self.level[new_y][new_x] == 2 or self.level[new_y][new_x] == 4:
            # If the new position has a box, try to push the box
            if self.level[new_y][new_x] == 2:
                self.level[self.player_y][self.player_x] = 0
                print("Trying to push the box.")
                self.push_box(new_x, new_y)
            # If the new position is empty, move the player
            elif self.level[new_y][new_x] == 0 or self.level[new_y][new_x] == 4:
                print("Moving player.")
                self.level[self.player_y][self.player_x] = 0
                self.player_x, self.player_y = new_x, new_y
                self.level[new_y][new_x] = 4
        else:
            print("Cannot move to the new position.")
        
        if self.level[new_y][new_x] != 3:
            print("Updated Position: ({}, {})".format(self.player_x, self.player_y))
            print("Updated Level:")
            self.printed_level()

    def push_box(self, new_x, new_y):
        """
        This method attempts to push a box from the player's current position to a new position.
        
        This method is called when the player attempts to move into a space occupied by a box.
        It calculates the new position for the box based on the player's movement direction and
        checks if the box can be moved to that position within thearea. A box can be pushed 
        onto an empty space or a target. The method updates the game state to reflect the box's 
        new position if the push is successful. It also checks for level completion 
        when a box is placed on a target. This also flags when the level is modified by the user

        Args:
            new_x (int): The x-coordinate of the position where the player is attempting to push the box.
            new_y (int): The y-coordinate of the position where the player is attempting to push the box.
        
        """        
        self.level_change = True
        # Calculate the new position of the box
        box_x, box_y = new_x, new_y
        new_box_x, new_box_y = box_x + (box_x - self.player_x), box_y + (box_y - self.player_y)
        print(f"Box Position: ({box_x}, {box_y})")
        print(f"New Box Position: ({new_box_x}, {new_box_y})")

        # Check if the new position for the box is within the screen bounds and is empty
        if (0 <= new_box_x < GRID_WIDTH and 0 <= new_box_y < GRID_HEIGHT and (self.level[new_box_y][new_box_x] == 0 or self.level[new_box_y][new_box_x] == 3)):
            if self.level[new_box_y][new_box_x] == 0:
                print("Moving player and pushing the box.")
                # Move the player and the box
                self.player_x, self.player_y = new_x, new_y
                self.level[box_y][box_x] = 0
                self.level[new_box_y][new_box_x] = 2
                self.level[new_y][new_x] = 4
            # Check for box placement and level completion
            elif self.level[new_box_y][new_box_x] == 3:
                self.player_x, self.player_y = new_x, new_y
                self.level[box_y][box_x] = 0
                self.level[new_box_y][new_box_x] = 2
                print("Box placed")
                self.placed_boxes_checker()
        else:
            print("Box cannot be pushed.")
    
    def placed_boxes_checker(self):
        """
        Checks if all boxes have been placed on their respective targets within the current level.

        This method iterates through the level's grid to count the number of target tiles remaining.
        If no targets are left (indicating that all boxes have been placed on targets), it proceeds
        to switch to the next level. Otherwise, it prints the number of targets that are still
        awaiting a box.

        """        
        target_count = sum(row.count(3) for row in self.level) # Counts number of targets

        if target_count == 0:
            print("All boxes placed on targets.")
            self.switch_level() # When there is no more unoccupied targets, it switches the level
        else:
            print(f"{target_count} target(s) remaining.") # Shows remaining targets still available
    
    # ----------AI element, involving the solve button and the animation of the solution----------

    def is_move_valid(self, player_x, player_y, new_box_x=None, new_box_y=None):
        """
        Determines if a move or box push is valid within the game grid.

        This method checks if the player's move is into an occupied space or if, when pushing a box,
        the box's new position is valid. It ensures that neither player or the box moves into walls, out of bounds,
        or onto another box.

        Args:
            player_x (int): The x-coordinate of the player's new position.
            player_y (int): The y-coordinate of the player's new position.
            new_box_x (int, optional): The x-coordinate of the box's new position if a box is being pushed.
            new_box_y (int, optional): The y-coordinate of the box's new position if a box is being pushed.

        Returns:
            bool: True if the move is valid, False if not.
        """
        # Check if player is moving into a wall or into the target
        if self.level[player_y][player_x] == 1 or self.level[player_y][player_x] == 3:
            return False

        # If checking a box push, ensure the new box position is valid
        if new_box_x is not None and new_box_y is not None:
            # Check if the new box position is out of bounds or into a wall or another box
            if not (0 <= new_box_x < GRID_WIDTH and 0 <= new_box_y < GRID_HEIGHT):
                return False
            if self.level[new_box_y][new_box_x] == 1 or self.level[new_box_y][new_box_x] == 2:  # Wall or another box
                return False

        return True

    def draw_solve_button(self):
        """
        Draws the 'Solve' button and handles its interaction.

        When clicked, if the level has been altered, it prompts the user to reset the level.
        Otherwise, it attempts to solve the level automatically using the AI solver. If a solution
        is found, it animates the solution on the screen. The button appearance changes when hovered
        to indicate it's interactive. There is also a delay for loop control, preventing uneccessary
        triggers in the log. 
        """
        # Draws the aesthetics of the button
        button_rect = pygame.Rect(30, HEIGHT - 80, 100, 50)
        font = pygame.font.Font(None, 36)
        button_text = font.render(solve, True, BLACK)
        
        # Handles mouse events
        if button_rect.collidepoint(self.mouse):
            pygame.draw.rect(self.screen, LIGHTER_SHADE, button_rect)
            if pygame.mouse.get_pressed()[0]: 
                if self.level_change: # Flag if theres been change to the level
                    print("USER! Please reset the level first before solving automatically solving the level!")
                else:
                    # Call AI method
                    solution_path = self.solve.solve_level()
                    if solution_path is not None:
                        print("Solution found:", solution_path)
                        self.animate_solution(solution_path)
                    else:
                        print("No solution found.")
                pygame.time.wait(100)  # Add a small delay to prevent multiple triggers
        else:
            pygame.draw.rect(self.screen, DARKER_SHADE, button_rect)

        # Button position
        self.screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))
    
    def simulate_move(self, x, y):
        """
        Simulates a move of the player by a given offset.

        This method calculates the new position of the player based on the provided x and y offsets
        and then attempts the move. It is typically used to simulate the player's movements to complement
        the AI solution path.

        Args:
            x (int): The x offset from the player's current position.
            y (int): The y offset from the player's current position.
        """

        # Calculate the new player position
        new_player_x = self.player_x + x
        new_player_y = self.player_y + y

        # player_actions method correctly moves the player and possibly pushes boxes
        self.player_actions(new_player_x, new_player_y)

    def animate_solution(self, solution_path):
        """
        Animates the solution on the game screen step by step.
            
        For each step in the solution path, this method simulates the player's move and updates the
        game screen to show its new state. It pauses briefly between each step to make the animation
        visible to the user.

        Args:
            solution_path (list of tuples): A sequence of (x, y) moves representing the solution.
        """
        for x, y in solution_path:
            # simulate_move method to apply each move from the solution
            self.simulate_move(x, y)

            # Redraw the game state to show the move
            self.update_solve_screen()
            pygame.display.flip()

            # Pause briefly between moves to animate
            time.sleep(1)    

        # Handling the quit event to keep the window responsive during the animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
    def update_solve_screen(self):
        """
        Redraws the game screen to demonstrate the current state during solution animation.

        This method clears the screen, redraws the level and the player in their current states,
        and then updates the display. It is specifically used during the animation of the AI's
        solution to ensure the screen is refreshed correctly after each move in the solution.
        """
        self.screen.fill(WHITE)
        self.draw_level()
        self.draw_player()
        pygame.display.flip()

    # ----------Method to run loop of the game events and elements----------
    def run(self):
        while self.is_running:
            self.clock.tick(FPS)
            self.events()
            self.update()
        
        # Quit Pygame
        pygame.quit()
        sys.exit()

# ----------Main game loop-----------
if __name__ == "__main__":
    print("I have been launched!")
    game = SokobanGame()
    game.run()
