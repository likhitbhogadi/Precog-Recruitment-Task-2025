import random # For random number generation
import json  # For JSON file handling
import string   # For string manipulation

# Function to generate a random string
def generate_random_string(length=10):  # Default length is 10
    letters = string.ascii_uppercase    # Uppercase letters
    return ''.join(random.choice(letters) for _ in range(length))   # Randomly select letters

# Function to create a solvable puzzle
def create_puzzle(problem_id):  # Problem ID is a unique identifier
    initial_string = generate_random_string(random.randint(5, 15))  # Random length of initial string
    transitions = []    # List of transitions
    
    # Break the initial string into random parts to create transitions
    i = 0   # Index
    while i < len(initial_string):  # Iterate over the initial string
        part_length = random.randint(1, 3)  # Random length of substring
        substring = initial_string[i:i+part_length] # Extract the substring
        transitions.append({"src": substring, "tgt": ""})   # Add the transition
        i += part_length    # Move the index

    # # Adding a decoy transition (to increase difficulty)
    # decoy = generate_random_string(3)   # Random decoy string
    # transitions.append({"src": decoy, "tgt": generate_random_string(2)})    # Add the decoy transition

    puzzle = {  # Puzzle object
        "problem_id": f"{problem_id:03}",   # Unique problem ID
        "initial_string": initial_string,   # Initial string
        "transitions": transitions  # List of transitions
    }
    
    return puzzle   # Return the puzzle

# Function to generate multiple puzzles
def generate_puzzles(num_puzzles=100):  # Default number of puzzles is 100
    dataset = []    # List of puzzles
    for i in range(num_puzzles):    # Iterate over the number of puzzles
        puzzle = create_puzzle(i)   # Create a puzzle
        dataset.append(puzzle)  # Add the puzzle to the list
    
    # Save to JSON file
    with open('sed_puzzle_dataset.json', 'w') as f:   # Open the file
        json.dump(dataset, f, indent=4) # Write the dataset to the file

# Generate the dataset
generate_puzzles(4)   # Generate 100 puzzles

print("Dataset generated and saved to sed_puzzle_dataset.json") # Print message
