# visualization/player_timeline.py
from utils.log_parser_utils import parse_log_file, extract_player_positions
from mplsoccer import Pitch
import matplotlib.pyplot as plt

def player_timeline(log_file_path, player_id):
    # Parse log data
    events = parse_log_file(log_file_path)
    player_positions_df = extract_player_positions(events)

    # Filter the DataFrame for the specified player
    player_data = player_positions_df[player_positions_df['player_id'] == player_id]

    if player_data.empty:
        print(f"No data available for Player {player_id}")
        return

    # Extract position data
    x_positions = player_data['position'].apply(lambda pos: pos[0])
    y_positions = player_data['position'].apply(lambda pos: pos[1])

    # Create a football pitch to visualize player movements
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 7))

    # Plot player trajectory over the pitch
    pitch.plot(x_positions, y_positions, ax=ax, color='red', linestyle='-', marker='o', label=f'Player {player_id}')
    plt.title(f"Player {player_id} Timeline - Position on the Pitch")
    plt.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    log_file_path = "data/logs/game_log_20241114_142736.txt"
    player_timeline(log_file_path, player_id=21)
