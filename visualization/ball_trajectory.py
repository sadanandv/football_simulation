# visualization/ball_trajectory.py
from utils.log_parser_utils import parse_log_file, extract_ball_trajectory
from mplsoccer import Pitch
import matplotlib.pyplot as plt

def ball_trajectory(log_file_path):
    # Extract events from log file
    events = parse_log_file(log_file_path)
    ball_trajectory_df = extract_ball_trajectory(events)

    if ball_trajectory_df.empty:
        print("No ball trajectory data available to plot.")
        return

    # Extract X and Y positions
    x_positions = ball_trajectory_df['position'].apply(lambda pos: pos[0])
    y_positions = ball_trajectory_df['position'].apply(lambda pos: pos[1])

    # Create a football pitch using mplsoccer
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 7))

    # Plot the ball trajectory on the pitch
    pitch.plot(x_positions, y_positions, ax=ax, color='blue', linestyle='-', marker='o')
    plt.title("Ball Trajectory Over the Match")
    plt.show()

if __name__ == "__main__":
    log_file_path = "data/logs/game_log_20241114_142736.txt"
    ball_trajectory(log_file_path)
