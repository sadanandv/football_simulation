# visualization/player_statistics.py
import matplotlib.pyplot as plt
import seaborn as sns
from utils.log_parser_utils import parse_log_file, extract_player_statistics

def player_statistics(log_file_path):
    # Parse log data and extract player statistics
    events = parse_log_file(log_file_path)
    player_stats_df = extract_player_statistics(events)

    if player_stats_df.empty:
        print("No player statistics available.")
        return

    # Plotting aggregated statistics for each player
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Player Statistics Summary', fontsize=16)

    stats = ['goals', 'passes', 'tackles', 'fouls', 'resting', 'dribbling']
    axes = axes.flatten()

    for i, stat in enumerate(stats):
        sns.barplot(ax=axes[i], x='player_id', y=stat, data=player_stats_df, palette='viridis')
        axes[i].set_title(f"{stat.capitalize()} per Player")
        axes[i].set_xlabel('Player ID')
        axes[i].set_ylabel(stat.capitalize())

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    log_file_path = "data/logs/game_log_20241114_142736.txt"
    player_statistics(log_file_path)
