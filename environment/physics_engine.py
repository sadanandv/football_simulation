# environment/field.py

class FootballField:
    def __init__(self):
        # Dimensions in meters (Standard Pitch)
        self.length = 105
        self.width = 68

        # Key field areas defined with coordinates (in meters)
        self.goal_area = {
            'left_goal': {
                'x_min': 0,
                'x_max': 5.5,
                'y_min': (self.width / 2) - 9.16,
                'y_max': (self.width / 2) + 9.16,
                'goal_line': 0  # Exact goal line for collision detection
            },
            'right_goal': {
                'x_min': self.length - 5.5,
                'x_max': self.length,
                'y_min': (self.width / 2) - 9.16,
                'y_max': (self.width / 2) + 9.16,
                'goal_line': self.length  # Exact goal line for collision detection
            }
        }

        self.penalty_area = {
            'left_penalty': {
                'x_min': 0,
                'x_max': 16.5,
                'y_min': (self.width / 2) - 20.15,
                'y_max': (self.width / 2) + 20.15,
            },
            'right_penalty': {
                'x_min': self.length - 16.5,
                'x_max': self.length,
                'y_min': (self.width / 2) - 20.15,
                'y_max': (self.width / 2) + 20.15,
            }
        }

        self.center_circle_radius = 9.15

    def get_dimensions(self):
        return self.length, self.width

    def is_in_goal_area(self, position):
        """Check if a position is inside any goal area"""
        x, y = position
        for goal_name, area in self.goal_area.items():
            if area['x_min'] <= x <= area['x_max'] and area['y_min'] <= y <= area['y_max']:
                return True
        return False

    def is_in_penalty_area(self, position):
        """Check if a position is inside any penalty area"""
        x, y = position
        for penalty_name, area in self.penalty_area.items():
            if area['x_min'] <= x <= area['x_max'] and area['y_min'] <= y <= area['y_max']:
                return True
        return False

    def is_in_sideline_area(self, position):
        """Check if a position is near the sideline (used for handling throw-ins)"""
        x, y = position
        if x < 0 or x > self.length or y < 0 or y > self.width:
            return True
        return False


if __name__ == "__main__":
    field = FootballField()
    print("Pitch dimensions (Length x Width):", field.get_dimensions())
    position = (5, 34)
    print("Is position in goal area:", field.is_in_goal_area(position))
    print("Is position in penalty area:", field.is_in_penalty_area(position))
    print("Is position in sideline area:", field.is_in_sideline_area((106, 34)))
