# utils/log_parser_utils.py
import re
import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

def parse_log_file(log_file_path):
    """
    Parses a log file to extract event data.

    Parameters:
        log_file_path (str): The path to the log file.

    Returns:
        dict: Dictionary containing parsed events categorized by event types.
    """
    events = {
        'goals': [],
        'passes': [],
        'tackles': [],
        'substitutions': [],
        'fouls': [],
        'resting': [],
        'ball_position': [],
        'player_positions': [],
        'dribbling': [],
        'throw_ins': [],
        'general': []
    }

    # Regular expressions for parsing specific events
    goal_pattern = re.compile(r"Player (\d+) scores a goal for (team_[a-b])!")
    pass_pattern = re.compile(r"Player (\d+) passed the ball to Player (\d+) at position \[(\d+)\. (\d+)\.")
    tackle_pattern = re.compile(r"Player (\d+) successfully tackled Player (\d+)")
    substitution_pattern = re.compile(r"Player (\d+) is being substituted.")
    foul_pattern = re.compile(r"Player (\d+) has received a red card!")
    resting_pattern = re.compile(r"Player (\d+) is resting to regain stamina. Current stamina: ([\-0-9.]+)")
    ball_position_pattern = re.compile(r"Half (\d+), Step (\d+): Ball position: \[([-\d.]+)\s+([-\d.]+)\]$")
    player_position_pattern = re.compile(r"Half (\d+), Step (\d+): Player (\d+) Position: \[([-\d.]+)\s+([-\d.]+)\], Stamina: ([-\d.]+)$")
    dribbling_pattern = re.compile(r"^Player (\d+) is dribbling\. Current position: \[([-\d.]+)\s+([-\d.]+)\]$")
    throw_in_pattern = re.compile(r"Throw-in awarded to (team_[a-b]). A player is assigned to take it.")

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            line = line.strip()
            events['general'].append(line)

            try:
                # Extracting goals
                if (goal_match := goal_pattern.search(line)):
                    player_id, team = goal_match.groups()
                    events['goals'].append({'player_id': int(player_id), 'team': team})
                    continue

                # Extracting passes
                if (pass_match := pass_pattern.search(line)):
                    player_id, target_player_id, x, y = pass_match.groups()
                    events['passes'].append({'player_id': int(player_id), 'target_player_id': int(target_player_id), 'position': (float(x), float(y))})
                    continue

                # Extracting tackles
                if (tackle_match := tackle_pattern.search(line)):
                    player_id, opponent_id = tackle_match.groups()
                    events['tackles'].append({'player_id': int(player_id), 'opponent_id': int(opponent_id)})
                    continue

                # Extracting substitutions
                if (substitution_match := substitution_pattern.search(line)):
                    player_id = substitution_match.group(1)
                    events['substitutions'].append({'player_id': int(player_id)})
                    continue

                # Extracting fouls
                if (foul_match := foul_pattern.search(line)):
                    player_id = foul_match.group(1)
                    events['fouls'].append({'player_id': int(player_id)})
                    continue

                # Extracting resting events
                if (resting_match := resting_pattern.search(line)):
                    player_id, stamina = resting_match.groups()
                    events['resting'].append({'player_id': int(player_id), 'stamina': float(stamina)})
                    continue

                # Extracting ball positions
                if (ball_position_match := ball_position_pattern.search(line)):
                    half, step, x, y = ball_position_match.groups()
                    events['ball_position'].append({'half': int(half), 'step': int(step), 'position': (float(x), float(y))})
                    continue

                # Extracting player positions
                if (player_position_match := player_position_pattern.search(line)):
                    half, step, player_id, x, y, stamina = player_position_match.groups()
                    events['player_positions'].append({'half': int(half), 'step': int(step), 'player_id': int(player_id), 'position': (float(x), float(y)), 'stamina': float(stamina)})
                    continue

                # Extracting dribbling events
                if (dribbling_match := dribbling_pattern.search(line)):
                    player_id, x, y = dribbling_match.groups()
                    events['dribbling'].append({'player_id': int(player_id), 'position': (float(x), float(y))})
                    continue

                # Extracting throw-ins
                if (throw_in_match := throw_in_pattern.search(line)):
                    team = throw_in_match.group(1)
                    events['throw_ins'].append({'team': team})
                    continue

            except Exception as e:
                logging.error(f"Failed to parse line: '{line}' due to {e}")

    return events

