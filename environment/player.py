# environment/player.py

import numpy as np
from environment.physics_engine import PhysicsEngine
from agents.team_agent import TeamAgent
from utils.trait_utils import generate_trait_profile
from utils.chemistry_utils import calculate_chemistry

class Player:
    def __init__(self, player_id, position, skill=0.7, traits=None, physical_attributes=None, coach=None, team=None):
        self.player_id = player_id
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array([0.0, 0.0], dtype=np.float64)
        self.stamina = 100.0
        self.skill = skill
        self.traits = traits if traits else generate_trait_profile()
        self.physical_attributes = physical_attributes if physical_attributes else self.initialize_random_physical_attributes()
        self.coach = coach
        self.team = team
        self.chemistry = 0.5  # Default value for chemistry, to be calculated later.

        self.role = "midfielder"  # Default role, to be reassigned later by team strategy.
        # Agent assigned later in simulation initialization with all team players
        self.agent = None

    def initialize_random_physical_attributes(self):
        """Initialize random physical attributes for a player."""
        return {
            "speed": np.random.randint(50, 100),
            "acceleration": np.random.randint(50, 100),
            "agility": np.random.randint(50, 100),
            "strength": np.random.randint(50, 100),
            "stamina": np.random.randint(50, 100),
            "jumping_ability": np.random.randint(50, 100),
            "balance": np.random.randint(50, 100),
            "coordination": np.random.randint(50, 100),
            "flexibility": np.random.randint(50, 100),
            "injury_resistance": np.random.randint(50, 100),
            "dribbling_skill": np.random.randint(50, 100),
            "shooting_accuracy": np.random.randint(50, 100),
            "passing_accuracy": np.random.randint(50, 100),
            "tackling_ability": np.random.randint(50, 100),
            "vision": np.random.randint(50, 100),
            "composure": np.random.randint(50, 100),
            "reaction_time": np.random.randint(50, 100),
            "preferred_foot": np.random.choice(['Left', 'Right', 'Both']),
            "height": np.random.uniform(160, 200),
            "weight": np.random.uniform(60, 100)
        }

    def update_chemistry(self, teammates):
        """Update the player's chemistry based on teammates."""
        total_chemistry = 0
        for teammate in teammates:
            if teammate.player_id != self.player_id:
                total_chemistry += calculate_chemistry(self, teammate)
        self.chemistry = total_chemistry / (len(teammates) - 1)

    def dribble(self, acceleration, physics_engine, dt):
        """Dribble while maintaining possession."""
        stamina_factor = max(self.stamina / 100.0, 0.2)
        effective_acceleration = acceleration * stamina_factor * self.skill * self.traits['Aggression']
        self.position, self.velocity = physics_engine.calculate_movement(
            self.position, self.velocity, effective_acceleration, dt, self.stamina
        )
        self.stamina = physics_engine.update_stamina(self.stamina, dt, effort_level=1.2, action_type="dribble")

    def pass_ball(self, ball, target_position, force):
        """Pass the ball to a teammate."""
        ball.pass_ball(force, target_position)
        # Influence of traits like 'team spirit' and 'vision' is considered.
        self.stamina -= force * 0.02  # Reduced stamina based on the passing effort.

    def shoot(self, ball, goal_position, force):
        """Shoot towards the goal."""
        ball.shoot_goal(force, goal_position)
        self.stamina -= force * 0.05  # Reduced stamina based on the shot effort.

    def tackle(self, target_player):
        """Attempt to tackle another player."""
        if np.linalg.norm(self.position - target_player.position) < 2.0:
            success_probability = self.skill * 0.8 * self.traits['aggression']
            if np.random.rand() < success_probability:
                return True
        return False

    def move_to_position(self, target_position, physics_engine, dt):
        """Move to a target position."""
        if np.linalg.norm(self.position - target_position) < 1e-3:
            return

        direction = target_position - self.position
        if np.linalg.norm(direction) != 0:
            direction = direction / np.linalg.norm(direction)
        acceleration = direction * 0.2
        self.position, self.velocity = physics_engine.calculate_movement(
            self.position, self.velocity, acceleration, dt, self.stamina
        )
        self.stamina = physics_engine.update_stamina(self.stamina, dt, effort_level=1.0, action_type="sprint")

    def make_decision(self, dt):
        """Make a decision based on the player's current state and role."""
        if self.agent:
            self.agent.decide_action(self, dt)  # Pass the player instance and dt to decide_action

if __name__ == "__main__":
    from ball import Ball
    physics = PhysicsEngine()
    ball = Ball()

    player = Player(player_id=1, position=[10.0, 34.0])
    player.dribble(np.array([0.1, 0.05]), physics, dt=0.5)
    #print(f"Player Position after Dribbling: {player.position}")

    player.pass_ball(ball, target_position=np.array([20.0, 40.0]), force=10)
   # print(f"Ball Position after Passing: {ball.get_position()}")
