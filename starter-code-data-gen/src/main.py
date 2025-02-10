import logging  # Import logging module

from utils import read_problem_folder, read_solution_folder, validate_solutions   # Import read_problem_folder, read_solution_folder, validate_solutions

def main(): # Define main function
    logging.basicConfig(level=logging.INFO, format="%(message)s")   # Configure logging

    # Loading the generated puzzles
    problems = read_problem_folder()
    # Loading the solution to the puzzles
    solutions = read_solution_folder()
    # Validate the solution
    validate_solutions(problems, solutions)

if __name__ == "__main__":
    main()
