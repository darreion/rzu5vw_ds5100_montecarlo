import numpy as np
import pandas as pd

class Die:
    """
    Represents a die with multiple faces and weights, which can be rolled to randomly select a face.

    Attributes:
        _df (DataFrame): A private DataFrame holding the faces and weights.
    """

    def __init__(self, faces):
        """
        Initializes the die with given faces and default weights.

        Args:
            faces (np.ndarray): An array of distinct faces.

        Raises:
            TypeError: If faces is not a NumPy array.
            ValueError: If faces are not distinct.
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

        Args:
            face: The face whose weight needs to be changed.
            weight (int or float): The new weight for the face.

        Raises:
            IndexError: If the face is not found.
            TypeError: If the weight is not a numeric type.
        """
        if face not in self._df.index:
            raise IndexError("Face not found in the die.")
        if not isinstance(weight, (int, float)):
            raise TypeError("Weight must be a numeric type.")
        
        self._df.loc[face, 'weight'] = weight

    def roll(self, num_rolls=1):
        """
        Rolls the die a specified number of times.

        Args:
            num_rolls (int): Number of times to roll the die.

        Returns:
            list: Outcomes of the rolls.
        """
        return self._df.sample(n=num_rolls, replace=True, weights='weight').index.tolist()

    def show(self):
        """
        Shows the current state of the die.

        Returns:
            DataFrame: A copy of the die's face and weight data.
        """
        return self._df.copy()
class Game:
    """
    Represents a game played with one or more dice.

    Attributes:
        _dice (list): A list of Die objects.
        _results (DataFrame): A DataFrame holding the results of the game plays.
    """

    def __init__(self, dice):
        """
        Initializes the game with a list of Die objects.

        Args:
            dice (list): A list of Die objects.
        """
        self._dice = dice
        self._results = pd.DataFrame()

    def play(self, num_rolls):
        """
        Plays the game by rolling all dice a specified number of times.

        Args:
            num_rolls (int): Number of rolls.
        """
        results = {
            f"die_{i}": [die.roll()[0] for _ in range(num_rolls)] for i, die in enumerate(self._dice)
        }
        self._results = pd.DataFrame(results)
        self._results.index.name = 'roll'

    def show(self, form='wide'):
        """
        Shows the results of the most recent game play.

        Args:
            form (str): The format to return the results in ('wide' or 'narrow').

        Returns:
            DataFrame: The game results in the specified format.

        Raises:
            ValueError: If the form is not 'wide' or 'narrow'.
        """
        if form not in ['wide', 'narrow']:
            raise ValueError("Form must be 'wide' or 'narrow'.")
        
        if form == 'narrow':
            return self._results.stack().reset_index().rename(columns={0: 'outcome'})
        return self._results.copy()

class Analyzer:
    """
    Analyzes the results from a game.

    Attributes:
        _game (Game): The game whose results to analyze.
    """

    def __init__(self, game):
        """
        Initializes the analyzer with a game object.

        Args:
            game (Game): A game object.

        Raises:
            ValueError: If the passed object is not a Game instance.
        """
        if not isinstance(game, Game):
            raise ValueError("Provided object must be a Game instance.")
        self._game = game

    def jackpot(self):
        """
        Calculates how many times all dice showed the same face.

        Returns:
            int: Number of jackpots.
        """
        return self._game._results.apply(lambda row: row.nunique() == 1, axis=1).sum()

    def face_counts_per_roll(self):
        """
        Calculates the count of each face per roll.

        Returns:
            DataFrame: Counts of each face per roll.
        """
        return pd.crosstab(index=self._game._results.index, columns=self._game._results.values.flatten())

    def combo_count(self):
        """
        Calculates counts of distinct combinations of faces.

        Returns:
            DataFrame: Counts of distinct combinations.
        """
        return self._game._results.apply(lambda row: tuple(sorted(row)), axis=1).value_counts().to_frame('counts')

    def permutation_count(self):
        """
        Calculates counts of distinct permutations of faces.

        Returns:
            DataFrame: Counts of distinct permutations.
        """
        return self._game._results.apply(lambda row: tuple(row), axis=1).value_counts().to_frame('counts')
