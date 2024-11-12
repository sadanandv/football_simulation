# environment/player.py

import numpy as np

class Player:
    def __init__(self, player_id, position, skill=0.7):
        self.player_id = player_id
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array([0.0, 0.0], dtype=np.float64)
        self.stamina = 100.0
        self.skill = skill

    def dribble(self, acceleration, physics_engine, dt):
        """Dribble while maintaining possession"""
        stamina_factor = max(self.stamina / 100.0, 0.2)
        effective_acceleration = acceleration * stamina_factor * self.skill
        self.position, self.velocity = physics_engine.calculate_movement(self.position, self.velocity, effective_acceleration, dt, self.stamina)
        self.stamina = physics_engine.update_stamina(self.stamina, dt, effort_level=1.2, action_type="dribble")

    def pass_ball(self, ball, target_position, force):
        """Pass the ball to a teammate"""
        ball.pass_ball(force, target_position)

    def shoot(self, ball, goal_position, force):
        """Shoot towards the goal"""
        ball.shoot_goal(force, goal_position)

    def tackle(self, target_player):
        """Attempt to tackle another player"""
        if np.linalg.norm(self.position - target_player.position) < 2.0:
            success_probability = self.skill * 0.8
            if np.random.rand() < success_probability:
                return True
        return False

    def move_to_position(self, target_position, physics_engine, dt):
        """Move to a target position"""
        if np.linalg.norm(self.position - target_position) < 1e-3:
            return

        direction = target_position - self.position
        if np.linalg.norm(direction) != 0:
            direction = direction / np.linalg.norm(direction)
        acceleration = direction * 0.2
        self.position, self.velocity = physics_engine.calculate_movement(self.position, self.velocity, acceleration, dt, self.stamina)
        self.stamina = physics_engine.update_stamina(self.stamina, dt, effort_level=1.0, action_type="sprint")


if __name__ == "__main__":
    from physics_engine import PhysicsEngine
    from ball import Ball

    player = Player(player_id=1, position=[10.0, 34.0])
    physics = PhysicsEngine()
    ball = Ball()

    player.dribble(np.array([0.1, 0.05]), physics, dt=0.5)
    print(f"Player Position after Dribbling: {player.position}")

    player.pass_ball(ball, target_position=np.array([20.0, 40.0]), force=10)
    print(f"Ball Position after Passing: {ball.get_position()}")
