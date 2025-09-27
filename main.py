import tkinter as tk
import argparse
from map_reader import map_reader
from graphics import SkyscraperPuzzleGUI
from CSP import CSP
from Solver import Solver


def find_longest_increasing_subsequence(nums):
 
    length = 1
    highest_value = nums[0]
    for i in range(1, len(nums)):
        if nums[i] > highest_value:
            length += 1
            highest_value = nums[i]
    return length


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Skyscraper Puzzle Solver")
    parser.add_argument(
        "-m",
        "--map",
        type=int,
        choices=[i for i in range(3, 100)],
        required=True,
        help="Map must be less than 100 and greater than 2",
    )
    parser.add_argument(
        "-lcv",
        "--lcv",
        action="store_true",
        help="Enable least constraint value (LCV) as a order-type optimizer",
    )
    parser.add_argument(
        "-mrv",
        "--mrv",
        action="store_true",
        help="Enable minimum remaining values (MRV) as a order-type optimizer",
    )
    parser.add_argument(
        "-maintaining_arc_consistency",
        "--maintaining_arc_consistency",
        action="store_true",
        help="Enable arc consistency to eliminate inconsistent domain values",
    )

    args = parser.parse_args()

    puzzle_clues = map_reader(args.map)  
    grid_data = []
    
    with open(f"map{args.map}.txt", "r") as file:
        lines = file.readlines()[1:-1]
        for line in lines:
            row = line.split("[")[1].split("]")[0]
            row = row.replace("np.int64(", "").replace(")", "")
            grid_data.append(list(map(int, row.split(","))))

    grid_size = len(grid_data)

   
    puzzle_csp = CSP()
    for row in range(1, grid_size + 1):
        for col in range(1, grid_size + 1):
            puzzle_csp.add_variable((row, col), list(range(1, grid_size + 1)))


    window = tk.Tk()
    window.title("Skyscraper Puzzle")

    window_width, window_height = 600, 700
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    top_position = int(screen_height / 2 - window_height / 2)
    right_position = int(screen_width / 2 - window_width / 2)
    window.geometry(f"{window_width}x{window_height}+{right_position}+{top_position}")

    puzzle_solver = Solver(puzzle_csp, args.lcv, args.mrv, args.maintaining_arc_consistency)
    puzzle_gui = SkyscraperPuzzleGUI(window, grid_size, puzzle_solver)
    for col in range(1, grid_size + 1):
        puzzle_gui.add_clue(0, col, puzzle_clues[0][col - 1], "down")  
        puzzle_gui.add_clue(grid_size + 1, col, puzzle_clues[1][col - 1], "up")  
    for row in range(1, grid_size + 1):
        puzzle_gui.add_clue(row, 0, puzzle_clues[2][row - 1], "right")  
        puzzle_gui.add_clue(row, grid_size + 1, puzzle_clues[3][row - 1], "left")  

    
    for row in range(grid_size):
        for col in range(grid_size):
            puzzle_gui.set_number(row, col, grid_data[row][col])

    window.mainloop()
