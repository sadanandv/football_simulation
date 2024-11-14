# visualization/match_replay.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils.log_parser_utils import parse_log_file, extract_ball_trajectory, extract_player_positions
from mplsoccer import Pitch

def match_replay(log_file_path):
    # Extract events from log file
    events = parse_log_file(log_file_path)
    ball_trajectory_df = extract_ball_trajectory(events)
    player_positions_df = extract_player_positions(events)

    if ball_trajectory_df.empty or player_positions_df.empty:
        print("No data available for replay.")
        return

    # Create a football pitch using mplsoccer
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 7))

    # Plotting elements for ball and players
    ball, = ax.plot([], [], 'o', color='black', markersize=5, label='Ball')
    player_plots = {player_id: ax.plot([], [], 'o', label=f'Player {player_id}')[0]
                    for player_id in player_positions_df['player_id'].unique()}

    def init():
        ball.set_data([], [])
        for plot in player_plots.values():
            plot.set_data([], [])
        return [ball] + list(player_plots.values())

    def animate(i):
        # Update ball position
        if i < len(ball_trajectory_df):
            ball_x, ball_y = ball_trajectory_df.loc[i, 'position']
            ball.set_data(ball_x, ball_y)

        # Update each player's position
        frame_data = player_positions_df[player_positions_df['step'] == i]
        for player_id, player_plot in player_plots.items():
            if player_id in frame_data['player_id'].values:
                player_x, player_y = frame_data[frame_data['player_id'] == player_id]['position'].iloc[0]
                player_plot.set_data(player_x, player_y)

        return [ball] + list(player_plots.values())

    ani = animation.FuncAnimation(fig, animate, init_func=init,
                                  frames=len(ball_trajectory_df), blit=True, interval=50, repeat=False)
    ax.legend()
    plt.show()

if __name__ == "__main__":
    log_file_path = "data/logs/game_log_20241114_142736.txt"
    match_replay(log_file_path)
