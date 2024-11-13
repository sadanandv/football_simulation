# Football Simulation Environment

This directory contains modules for simulating a football game environment, including player actions, ball dynamics, field settings, and game rules. The code is designed to be modular and extendable, allowing the implementation of different strategies, player attributes, and interactions.

## **Directory Structure**

- **`ball.py`**: Defines the `Ball` class, which models the ball's properties and dynamics, including kicking, passing, and shooting.
- **`field.py`**: Defines the `FootballField` class, which models the dimensions of the field, goal areas, penalty boxes, and other key field features.
- **`physics_engine.py`**: Implements the `PhysicsEngine` class that provides physics-based calculations, including friction, air resistance, and movement calculations.
- **`player.py`**: Contains the `Player` class, representing individual players with attributes like position, skill, stamina, and new features such as physical traits and action decisions.
- **`rules.py`**: Contains the `GameRules` class, responsible for managing game rules, including offsides, fouls, goals, and substitutions.
- **`simulation.py`**: Implements the `FootballSimulation` class, which runs the overall game simulation, managing teams, players, actions, and match flow.

## **Getting Started**

### **Dependencies**

- Python 3.6+
- Numpy

To install the dependencies, run:
```sh
pip install -r requirements.txt
```

### **Usage**

To run a full simulation, use the `simulation.py` file. The simulation initializes players, field, and ball, and simulates two halves of a football match:

```sh
python simulation.py
```

You can modify the parameters such as the **half duration**, **player roles**, and **team formations** by editing the `FootballSimulation` class in `simulation.py`.

### **Modules Overview**

#### **Ball Module (`ball.py`)**
- **Class**: `Ball`
  - **Attributes**: Position, velocity, friction.
  - **Methods**:
    - `kick(force, direction)`: Applies a force to kick the ball in a given direction.
    - `pass_ball(force, target_position)`: Passes the ball to a specific target.
    - `shoot_goal(force, goal_position)`: Shoots the ball towards the goal.
    - `update_position(dt)`: Updates the ball's position based on its velocity and friction.

#### **Field Module (`field.py`)**
- **Class**: `FootballField`
  - **Attributes**: Length, width, goal areas, penalty areas.
  - **Methods**:
    - `is_in_goal_area(position)`: Checks if a given position is inside a goal area.
    - `is_in_penalty_area(position)`: Checks if a given position is inside a penalty area.

#### **Physics Engine (`physics_engine.py`)**
- **Class**: `PhysicsEngine`
  - **Methods**:
    - `update_position(position, velocity, dt)`: Updates a player's position based on velocity and time step.
    - `apply_friction(velocity, dt)`: Applies friction to reduce velocity over time.
    - `calculate_movement(position, velocity, acceleration, dt, stamina)`: Calculates movement based on physics and stamina.

#### **Player Module (`player.py`)**
- **Class**: `Player`
  - **Attributes**: Player ID, position, velocity, stamina, skill level, physical attributes, traits.
  - **Methods**:
    - `dribble(acceleration, physics_engine, dt)`: Dribble with the ball while maintaining control.
    - `pass_ball(ball, target_position, force)`: Pass the ball to a teammate.
    - `shoot(ball, goal_position, force)`: Shoot towards the goal.
    - `move_to_position(target_position, physics_engine, dt)`: Move to a target position.

#### **Game Rules Module (`rules.py`)**
- **Class**: `GameRules`
  - **Attributes**: Score, fouls, yellow cards, red cards.
  - **Methods**:
    - `check_offside(player_position, ball_position, team, opposing_players)`: Checks if a player is offside.
    - `award_goal(team)`: Awards a goal to a team.
    - `commit_foul(team, player_id, position)`: Records a foul and determines if penalties are needed.

#### **Simulation Module (`simulation.py`)**
- **Class**: `FootballSimulation`
  - **Attributes**: Field, physics engine, rules, ball, teams, half duration.
  - **Methods**:
    - `assign_roles()`: Assigns roles to players based on formations.
    - `run_simulation()`: Runs the match simulation, iterating through player actions and game events.
