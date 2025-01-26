import numpy as np
import itertools
import hashlib
import os

output = ""

def write(content):
    global output
    output += content

class MinesweeperPredictor:
    def __init__(self, size=5, num_mines=3, client_seed="", server_seed="", previous_mine_tiles=None):
        self.size = size
        self.num_mines = num_mines
        self.client_seed = client_seed
        self.server_seed = server_seed
        self.previous_mine_tiles = previous_mine_tiles if previous_mine_tiles else []
        self.board = np.zeros((size, size), dtype=int)
        self.probabilities = np.full((size, size), num_mines / (size * size))
        self.mines = []
        self._place_mines()
        self.update_probabilities()

    def _generate_random_sequence(self):
        combined_seed = self.client_seed + self.server_seed
        if self.previous_mine_tiles:
            combined_seed += ''.join(map(str, self.previous_mine_tiles))
        hash_object = hashlib.sha256(combined_seed.encode())
        hex_dig = hash_object.hexdigest()
        seed = int(hex_dig, 16) % (2**32)  # Ensure the seed is within the valid range
        np.random.seed(seed)

    def _tile_to_position(self, tile):
        """Convert a tile number (1 to size*size) to a board position (row, col)."""
        tile -= 1  # Make tile zero-indexed
        row = tile // self.size
        col = tile % self.size
        return (row, col)

    def _place_mines(self):
        self._generate_random_sequence()
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        np.random.shuffle(positions)
        for _ in range(self.num_mines):
            pos = positions.pop()
            self.board[pos] = -1  # -1 represents a mine
            self.mines.append(pos)
        self._calculate_adjacent()

    def _calculate_adjacent(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == -1:
                    continue
                mine_count = sum(self.board[x][y] == -1
                                 for x in range(max(0, i-1), min(self.size, i+2))
                                 for y in range(max(0, j-1), min(self.size, j+2)))
                self.board[i][j] = mine_count

    def update_probabilities(self):
        for i, j in itertools.product(range(self.size), repeat=2):
            self.probabilities[i, j] = self._calculate_mine_probability(i, j)

    def _calculate_mine_probability(self, i, j):
        if self.board[i, j] == -1:
            return 1.0

        # Bayesian calculation based on adjacent tiles
        surrounding = [(x, y) for x in range(max(0, i-1), min(self.size, i+2))
                               for y in range(max(0, j-1), min(self.size, j+2))]
        revealed = [(x, y) for x, y in surrounding if self.board[x, y] != -1]
        mines = sum(self.board[x, y] == -1 for x, y in revealed)
        total = len(surrounding)
        if total == 0:
            return self.num_mines / (self.size * self.size)

        # Additional factors
        revealed_adjacent = sum(1 for x, y in surrounding if self.probabilities[x, y] == 0)
        distance_to_edge = min(i, self.size - i - 1, j, self.size - j - 1)

        # Probability calculation
        probability = mines / total
        probability *= (1 + revealed_adjacent)  # Increase probability for adjacent revealed tiles
        probability *= (1 + distance_to_edge)   # Increase probability for tiles closer to the edge
        return min(probability, 1.0)
    
    

    def display_probabilities(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == -1:
                    write("💣  ")  # Emoji for mine
                else:
                    probability = self.probabilities[i, j]
                    if probability == 0:
                        write("💎  ")  # Emoji for safe tile
                    else:
                        probability_percent = int(probability * 100)
                        write(f"{probability_percent}%  ")
            write("\n")  # Newline after each row

    def display_lines_and_diagonals(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == -1:
                    write("💣 ")
                else:
                    write("⬜️ ")
            write("\n")

        write("\nPotential mine locations (lines and diagonals):")
        for i in range(self.size):
            # Rows
            row = [self.probabilities[i, j] for j in range(self.size)]
            write(f"Row {i + 1}: {row}")

            # Columns
            col = [self.probabilities[j, i] for j in range(self.size)]
            write(f"Column {i + 1}: {col}")

        # Diagonals
        main_diagonal = [self.probabilities[i, i] for i in range(self.size)]
        anti_diagonal = [self.probabilities[i, self.size - i - 1] for i in range(self.size)]
        write(f"Main Diagonal: {main_diagonal}")
        write(f"Anti Diagonal: {anti_diagonal}")

class MonteCarloMinesweeperPredictor(MinesweeperPredictor):
    def __init__(self, size=5, num_mines=3, client_seed="", server_seed="", previous_mine_tiles=None, num_simulations=1000):
        super().__init__(size, num_mines, client_seed, server_seed, previous_mine_tiles)
        self.num_simulations = num_simulations

    def simulate_mine_placement(self):
        mine_counts = np.zeros((self.size, self.size), dtype=int)
        for _ in range(self.num_simulations):
            simulated_board = np.zeros((self.size, self.size), dtype=int)
            positions = [(i, j) for i in range(self.size) for j in range(self.size)]
            np.random.shuffle(positions)
            mine_positions = positions[:self.num_mines]
            for pos in mine_positions:
                simulated_board[pos] = -1
            for i in range(self.size):
                for j in range(self.size):
                    if simulated_board[i][j] == -1:
                        continue
                    mine_count = sum(simulated_board[x][y] == -1
                                     for x in range(max(0, i-1), min(self.size, i+2))
                                     for y in range(max(0, j-1), min(self.size, j+2)))
                    simulated_board[i][j] = mine_count
            mine_counts += (simulated_board == -1).astype(int)
        self.probabilities = mine_counts / self.num_simulations



def runMine(client, server, mines, previous_mine_tiles):
    global output
    output = ""

    previous_mine_positions = [MinesweeperPredictor()._tile_to_position(tile) for tile in previous_mine_tiles]

    game = MinesweeperPredictor(num_mines=mines, client_seed=client, server_seed=server, previous_mine_tiles=previous_mine_tiles)
    game.display_probabilities()
    # game.display_lines_and_diagonals()

    monte_carlo_game = MonteCarloMinesweeperPredictor(num_mines=mines, client_seed=client, server_seed=server, previous_mine_tiles=previous_mine_tiles)
    monte_carlo_game.simulate_mine_placement()
    write("\nʀᴇꜱᴜʟᴛ ᴀᴄᴄᴜʀᴀᴄʏ:\n\n")
    monte_carlo_game.display_probabilities()

    return output