def extract_player_statistics(events):
    """
    Extract player statistics based on parsed event data.

    Parameters:
        events (dict): Dictionary of events parsed from the log file.

    Returns:
        pd.DataFrame: DataFrame containing player statistics.
    """
    player_stats = {}

    for goal in events['goals']:
        player_id = goal['player_id']
        player_stats.setdefault(player_id, {'goals': 0, 'passes': 0, 'tackles': 0, 'fouls': 0, 'resting': 0, 'dribbling': 0})
        player_stats[player_id]['goals'] += 1

    for pass_event in events['passes']:
        player_id = pass_event['player_id']
        player_stats.setdefault(player_id, {'goals': 0, 'passes': 0, 'tackles': 0, 'fouls': 0, 'resting': 0, 'dribbling': 0})
        player_stats[player_id]['passes'] += 1

    for tackle in events['tackles']:
        player_id = tackle['player_id']
        player_stats.setdefault(player_id, {'goals': 0, 'passes': 0, 'tackles': 0, 'fouls': 0, 'resting': 0, 'dribbling': 0})
        player_stats[player_id]['tackles'] += 1

    for foul in events['fouls']:
        player_id = foul['player_id']
        player_stats.setdefault(player_id, {'goals': 0, 'passes': 0, 'tackles': 0, 'fouls': 0, 'resting': 0, 'dribbling': 0})
        player_stats[player_id]['fouls'] += 1

    for rest in events['resting']:
        player_id = rest['player_id']
        player_stats.setdefault(player_id, {'goals': 0, 'passes': 0, 'tackles': 0, 'fouls': 0, 'resting': 0, 'dribbling': 0})
        player_stats[player_id]['resting'] += 1

    for dribble in events['dribbling']:
        player_id = dribble['player_id']
        player_stats.setdefault(player_id, {'goals': 0, 'passes': 0, 'tackles': 0, 'fouls': 0, 'resting': 0, 'dribbling': 0})
        player_stats[player_id]['dribbling'] += 1

    # Convert dictionary to DataFrame
    player_stats_df = pd.DataFrame.from_dict(player_stats, orient='index').reset_index()
    player_stats_df.rename(columns={'index': 'player_id'}, inplace=True)
    return player_stats_df

def extract_ball_trajectory(events):
    """
    Extract ball trajectory from parsed event data.

    Parameters:
        events (dict): Dictionary of events parsed from the log file.

    Returns:
        pd.DataFrame: DataFrame containing ball trajectory information.
    """
    ball_positions = events.get('ball_position', [])
    if not ball_positions:
        logging.warning("'ball_position' key not found in events or no ball positions available.")
        return pd.DataFrame()
    return pd.DataFrame(ball_positions)

def extract_player_positions(events):
    """
    Extract player positions from parsed event data.

    Parameters:
        events (dict): Dictionary of events parsed from the log file.

    Returns:
        pd.DataFrame: DataFrame containing player position information over time.
    """
    player_positions = events.get('player_positions', [])
    return pd.DataFrame(player_positions)

if __name__ == "__main__":
    # Example usage
    log_file_path = "data/logs/game_log_20241114_125614.txt"
    events = parse_log_file(log_file_path)
    player_stats_df = extract_player_statistics(events)
    ball_trajectory_df = extract_ball_trajectory(events)
    player_positions_df = extract_player_positions(events)
    print(player_stats_df)
    print(ball_trajectory_df)
    print(player_positions_df)
