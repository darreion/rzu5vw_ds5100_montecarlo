# Montecarlo Simulator



## Meta
- **Author:** Darreion Bailey
- **Contact:** [rzu5vw@virginia.edu](mailto:rzu5vw@virginia.edu)
- **License:** [MIT](https://opensource.org/licenses/MIT)

## Synopsis

```python
from montecarlo import Die, Game, Analyzer

# Create a die with six faces
die = Die(np.array([1, 2, 3, 4, 5, 6]))

# Initialize a game with one die
game = Game([die])

# Play the game
game.play(10)

# Analyze the game results
analyzer = Analyzer(game)
jackpot_count = analyzer.jackpot()

### 3. API

  ### Class: Die

- `__init__(faces: np.ndarray)`
  - Initializes a new die with given faces.
- `change_weight(face, weight)`
  - Changes the weight for a specific face.
- `roll(num_rolls=1)`
  - Rolls the die the specified number of times.
- `show()`
  - Returns a DataFrame showing the faces and weights of the die.

  ### Class: Game

- `__init__(dice: List[Die])`
  - Initializes a new game with a list of Die objects.
- `play(num_rolls)`
  - Simulates rolling all dice the specified number of times.
- `show(form='wide')`
  - Shows game results in either 'wide' or 'narrow' format.

  ### Class: Analyzer

- `__init__(game: Game)`
  - Initializes an analyzer for the given game results.
- `jackpot()`
  - Calculates how many times all dice showed the same face.
- `face_counts_per_roll()`
  - Returns a DataFrame with counts of each face per roll.
- `combo_count()`
  - Calculates counts of distinct combinations of faces rolled.
- `permutation_count()`
  - Calculates counts of distinct permutations of faces rolled.
