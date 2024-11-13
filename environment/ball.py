# environment/ball.py

import numpy as np

class Ball:
    def __init__(self):
        self.position = np.array([52.5, 34.0], dtype=np.float64)  # Initial position (center of field)
        self.velocity = np.array([0.0, 0.0], dtype=np.float64)
        self.friction = 0.015

    def kick(self, force, direction):
        """Apply force to the ball in a given direction"""
        if np.linalg.norm(direction) != 0:
            direction = direction / np.linalg.norm(direction)
        self.velocity = force * direction

    def pass_ball(self, force, target_position):
        """Pass the ball to a target position"""
        direction = target_position - self.position
        if np.linalg.norm(direction) != 0:
            direction = direction / np.linalg.norm(direction)
        self.kick(force, direction)

    def shoot_goal(self, force, goal_position):
        """Shoot the ball towards the goal"""
        direction = goal_position - self.position
        if np.linalg.norm(direction) != 0:
            direction = direction / np.linalg.norm(direction)
        self.kick(force, direction)


    def update_position(self, dt):
        self.position += self.velocity * dt
        if self.position[0] < 0 or self.position[0] > 105:  # Bounce on horizontal boundaries
            self.velocity[0] = -self.velocity[0]
        if self.position[1] < 0 or self.position[1] > 68:  # Bounce on vertical boundaries
            self.velocity[1] = -self.velocity[1]

        self.velocity -= self.velocity * self.friction  # Apply friction


    def get_position(self):
        return self.position


if __name__ == "__main__":
    ball = Ball()
    print(f"Initial Ball Position: {ball.get_position()}")
    ball.kick(force=10, direction=np.array([1.0, 0.5]))
    dt = 0.5

    for step in range(10):
        ball.update_position(dt)
        print(f"Step {step}: Ball Position: {ball.get_position()}")
