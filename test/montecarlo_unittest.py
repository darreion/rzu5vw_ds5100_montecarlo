import unittest
import numpy as np
import pandas as pd
from Montecarlo.montecarlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    def test_init(self):
        """Test Die initialization"""
        faces = np.array(['A', 'B', 'C'])
        die = Die(faces)
        self.assertEqual(len(die.show()), 3)

    def test_init_with_non_numpy_array(self):
        """Test Die initialization shows error if faces are not a numpy array."""
        with self.assertRaises(TypeError):
            Die(['A', 'B', 'C'])

    def test_init_with_non_unique_faces(self):
        """Test Die initialization shows error if faces are not unique."""
        faces = np.array(['A', 'A', 'B'])
        with self.assertRaises(ValueError):
            Die(faces)

    def test_change_weight_invalid_face(self):
        """Test changing weight of a face not existing in the die."""
        faces = np.array(['A', 'B', 'C'])
        die = Die(faces)
        with self.assertRaises(IndexError):
            die.change_weight('D', 2)

    def test_change_weight_invalid_weight_type(self):
        """Test changing weight with a non-numeric weight."""
        faces = np.array(['A', 'B', 'C'])
        die = Die(faces)
        with self.assertRaises(TypeError):
            die.change_weight('A', 'heavy')

    def test_roll(self):
        """Test rolling the die produces results within expected faces."""
        faces = np.array(['A', 'B', 'C'])
        die = Die(faces)
        results = die.roll(10)
        for result in results:
            self.assertIn(result, faces)

    def test_show(self):
        """Test show method returns DataFrame of correct format."""
        faces = np.array(['A', 'B', 'C'])
        die = Die(faces)
        df = die.show()
        self.assertTrue('weight' in df.columns)

class TestGame(unittest.TestCase):
    def test_game_play(self):
        """Test playing a game produces the correct number of results."""
        faces = np.array(['1', '2', '3'])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(5)
        results = game.show()
        self.assertEqual(len(results), 5)

    def test_game_results_format(self):
        """Test the format of the game results in wide form."""
        faces = np.array(['1', '2', '3'])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(3)
        results = game.show('wide')
        self.assertEqual(len(results.columns), 2)

    def test_invalid_form(self):
        """Test show method with invalid form raises ValueError."""
        faces = np.array(['1', '2', '3'])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(3)
        with self.assertRaises(ValueError):
            game.show('invalid')

class TestAnalyzer(unittest.TestCase):
    
    def setUp(self):
    
        die = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die])
        self.analyzer = Analyzer(game)  # This is critical
        
    def test_jackpot_count(self):
       
        jackpots = self.analyzer.jackpot() 
        print(f"Jackpot count returned: {jackpots}") 
        
        self.assertIsInstance(jackpots, int) 
    

    def test_combo_count(self):
        """Test combo count returns DataFrame with expected indices."""
        faces = np.array(['1', '2', '3'])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(100)
        analyzer = Analyzer(game)
        combo_df = analyzer.combo_count()
        self.assertTrue(isinstance(combo_df, pd.DataFrame))

    def test_face_counts_per_roll(self):
        """Test face counts per roll returns correct DataFrame format."""
        faces = np.array(['1', '2', '3'])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(10)
        analyzer = Analyzer(game)
        count_df = analyzer.face_counts_per_roll()
        self.assertTrue(isinstance(count_df, pd.DataFrame))

    def test_permutation_count(self):
        """Test permutation count returns DataFrame with expected"""
        faces = np.array(['1', '2', '3'])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(100)
        analyzer = Analyzer(game)
        perm_df = analyzer.permutation_count()
        self.assertTrue(isinstance(perm_df, pd.DataFrame))

if __name__ == '__main__':
    unittest.main()
