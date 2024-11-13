# agents/team_agent.py

import numpy as np
from utils.chemistry_utils import calculate_chemistry
from environment.ball import Ball
from environment.physics_engine import PhysicsEngine
from environment.rules import GameRules

class TeamAgent:
    def __init__(self, players,field,rules):
        self.players = players
        self.field = field
        self.rules = rules
        self.player_id_to_index = {player.player_id: idx for idx, player in enumerate(players)}
        self.chemistry_matrix = self.initialize_chemistry_matrix()

    def initialize_chemistry_matrix(self):
        """Initialize the chemistry matrix based on each player's chemistry with others."""
        num_players = len(self.players)
        chemistry_matrix = np.zeros((num_players, num_players))
        for i in range(num_players):
            for j in range(num_players):
                if i != j:
                    chemistry_matrix[i][j] = calculate_chemistry(self.players[i], self.players[j])
        return chemistry_matrix

    def get_chemistry_influence(self, player_id, teammate_id):
        """Get chemistry influence between two players."""
        if player_id not in self.player_id_to_index or teammate_id not in self.player_id_to_index:
            raise ValueError(f"Player ID {player_id} or {teammate_id} is not found in the team.")
        
        player_idx = self.player_id_to_index[player_id]
        teammate_idx = self.player_id_to_index[teammate_id]
        return self.chemistry_matrix[player_idx][teammate_idx]

    def decide_action(self, player, dt):
        """
        Decide what action the player should take based on their role, stamina, and game state.
        """
        if player.stamina < 10:
            self.rest(player)
            return

        role = player.role
        action_probability = np.random.rand()
        
        # Rest if stamina is too low
        if player.stamina < 10:
            self.rest(player)
            return

        if player.role == 'goalkeeper':
            self.goalkeeper_action(player, action_probability, dt)
        elif player.role == 'defender':
            if action_probability < 0.4:
                self.move_to_position(player, 'defender', dt)
            elif action_probability < 0.8:
                self.attempt_pass(player, dt)
            else:
                self.attempt_tackle(player, dt)
        elif player.role == 'midfielder':
            if action_probability < 0.3:
                self.move_to_position(player, 'midfielder', dt)
            elif action_probability < 0.6:
                self.attempt_pass(player, dt)
            else:
                self.dribble(player, dt)
        elif player.role == 'attacker':
            if action_probability < 0.2:
                self.dribble(player, dt)
            elif action_probability < 0.5:
                self.attempt_pass(player, dt)
            elif action_probability < 0.8:
                self.attempt_shot(player, dt)
            else:
                self.move_to_position(player, 'attacker', dt)

    def rest(self, player):
        # Attackers should rest only if absolutely necessary
        if player.role == 'attacker' and player.stamina > 30:
            return
        player.stamina += 5
        player.stamina = min(player.stamina, 100)
        #print(f"Player {player.player_id} is resting to regain stamina. Current stamina: {player.stamina}")

    def goalkeeper_action(self, player, action_probability, dt):
        """Define specific actions for the goalkeeper."""
        if action_probability < 0.7:
            # Goalkeeper stays near goal
            target_position = np.array([5, player.position[1]])
            player.move_to_position(target_position, PhysicsEngine(), dt)
        else:
            # Attempt to pass to a defender
            self.attempt_pass(player, dt)

    def move_to_position(self, player, role, dt):
        """Move player to a target position based on role."""
        if role == 'defender':
            # Move towards the defensive area
            target_position = np.array([np.random.uniform(0, 40), np.random.uniform(0, 68)])
        elif role == 'midfielder':
            # Move towards the midfield area
            target_position = np.array([np.random.uniform(40, 70), np.random.uniform(0, 68)])
        else:
            # Default to midfield
            target_position = np.array([52.5, 34.0])

        player.move_to_position(target_position, PhysicsEngine(), dt)
        #print(f"Player {player.player_id} moved to position {player.position} as per their role.")

    def attempt_pass(self, player, dt):
        """Attempt to pass the ball to a teammate."""
        teammates = [p for p in self.players if p.player_id != player.player_id and p.team == player.team]
        if not teammates:
            return
        
        target_player = max(teammates, key=lambda p: (
            self.get_chemistry_influence(player.player_id, p.player_id) * 0.6 + 
            (1 / (np.linalg.norm(player.position - p.position) + 1e-5)) * 0.4
        ))        
        # Assume pass requires ball possession
        if player.stamina > 5:
            player.pass_ball(Ball(), target_player.position, force=10)
            player.stamina -= 5
            #print(f"Player {player.player_id} passed the ball to Player {target_player.player_id} at position {target_player.position}")

    def attempt_tackle(self, player, dt):
        """Attempt to tackle an opponent if they are within range."""
        opponents = [p for p in self.players if p.team != player.team and np.linalg.norm(player.position - p.position) < 5]
        if not opponents:
            return

        target_opponent = opponents[0]  # Tackle the nearest opponent
        if player.tackle(target_opponent):
            print(f"Player {player.player_id} successfully tackled Player {target_opponent.player_id}")
        else:
            print(f"Player {player.player_id} failed to tackle Player {target_opponent.player_id}")

    def dribble(self, player, dt):
        """Player dribbles towards a more advanced position."""
        if player.stamina > 10:
            acceleration = np.array([0.1, 0.05])
            player.dribble(acceleration, PhysicsEngine(), dt)
            #print(f"Player {player.player_id} is dribbling. Current position: {player.position}")
            player.stamina -= 10

    def attempt_shot(self, player, dt):
        """Player attempts to shoot at the goal."""
        if player.stamina > 15:
            # Determine goal position based on the player's team
            goal_position = np.array([105, 34]) if player.team == 'team_a' else np.array([0, 34])

            # Calculate distance to the goal and determine shot success probability
            distance_to_goal = np.linalg.norm(player.position - goal_position)
            shot_success_prob = player.skill * 0.5 + (100 / distance_to_goal) * 0.2

            # Determine if shot is successful
            if np.random.rand() < shot_success_prob:
                # Player successfully scores a goal
                print(f"Player {player.player_id} scores a goal for {player.team}!")

                # Update the game score using the game rules reference
                self.rules.award_goal(player.team)

            else:
                # Shot missed or saved by the goalkeeper
                player.shoot(Ball(), goal_position, force=20)

            # Reduce player's stamina after attempting a shot
            player.stamina -= 15

