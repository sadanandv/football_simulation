# environment/simulation.py

import numpy as np
from .field import FootballField
from .physics_engine import PhysicsEngine
from .rules import GameRules
from .ball import Ball
from .player import Player

class FootballSimulation:
    def __init__(self, half_duration=45):
        self.field = FootballField()
        self.physics_engine = PhysicsEngine()
        self.rules = GameRules(self.field)
        self.ball = Ball()
        self.half_duration = half_duration  # Duration of each half in minutes
        self.current_half = 1
        self.total_goals = {'team_a': 0, 'team_b': 0}

        self.team_a_players = [Player(player_id=i, position=[10 * i % 105, 34], skill=np.random.uniform(0.6, 0.9)) for i in range(11)]
        self.team_b_players = [Player(player_id=i, position=[105 - 10 * i % 105, 34], skill=np.random.uniform(0.6, 0.9)) for i in range(11, 22)]

        self.assign_roles()

    def assign_roles(self):
        """Assign roles to players to implement team-specific strategies"""
        roles = ['goalkeeper', 'defender', 'midfielder', 'attacker']
        for i, player in enumerate(self.team_a_players):
            player.role = roles[min(i // 3, len(roles) - 1)]
        for i, player in enumerate(self.team_b_players):
            player.role = roles[min(i // 3, len(roles) - 1)]

    def run_simulation(self):
        dt = 2.00  # time step in seconds
        half_time_steps = int((self.half_duration * 60) / dt)

        for half in range(1, 3):  # Loop for two halves
            print(f"Starting Half {half}")
            for step in range(half_time_steps):
                # Simulate actions for each player in Team A
                for player in self.team_a_players:
                    if player.stamina > 0:
                        # Move player towards a target based on role
                        if player.role == 'goalkeeper':
                            target_position = np.array([5, self.field.width / 2], dtype=np.float64)
                        elif player.role in ['defender', 'midfielder']:
                            target_position = np.array([np.random.uniform(0, 50), np.random.uniform(0, self.field.width)], dtype=np.float64)
                        else:
                            target_position = np.array([np.random.uniform(50, 105), np.random.uniform(0, self.field.width)], dtype=np.float64)

                        player.move_to_position(target_position, self.physics_engine, dt)

                        print(f"Player {player.player_id} ({player.role}) moved to {player.position}")

                        #pass
                        if np.random.rand() < 0.1:  # Random chance to pass
                            target_player = np.random.choice(self.team_a_players)
                            player.pass_ball(self.ball, target_player.position, force=10)
                            player.stamina = self.physics_engine.update_stamina(player.stamina, dt, effort_level=0.5, action_type="stand")
                            print(f"Player {player.player_id} passed the ball to Player {target_player.player_id}")
                        
                        # shoot towards goal 
                        if np.random.rand() < 0.05:  # Random chance to shoot
                            goal_position = np.array([105, 34])
                            player.shoot(self.ball, goal_position, force=20)
                            print(f"Player {player.player_id} shoots towards the goal at position {goal_position}")

                self.ball.update_position(dt)

                if self.rules.check_out_of_bounds(self.ball.get_position()):
                    self.rules.handle_throw_in(self.ball.get_position(), 'team_a')

                if self.field.is_in_goal_area(self.ball.get_position()):
                    self.rules.award_goal('team_a')
                    self.total_goals['team_a'] += 1
                    break

                print(f"Half {half}, Step {step}: Ball position: {self.ball.get_position()}")

            if half == 1:
                print("Half-time break. Players rest.")

        print("Full Time!")
        if self.total_goals['team_a'] > self.total_goals['team_b']:
            print("Team A Wins!")
        elif self.total_goals['team_b'] > self.total_goals['team_a']:
            print("Team B Wins!")
        else:
            print("Match Drawn!")

if __name__ == "__main__":
    sim = FootballSimulation(half_duration=1)
    sim.run_simulation()
