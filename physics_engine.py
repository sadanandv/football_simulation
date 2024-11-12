# environment/physics_engine.py

import numpy as np

class PhysicsEngine:
    def __init__(self):
        # Physical constants
        self.friction = 0.1  # Friction coefficient to reduce speed over time
        self.air_resistance = 0.02  # Air resistance coefficient

    def update_position(self, position, velocity, dt):
        """Update position based on velocity and time step (dt)"""
        new_position = position + velocity * dt
        return new_position.astype(np.float64)

    def apply_friction(self, velocity, dt):
        """Apply friction to reduce velocity over time"""
        deceleration = self.friction * dt
        new_velocity = velocity * (1 - deceleration)
        return new_velocity.astype(np.float64)

    def apply_air_resistance(self, velocity, dt):
        """Apply air resistance to reduce velocity"""
        new_velocity = velocity * (1 - self.air_resistance * dt)
        return new_velocity.astype(np.float64)

    def calculate_movement(self, position, velocity, acceleration, dt, stamina):
        """Calculate new position and velocity based on acceleration and other factors"""
        stamina_factor = max(stamina / 100.0, 0.2)
        adjusted_acceleration = acceleration * stamina_factor
        adjusted_velocity = velocity + adjusted_acceleration * dt

        adjusted_velocity = self.apply_friction(adjusted_velocity, dt)
        adjusted_velocity = self.apply_air_resistance(adjusted_velocity, dt)

        new_position = self.update_position(position, adjusted_velocity, dt)
        
        return new_position, adjusted_velocity

    def update_stamina(self, stamina, dt, effort_level, action_type):
        stamina_decrease_rate = 0.05 * effort_level
        
        if action_type == "sprint":
            stamina_decrease_rate *= 2.0
        elif action_type == "tackle":
            stamina_decrease_rate *= 1.5
        elif action_type == "walk":
            stamina_decrease_rate *= 0.5
        elif action_type == "stand":
            stamina_decrease_rate *= 0.2

        stamina -= stamina_decrease_rate * dt
        stamina = max(stamina, 0)
        return stamina


if __name__ == "__main__":
    physics = PhysicsEngine()
    position = np.array([0, 0])
    velocity = np.array([5, 3])  # Velocity in x and y directions
    acceleration = np.array([0.2, 0.1])  # Acceleration in x and y directions
    stamina = 100.0  # Player starts with full stamina
    dt = 0.5  # Time step (in seconds)
    for _ in range(10):
        position, velocity = physics.calculate_movement(position, velocity, acceleration, dt, stamina)
        print("Position:", position, "Velocity:", velocity)
