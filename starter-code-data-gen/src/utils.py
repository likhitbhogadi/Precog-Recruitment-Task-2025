import os # for os.path
from pathlib import Path    # for Path
import schema   # for schema.Problem and schema.Solution
import json # for json
import logging  # for logging

import pydantic # for pydantic

# def read_problem_folder(path=Path("../sample-data/puzzles")):   # Define read_problem_folder function
#     """Opens all problems at the folder and reads them using Pydantic"""
#     problems = {}   # Define problems as empty dictionary
#     for file_path in path.iterdir():    # For each file in the path
#         problem_data = json.loads(file_path.read_text())    # Load the file as json
#         try:    # Try to
#             problem = schema.Problem(**problem_data)    # Load the json as schema.Problem
#             problems[problem.problem_id] = problem  # Add the problem to the problems dictionary
#         except pydantic.ValidationError as e:   # If there is a validation error
#             logging.warning(f"Validation error while processing {file_path}! skipping...", exc_info=True)   # Log the error
#     return problems # Return the problems dictionary

def read_problem_folder(path=Path("../sample-data/puzzles/problems.json")):   # Define read_problem_folder function
    """Opens all problems at the folder and reads them using Pydantic"""
    with open(path, 'r') as f:
        problems = {}

        array_problems = json.load(f)
        for problem_data in array_problems:
            try:
                # print(problem_data)
                # problem = schema.Problem(**problem_data)
                problems[problem_data['problem_id']] = problem_data
            except pydantic.ValidationError as e:
                logging.warning(f"Validation error while processing {problem_data}! skipping...", exc_info=True)
    return problems

def read_solution_folder(path=Path("../sample-data/solutions")):    # Define read_solution_folder function
    """Opens all solutions at the folder and reads them using Pydantic"""
    solutions = {}  # Define solutions as empty dictionary
    for file_path in path.iterdir():    # For each file in the path
        solution_data = json.loads(file_path.read_text())   # Load the file as json
        try:    # Try to
            solution = schema.Solution(**solution_data) # Load the json as schema.Solution
            solutions[solution.problem_id] = solution   # Add the solution to the solutions dictionary
        except pydantic.ValidationError as e:   # If there is a validation error
            logging.warning(f"Validation error while processing {file_path}! skipping... ", exc_info=True)  # Log the error
    return solutions    # Return the solutions dictionary

def write_problem_folder(problems, path=Path("../sample-data/puzzles")):    # Define write_problem_folder function
    path.mkdir(exist_ok=True)   # Create the path if it does not exist

    for problem_id, problem in problems.items():    # For each problem in the problems dictionary
        logging.info(f"Saving problem {problem_id}...")   # Log the saving of the problem
        with open(path / f"{problem_id}.json", 'w') as f:    # Open the file
            f.write(problem.json()) # Write the problem as json

def write_solution_folder(solutions, path=Path("../sample-data/solutions")):    # Define write_solution_folder function
    path.mkdir(exist_ok=True)   # Create the path if it does not exist

    for problem_id, solution in solutions.items():  # For each solution in the solutions dictionary
        logging.info("=====================================================")   # Log the saving of the solution
        logging.info(f"Saving solution to problem {problem_id}...")   # Log the saving of the solution
        with open(path / f"{problem_id}.json", 'w') as f:   # Open the file
            f.write(solution.json())    # Write the solution as json

def validate_solutions(problems, solutions):    # Define validate_solutions function
    """
    Validates solutions by checking if they result in an empty string at the end of their transitions.
    """
    count=0
    for problem_id in problems: # For each problem in the problems dictionary
        logging.info("=====================================================")   # Log the validation of the solution
        if problem_id not in solutions: # If the problem is not in the solutions dictionary
            logging.warning(f"Problem {problem_id} does not have a solution, skipping...")  # Log the error
            continue    # Skip the problem

        problem = problems[problem_id]  # Get the problem
        solution = solutions[problem_id]    # Get the solution

        transitions = problem['transitions']   # Get the transitions
        current = problem['initial_string']    # Get the initial string

        for step in solution.solution:  # For each step in the solution
            if step >= len(transitions):    # If the step is greater than the length of the transitions
                logging.warning(f"Invalid step number {step} found! skipping problem...")   # Log the error
                break   # Break the loop
            from_pattern = transitions[step]['src']    # Get the source pattern
            to_pattern = transitions[step]['tgt']  # Get the target pattern
            current = current.replace(from_pattern, to_pattern, 1)  # Replace the source pattern with the target pattern
            logging.info(f"Pattern: {from_pattern} -> {to_pattern}, String: {current}")   # Log the pattern and string
        

        if current != '':   # If the current string is not empty
            logging.warning(f"Problem {problem_id} has an invalid solution!")   # Log the error
        else:   # If the current string is empty
            logging.info(f"Problem {problem_id} has a valid solution!") # Log the solution
            count+=1

    logging.info(f"Total number of valid solutions: {count}")    # Log the total number of valid
    logging.info(f"Total number of invalid solutions: {len(problems)-count}")    # Log the total number of invalid