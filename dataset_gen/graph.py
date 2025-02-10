import json
import graphviz

def apply_transition(current_string, transition):   
    src = transition["src"]
    tgt = transition["tgt"]
    pos = current_string.find(src)
    if pos != -1:
        return current_string[:pos] + tgt + current_string[pos + len(src):]
    return current_string

def generate_state_diagram_from_json(json_filepath, output_filepath_prefix):
    with open(json_filepath, 'r') as f:
        problems = json.load(f)

    for problem in problems:    # Iterate over each problem
        problem_id = problem["problem_id"]  # Get the problem ID
        initial_string = problem["initial_string"]  # Get the initial string
        transitions = problem["transitions"]        # Get the transitions

        dot = graphviz.Digraph(comment=f'Finite Automaton {problem_id}')    # Create a new graph

        dot.node(initial_string, initial_string, shape='circle')    # Add the initial state to the graph
        queue = [initial_string]    # Initialize a queue with the initial state
        visited = set([initial_string])   # Initialize a set with the initial state

        while queue:    # While the queue is not empty
            current_string = queue.pop(0)   # Pop the first element from the queue

            for transition in transitions:  # Iterate over each transition
                new_string = apply_transition(current_string, transition)   # Apply the transition to the current state
                # if new_string != current_string:    # If the new state is different from the current state
                if new_string not in visited:   # If the new state has not been visited before
                    dot.node(new_string, new_string, shape='circle')    # Add the new state to the graph
                    queue.append(new_string)    # Add the new state to the queue
                    visited.add(new_string)    # Add the new state to the visited set
                dot.edge(current_string, new_string, label=f'{transition["src"]}->{transition["tgt"]}')   # Add an edge between the current state and the new state
                # add the visited node to the visited set

        dot.render(f'{output_filepath_prefix}_{problem_id}', format='png', cleanup=True)    # Render the graph to a PNG file

# Example usage
generate_state_diagram_from_json(
    '/home/likhitbhogadi/all projects/Precog-Recruitment-Task-2025/ai_help/sed_puzzle_dataset.json',
    'finite_automaton_from_json'
)
