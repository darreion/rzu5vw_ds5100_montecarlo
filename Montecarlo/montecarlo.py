import numpy as np
import pandas as pd

class Die:
    """
    Represents a die with multiple faces and weights, which can be rolled to randomly select a face.

    """

    def __init__(self, faces):
        """
        Initializes the die with given faces and default weights.

        """
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be a numpy array.")
        if len(faces) != len(set(faces)):
            raise ValueError("Faces must be distinct.")
        
        self._df = pd.DataFrame({
            'face': faces,
            'weight': np.ones(len(faces))
        }).set_index('face')

    def change_weight(self, face, weight):
        """
        Changes the weight of a specific face.

        """
        if face not in self._df.index:
            raise IndexError("Face not found in the die.")
        if not isinstance(weight, (int, float)):
            raise TypeError("Weight must be a numeric type.")
        
        self._df.loc[face, 'weight'] = weight

    def roll(self, num_rolls=1):
        """
        Rolls the die a specified number of times.

        """
        return self._df.sample(n=num_rolls, replace=True, weights='weight').index.tolist()

    def show(self):
        """
        Shows the current state of the die.

       
        """
        return self._df.copy()
class Game:
    def __init__(self, dice):
        self._dice = dice
        self._results = pd.DataFrame()

    def play(self, num_rolls):
        results = {}
        for i, die in enumerate(self._dice):
            rolls = [die.roll()[0] for _ in range(num_rolls)]
            results[f"die_{i}"] = rolls
        self._results = pd.DataFrame(results)
        self._results.index.name = 'roll'

    def show(self, form='wide'):
        if form not in ['wide', 'narrow']:
            raise ValueError("Form must be 'wide' or 'narrow'.")
        if form == 'narrow':
            return self._results.stack().reset_index(name='outcome').rename(columns={'level_0': 'roll', 'level_1': 'die'})
        return self._results.copy()


class Analyzer:
    def __init__(self, game):
        if not isinstance(game, Game):
            raise ValueError("Provided object must be a Game instance.")
        self._game = game

    def jackpot(self):
        if self._game._results.empty:
            return 0
        return self._game._results.apply(lambda row: row.nunique() == 1, axis=1).sum()

    def face_counts_per_roll(self):
        if self._game._results.empty:
            print("Results DataFrame is empty.")
            return pd.DataFrame()
        try:
       
            if not all(len(col) == len(self._game._results.index) for col in self._game._results.values.T):
                print("Columns vary in length.")
                return pd.DataFrame()
            return pd.crosstab(index=self._game._results.index, columns=self._game._results.values.flatten())
        except Exception as e:
            print(f"Error in face_counts_per_roll: {e}")
            return pd.DataFrame()



    def combo_count(self):
        if self._game._results.empty:
            return pd.DataFrame()
        return self._game._results.apply(lambda row: tuple(sorted(row)), axis=1).value_counts().to_frame('counts')

    def permutation_count(self):
        if self._game._results.empty:
            return pd.DataFrame()
        return self._game._results.apply(lambda row: tuple(row), axis=1).value_counts().to_frame('counts')
