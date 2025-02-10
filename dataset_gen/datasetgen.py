import random
import json
import graphviz
from graph_generator import generate_fsm_graph

# Class to represent a finite automaton
class FiniteAutomaton:
    def __init__(self, initial_string, transitions):
        self.initial_string = initial_string
        self.transitions = transitions
        self.states = {initial_string}
        self.final_state = ""

    def add_transition(self, src, tgt):
        self.transitions.append({"src": src, "tgt": tgt})

    def apply_transition(self, current_string, transition):
        src = transition["src"]
        tgt = transition["tgt"]
        pos = current_string.find(src)
        if pos != -1:
            return current_string[:pos] + tgt + current_string[pos + len(src):]
        return current_string

    def is_reachable(self):
        queue = [self.initial_string]
        visited = set()

        while queue:
            current_string = queue.pop(0)
            if current_string == self.final_state:
                return True
            if current_string in visited:
                continue
            visited.add(current_string)

            for transition in self.transitions:
                new_string = self.apply_transition(current_string, transition)
                if new_string not in visited:
                    queue.append(new_string)

        return False

# Function to generate random strings
def random_string(length=3):    # Default length is 5
    return ''.join(random.choices('AB', k=length))  # Randomly select letters
    
# Function to generate transitions
def generate_transitions(start_string, num_transitions=4):  # Default number of transitions is 5
    
    # Initialize variables
    transitions = []                # List of transitions
    # src_states = []                 # List of source states
    current_string = start_string   # Current string is the start string
    states = [current_string]       # List of states
    var1=3                          # Number of transitions to be reused
    transition_srcs = []            # List of source substrings
    no_of_reuses = 0

    # print("current_string: ", current_string)

    # Generate transitions
    for _ in range(num_transitions - 1):    # Iterate over the number of transitions
        # print("current_string: ", current_string)
        if len(current_string) < 2:         # If the current string is less than 2, break
            break
        count = 0
        # fl=1
        # print("len(src_states): ",  len(src_states))
        for i in range(len(transition_srcs)):                           # Iterate over the transitions 
            if(count==var1):
                break
            # print(i)
            transition_src = transition_srcs[i]                         # Get the source state
            transition = transitions[i]                                 # Get the transition
            if(transition_src in current_string):                       # If the source state is in the current string
                # print("resusing a transition")
                no_of_reuses = no_of_reuses + 1
                # print("transition_src: ", transition_src)
                # print("current_string: ", current_string)
                # print("curr "+ current_string)
                substring_to_replace = transition["src"]                # Get the source substring
                # print("src " + substring_to_replace)
                new_substring = transition["tgt"]                       # Get the target substring
                # print("tgt " + new_substring)
                current_string = current_string.replace(substring_to_replace, new_substring, 1)
                # print("current_string: ", current_string)
                # fl=0
                count = count + 1
                # break
        # if(fl==1):
        if(len(current_string) >= 2):
            substring_length = random.randint(2, min(3, len(current_string)))                   # Random length of substring (2 to 3)
            start_index = random.randint(0, len(current_string) - substring_length)             # Random start index
            substring_to_replace = current_string[start_index:start_index + substring_length]   # Substring to replace
            new_substring = random_string(random.randint(1, 2))                                 # Random new substring
            if((substring_to_replace != new_substring) and (substring_to_replace not in transition_srcs)):  # If the substrings are different and not already used
                transitions.append({"src": substring_to_replace, "tgt": new_substring})
                # src_states.append(current_string)
                current_string = current_string.replace(substring_to_replace, new_substring, 1)
                # print("current_string: ", current_string)
                states.append(current_string)
                transition_srcs.append(substring_to_replace)
                # print(current_string)

        # if ( (random.random() > 0.1) and ( _==0)):  # Randomly decide to add a transition but not change the current string
        #     # print("here")
        #     continue
    # print(count)

    # Add cross transitions
    # for i in range(len(states)):
    #     if(i % 2 == 0):
    #         src_state = states[i]
    #         tgt_state = random_string(random.randint(1, 3)) 
    #         if src_state != tgt_state:
    #             transitions.append({"src": src_state, "tgt": tgt_state})

    # Final transition to empty string
    if (current_string and (current_string not in transition_srcs)):
        transitions.append({"src": current_string, "tgt": ""})
        # src_states.append(current_string)
        transition_srcs.append(current_string)

    # print(src_states)
    # print(transition_srcs)
    # print(transitions)
    print("no_of_reuses: ", no_of_reuses)
    return transitions

# Main generator function
def generate_problem(problem_id):
    while True:
        start_string = random_string(6)
        transitions = generate_transitions(start_string)
        fa = FiniteAutomaton(start_string, transitions)

        # Ensure the final state is empty and reachable
        if fa.is_reachable():
            return {
                "problem_id": problem_id,
                "initial_string": start_string,
                "transitions": transitions
            }

# Function to generate multiple problems and save to a JSON file
def generate_problems(num_problems, filename):
    problems = []
    for i in range(num_problems):
        problem_id = f"{i:03d}"
        problem = generate_problem(problem_id)
        problems.append(problem)

    with open(filename, 'w') as f:
        json.dump(problems, f, indent=4)

    # Generate state diagram
    # generate_state_diagram(problems)

# Function to generate state diagram using graphviz
def generate_state_diagram(problems):
    dot = graphviz.Digraph(comment='Finite Automaton')

    for problem in problems:
        initial_string = problem["initial_string"]
        transitions = problem["transitions"]

        dot.node(initial_string, initial_string, shape='circle')
        current_string = initial_string

        for transition in transitions:
            src = transition["src"]
            tgt = transition["tgt"]
            new_string = current_string.replace(src, tgt, 1)
            dot.node(new_string, new_string, shape='circle')
            dot.edge(current_string, new_string, label=f'{src}->{tgt}')
            current_string = new_string

    dot.render('finite_automaton', format='png', cleanup=True)

# Example usage
generate_problems(100, '../starter-code-data-gen/sample-data/puzzles/problems.json')

# Load JSON from file and generate graphs
with open('fsm_data.json', 'r') as f:
    fsm_data_list = json.load(f)

# for fsm_data in fsm_data_list:
#     generate_fsm_graph(fsm_data)
