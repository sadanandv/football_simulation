# environment/rules.py

class GameRules:
    def __init__(self, field):
        self.field = field
        self.score = {'team_a': 0, 'team_b': 0}
        self.fouls = {'team_a': 0, 'team_b': 0}
        self.yellow_cards = {}
        self.red_cards = {}

    def check_offside(self, player_position, ball_position, team, opposing_players):
        """Check if a player is in an offside position"""
        if team == 'team_a' and player_position[0] > self.field.length / 2:
            defending_line = max(player.position[0] for player in opposing_players)
            return player_position[0] > defending_line and player_position[0] > ball_position[0]
        elif team == 'team_b' and player_position[0] < self.field.length / 2:
            defending_line = min(player.position[0] for player in opposing_players)
            return player_position[0] < defending_line and player_position[0] < ball_position[0]
        return False

    def award_goal(self, team):
        """Award a goal to a team"""
        self.score[team] += 1
        print(f"Goal awarded to {team}! Current score: {self.score}")

    def commit_foul(self, team, player_id, position):
        """Record a foul committed by a team"""
        self.fouls[team] += 1
        if player_id not in self.yellow_cards:
            self.yellow_cards[player_id] = 1
        else:
            self.yellow_cards[player_id] += 1
            if self.yellow_cards[player_id] >= 2:
                self.red_cards[player_id] = True
                print(f"Player {player_id} has received a red card!")

        # Check if foul occurred inside penalty area
        if self.field.is_in_penalty_area(position):
            print(f"Penalty awarded to {'team_b' if team == 'team_a' else 'team_a'}")

    def handle_throw_in(self, ball_position, team):
        """Handle throw-in after ball goes out of bounds over the sideline"""
        if self.field.is_in_sideline_area(ball_position):
            print(f"Throw-in awarded to {team}. A player is assigned to take it.")

    def handle_corner_kick(self, ball_position, last_team):
        """Handle corner kick scenario"""
        if ball_position[0] <= 0 or ball_position[0] >= self.field.length:
            if last_team == 'defending':
                print("Corner kick awarded to attacking team.")

    def handle_free_kick(self, foul_position, team):
        """Handle free kick awarded after a foul"""
        print(f"Free kick awarded to {team} at position {foul_position}")

    def check_out_of_bounds(self, ball_position):
        """Check if the ball is out of bounds"""
        x, y = ball_position
        if x < 0 or x > self.field.length or y < 0 or y > self.field.width:
            return True
        return False

    def substitution(self, player, new_player):
        """Substitute a player"""
        if player.stamina < 20:
            print(f"Player {player.player_id} is being substituted.")
            return new_player
        return player

    def get_score(self):
        """Return the current score"""
        return self.score


if __name__ == "__main__":
    from field import FootballField

    field = FootballField()
    rules = GameRules(field)

    '''print("Initial score:", rules.get_score())
    rules.award_goal('team_a')
    player_position = (60, 34)
    print("Is player offside (team_a)?", rules.check_offside(player_position, (52.5, 34), 'team_a', []))
    rules.commit_foul('team_b', player_id=10, position=(16, 30))  # Inside penalty area
    rules.handle_throw_in(ball_position=(106, 34), team='team_a')  # Out of bounds
    rules.handle_corner_kick(ball_position=(0, 30), last_team='defending')  # Corner kick scenario
    rules.handle_free_kick(foul_position=(50, 40), team='team_a')  # Free kick after a foul'''
