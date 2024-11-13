#utils/chemisrty_utils.py

import numpy as np

def generate_trait_profile():
    traits = {
        "Drive and Determination": np.random.uniform(0, 1),
        "Aggression": np.random.uniform(0, 1),
        "Mental Toughness": np.random.uniform(0, 1),
        "Conscientiousness": np.random.uniform(0, 1),
        "Responsibility": np.random.uniform(0, 1),
        "Leadership": np.random.uniform(0, 1),
        "Self-Control": np.random.uniform(0, 1),
        "Self-Confidence": np.random.uniform(0, 1),
        "Coachability": np.random.uniform(0, 1),
        "Truthfulness": np.random.uniform(0, 1),
        "Team Spirit": np.random.uniform(0, 1),
        "Learnability": np.random.uniform(0, 1),
        "Communication": np.random.uniform(0, 1),
        "Game Sense": np.random.uniform(0, 1)
    }
    return traits
