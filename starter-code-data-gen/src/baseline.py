import os   # for os.path
import json # for json
import time # for time
from utils import read_problem_folder, write_solution_folder    # from utils import read_problem_folder, write_solution_folder
from schema import Solution # from schema import Solution
import logging  # for logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")   # Configure logging

def bfs(problem, time_limit=5): # Define bfs function
    initial = problem.initial_string    # Get the initial string
    transitions = problem.transitions   # Get the transitions

    queue = [(initial, 0)]  # Initialize the queue with the initial string
    operation = {initial: -1}  # Map current string to the transition index used
    parent = {initial: None}  # Map current string to its parent string
    start_time = time.time()  # Record the start time

    while queue:    # While queue is not empty
        current_string, steps = queue.pop(0)    # Pop the first element from the queue

        if time.time() - start_time > time_limit:   # If time exceeds the time limit
            return None # Return None

        # Check if the target string is empty
        if current_string == "":    # If the target string is empty
            solution = []   # Initialize the solution list
            while current_string is not None:   # While current string is not None
                operation_index = operation[current_string]   # Get the operation index
                if operation_index != -1:   # If operation index is not -1
                    solution.append(operation_index)    # Append the operation index to the solution list
                current_string = parent[current_string]  # Update the current string

            return solution[::-1]  # Reverse to get the correct order

        # Process all transitions
        for i, transition in enumerate(transitions):    # For each transition
            src = transition.src    # Get the source string
            tgt = transition.tgt    # Get the target string

            pos = current_string.find(src) if src else 0    # Find the position of the source string in the current string
            if pos != -1:   # If the position is not -1
                new_string = current_string[:pos] + tgt + current_string[pos + len(src):]   # Replace the source string with the target string

                if new_string not in operation: # If the new string is not in the operation
                    operation[new_string] = i  # Store the transition index
                    parent[new_string] = current_string   # Store the parent string
                    queue.append((new_string, steps + 1))   # Append the new string to the queue

    return None  # No solution found

def main(): # Define main function
    # Load the generated puzzles
    problems = read_problem_folder()    # Read the problem folder

    solutions = {}  # Initialize the solutions dictionary
    for problem in problems.values():   # For each problem
        logging.info("=====================================================")   # Log the separator
        solution = bfs(problem) # Find the solution using bfs
        if solution is not None:    # If solution is found
            solutions[problem.problem_id] = Solution(   # Store the solution
                problem_id = problem.problem_id,    # Get the problem id
                solution = solution   # Get the solution
            )
            logging.info(f"Solution found for puzzle {problem.problem_id}")   # Log the solution found
        else:   # If solution is not found
            logging.info(f"Baseline exceedes time limit for puzzle {problem.problem_id}")   # Log the time limit exceeded

    write_solution_folder(solutions)    # Write the solutions to the solution folder

if __name__ == "__main__":  # If the script is executed
    main()  # Execute the main function
