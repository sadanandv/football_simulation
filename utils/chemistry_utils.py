#utils/chemisrty_utils.py

def calculate_chemistry(player_1, player_2):
    """
    Calculate chemistry between two players based on shared traits.
    """
    common_traits = [
        player_1.traits[trait] * player_2.traits[trait] for trait in player_1.traits
    ]
    chemistry = sum(common_traits) / len(common_traits)
    return chemistry
