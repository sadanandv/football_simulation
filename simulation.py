# /simulation.py

import numpy as np
import datetime
from environment.field import FootballField
from environment.physics_engine import PhysicsEngine
from environment.rules import GameRules
from environment.ball import Ball
from agents.team_agent import TeamAgent
from environment.player import Player
import os

class FootballSimulation:
    def __init__(self, half_duration=45):
        self.log_file = f"data/logs/game_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        self.field = FootballField()
        self.physics_engine = PhysicsEngine()
        self.rules = GameRules(self.field, self.log_file)
        self.ball = Ball()
        self.half_duration = half_duration  # Duration of each half in minutes
        self.current_half = 1
        self.rewards = {'team_a': {}, 'team_b': {}}
        
        self.team_a_players = [
            Player(player_id=i, position=[10 * i % 105, 34], skill=np.random.uniform(0.6, 0.9), team='team_a')
            for i in range(11)
        ]
        self.team_b_players = [
            Player(player_id=i, position=[105 - 10 * i % 105, 34], skill=np.random.uniform(0.6, 0.9), team='team_b')
            for i in range(11, 22)
        ]

        # Create Team Agents
        self.team_a_agent = TeamAgent(self.team_a_players, self.field, self.rules, self.log_file)
        self.team_b_agent = TeamAgent(self.team_b_players, self.field, self.rules, self.log_file)

        # Assign agents to players
        for player in self.team_a_players + self.team_b_players:
            player.agent = self.team_a_agent if player.team == 'team_a' else self.team_b_agent

        self.assign_roles()
        self.update_team_chemistry()
        self.initialize_rewards()

    def log_event(self, message):
        with open(self.log_file, 'a') as f:
            f.write("[SIMULATION]" + message + '\n')
        print(message)  # Keep printing to the console for visibility as well

    def assign_roles(self):
        """Assign roles to players to implement team-specific strategies."""
        roles = ['goalkeeper', 'defender', 'midfielder', 'attacker']
        for i, player in enumerate(self.team_a_players):
            player.role = roles[min(i // 3, len(roles) - 1)]
        for i, player in enumerate(self.team_b_players):
            player.role = roles[min(i // 3, len(roles) - 1)]

    def update_team_chemistry(self):
        """Update chemistry values for all players based on teammates."""
        for player in self.team_a_players:
            player.update_chemistry(self.team_a_players)
        for player in self.team_b_players:
            player.update_chemistry(self.team_b_players)

    def initialize_rewards(self):
        """Initialize rewards dictionary for tracking player rewards."""
        for player in self.team_a_players:
            self.rewards['team_a'][player.player_id] = 0
        for player in self.team_b_players:
            self.rewards['team_b'][player.player_id] = 0

    def update_reward(self, team, player_id, reward):
        """Update reward for a given player."""
        self.rewards[team][player_id] += reward
    
    def rest_all_players(self):
        """Rest all players during half-time."""
        for player in self.team_a_players + self.team_b_players:
            player.stamina = min(player.stamina + 30, 100)  # Add 30 stamina points, cap at 100
            self.log_event(f"Player {player.player_id} rests during half-time. Stamina is now {player.stamina}")

    def run_simulation(self):
        dt = 60.00  # time step in seconds
        half_time_steps = int((self.half_duration * 60) / dt)
        self.log_event(f"Before Game:\t Team A:{self.rules.score['team_a']} - Team B:{self.rules.score['team_b']}")

        for half in range(1, 3):  # Loop for two halves
            self.log_event(f"Starting Half {half}")
            for step in range(half_time_steps):
                # Simulate actions for each player in Team A and Team B
                for player in self.team_a_players + self.team_b_players:
                    if player.stamina > 0:
                        player.make_decision(dt)

                        # Randomly decide to pass or shoot
                        if np.random.rand() < 0.1:  # Random chance to pass
                            target_player = np.random.choice(self.team_a_players if player.team == 'team_a' else self.team_b_players)
                            player.pass_ball(self.ball, target_player.position, force=10)
                            player.stamina = self.physics_engine.update_stamina(player.stamina, dt, effort_level=0.5, action_type="stand", attr=player.physical_attributes['stamina'])
                            # Reward for successful pass
                            self.update_reward(player.team, player.player_id, 10)

                        if np.random.rand() < 0.05:  # Random chance to shoot
                            goal_position = np.array([105, 34]) if player.team == 'team_a' else np.array([0, 34])
                            player.shoot(self.ball, goal_position, force=20)
                            # Reward for shooting on target
                            self.update_reward(player.team, player.player_id, 30)

                    # Update ball position
                    self.ball.update_position(dt)

                    # Check game rules such as out-of-bounds, goals, etc.
                    if self.rules.check_out_of_bounds(self.ball.get_position()):
                        self.rules.handle_throw_in(self.ball.get_position(), player.team)

                    if self.field.is_in_goal_area(self.ball.get_position()):
                        scoring_team = player.team
                        self.rules.award_goal(scoring_team)

                        # Reward for scoring a goal
                        self.update_reward(scoring_team, player.player_id, 100)

                        # Instead of breaking, reset the ball position and continue playing
                        self.ball.position = np.array([52.5, 34.0])  # Reset to center
                        self.ball.velocity = np.array([0.0, 0.0])
                        self.log_event(f"Goal by {scoring_team}! Game resumes after reset.")
                
                # Log the current state every step (optional for debugging)
                self.log_event(f"Half {half}, Step {step}: Ball position: {self.ball.get_position()}")
                for player in self.team_a_players + self.team_b_players:
                    self.log_event(f"Half {half}, Step {step}: Player {player.player_id} Position: {player.position}, Stamina: {player.stamina}")
                
            # Half-time reset
            if half == 1:
                self.log_event("Half-time break. Players rest.")
                self.rest_all_players()

        # Final score and full-time announcement
        final_score = self.rules.score
        self.log_event("Full Time!")
        if final_score['team_a'] > final_score['team_b']:
            self.log_event("Team A Wins!")
            for player in self.team_a_players:
                self.update_reward('team_a', player.player_id, 50)
        elif final_score['team_b'] > final_score['team_a']:
            self.log_event("Team B Wins!")
            for player in self.team_b_players:
                self.update_reward('team_b', player.player_id, 50)
        else:
            self.log_event("Match Drawn!")
            for player in self.team_a_players + self.team_b_players:
                self.update_reward(player.team, player.player_id, 10)

        # Print final rewards
        self.log_event("Final Rewards:")
        self.log_event(f"Team A: {self.rewards['team_a']}")
        self.log_event(f"Team B: {self.rewards['team_b']}")
        self.log_event(f"Final Scores:\t Team A:{final_score['team_a']} - Team B:{final_score['team_b']}")


if __name__ == "__main__":
    sim = FootballSimulation(half_duration=45)
    sim.run_simulation()
