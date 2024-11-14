# visualization/player_heatmap.py
import matplotlib.pyplot as plt
from utils.log_parser_utils import parse_log_file, extract_player_positions
from mplsoccer import Pitch

def player_heatmap(log_file_path, player_id):
    # Extract events from log file
    events = parse_log_file(log_file_path)
    player_positions_df = extract_player_positions(events)

    # Filter positions for the specific player
    player_data = player_positions_df[player_positions_df['player_id'] == player_id]

    if player_data.empty:
        print(f"No data found for player {player_id}.")
        return

    # Extract X and Y positions
    x_positions = [pos[0] for pos in player_data['position']]
    y_positions = [pos[1] for pos in player_data['position']]

    # Generate heatmap on pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 6))
    pitch.kdeplot(x_positions, y_positions, ax=ax, fill=True, cmap="Reds", alpha=0.6)
    plt.title(f"Heatmap for Player {player_id}")
    plt.show()

if __name__ == "__main__":
    log_file_path = "data/logs/game_log_20241114_142736.txt"
    player_heatmap(log_file_path, player_id=1)
