import heapq
from Levels import levels

class AI:
    def __init__(self, game_instance):
        self.game_instance = game_instance

    def find_boxes(self):
        """
        Searches and returns a list of positions for all boxes within the game level.

        Scans the entire level grid and identifies the positions of all 'box' tiles,
        represented by the tile value 2. This function returns the positions of all boxes.

        Returns:
            list of tuples: A list where each tuple represents the position (x, y) of a box on the game level grid.
        """
        return [(x, y) for y, row in enumerate(self.game_instance.level) for x, tile in enumerate(row) if tile == 2]

    
    def box_heuristic(self, boxes):
        """
        Calculates the heuristic cost for a given state based on the sum of the minimum distances
        from each box to its nearest calculated target.

        This function estimates the cost to reach the goal state from the current state 
        by considering the total distance that all boxes need to cover to reach the
        closest target.

        Args:
            boxes (list of tuples): The current positions of all boxes in the level, where each
                                    box's position is represented as a tuple (x, y).

        Returns:
            int: The total heuristic cost for the given state, calculated as the sum of the
                minimum Manhattan distances from each box to its nearest target.
        """       
        total_distance = 0
        targets = [(x, y) for y, row in enumerate(self.game_instance.level) for x, tile in enumerate(row) if tile == 3]
        for box in boxes: # Iterates all shown box in the level
            min_distance = min(abs(box[0] - target[0]) + abs(box[1] - target[1]) for target in targets) # Calculates minimum distances to box
            total_distance += min_distance
        return total_distance

    def goal_state(self, boxes):
        """
        Checks if the current state meets the goal state, where all boxes are placed on targets.

        The goal state is reached when the set of box positions exactly matches the set of target
        positions within the current level.

        Args:
            boxes (list of tuples): The current positions of all boxes in the level, where each
                                    box's position is represented as a tuple (x, y).

        Returns:
            bool: True if all boxes are on targets, False otherwise.
        """
        targets = [(x, y) for y, row in enumerate(self.game_instance.level) for x, tile in enumerate(row) if tile == 3]
        return set(boxes) == set(targets)

    def generate_successors(self, state):
        """
        Generates all possible successor states from the current state.

        For each possible move direction, this method checks if moving the player or pushing a box
        in that direction is valid. It generates a new state for each valid move, capturing the
        player's new position and any changes in box positions.

        Args:
            state (tuple): The current state, represented as a tuple containing the player's
                        position (x, y) and the positions of all boxes.

        Returns:
            list of tuples: A list of successor states, where each state is represented as a tuple
                            containing the new player position, updated box positions, and the move
                            direction that led to this state.
        """
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        direction_names = {(0, -1): "Up", (0, 1): "Down", (-1, 0): "Left", (1, 0): "Right"}
        successors = []
        player_x, player_y, boxes = state
        for y, x in directions:
            new_player_x, new_player_y = player_x + x, player_y + y
            direction = direction_names[(x, y)]
            move_is_valid = self.game_instance.is_move_valid(new_player_x, new_player_y, None, None)  # For player moves without pushing a box
            new_boxes = list(boxes)
            if (new_player_x, new_player_y) in boxes:
                box_index = boxes.index((new_player_x, new_player_y))
                new_box_x, new_box_y = new_player_x + x, new_player_y + y
                move_is_valid = self.game_instance.is_move_valid(new_player_x, new_player_y, new_box_x, new_box_y)  # For moves involving pushing a box
                if move_is_valid:
                    new_boxes[box_index] = (new_box_x, new_box_y)
                    successors.append(((new_player_x, new_player_y, tuple(new_boxes)), (x, y)))
            elif move_is_valid:
                successors.append(((new_player_x, new_player_y, tuple(boxes)), (x, y)))
            
            if move_is_valid == True:
                print(f"Trying move: Player({player_x}, {player_y}) to ({new_player_x}, {new_player_y}), Move valid: {move_is_valid}")

        print(f"Generated {len(successors)} successors from state: {state}")
        print(f"Trying direction: {direction}, From: ({player_x}, {player_y}) to ({new_player_x}, {new_player_y})")
        return successors

    def solve_level(self):
        """
        Tries to find a solution to the current level using the A* search algorithm.

        This method iterates through possible game states using a priority queue, where the
        priority is determined by a heuristic cost function. It explores different states 
        until it finds a solution that meets the goal condition or exhausts all possibilities.
        It logs the initial player position, the final solution path, and the player's
        position after each move in the solution, if a solution path is found.

        Returns:
            list of tuples or None: A sequence of (x, y) moves representing the solution if one
                                    is found, otherwise None.
        """
        direction_names = {(0, -1): "Up", (0, 1): "Down", (-1, 0): "Left", (1, 0): "Right"}
        start_state = (self.game_instance.player_x, self.game_instance.player_y, tuple(self.find_boxes()))
        frontier = []
        heapq.heappush(frontier, (0, start_state, []))  # Cost, state, path
        explored = set()
        
        while frontier:
            cost, current_state, path = heapq.heappop(frontier)
            if current_state in explored:
                continue
            explored.add(current_state)
            _, _, boxes = current_state
            
            if self.goal_state(boxes):
                # Log the final solution path and calculate player positions
                current_player_x, current_player_y = start_state[:2]  # Get initial player position
                print(f"Initial Player Position: ({current_player_x}, {current_player_y})")
                for x, y in path:
                    move_direction = direction_names[(x, y)]
                    current_player_x += x
                    current_player_y += y
                    print(f"After moving {move_direction}, Player Position: ({current_player_x}, {current_player_y})")
                return path
                
            for successor, (x, y) in self.generate_successors(current_state):
                if successor not in explored:
                    new_cost = cost + 1  # Assuming each move costs 1
                    new_path = path + [(x, y)]
                    heapq.heappush(frontier, (new_cost + self.box_heuristic(successor[2]), successor, new_path))
                    
        return None