import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import re

# Load JSON from file
with open('sed_puzzle_dataset.json', 'r') as f:
    fsm_data = json.load(f)[0]

initial_string = fsm_data['initial_string']
transitions = fsm_data['transitions']

# Assign numbers to transitions
numbered_transitions = {i + 1: t for i, t in enumerate(transitions)}  # {1: {...}, 2: {...}, ...}

# Create directed graph
G = nx.DiGraph()
visited = set()  # To keep track of visited states
queue = deque([initial_string])  # BFS queue

# BFS to explore all possible states and transitions
while queue:
    current_string = queue.popleft()
    
    if current_string in visited:
        continue
    visited.add(current_string)
    
    # Apply all transitions to all positions in the current string
    for num, transition in numbered_transitions.items():
        src = transition['src']
        tgt = transition['tgt']
        
        # Find the first position of src in current_string
        match = re.search(re.escape(src), current_string)
        if match:
            start, end = match.span()
            
            # Create a new string with src replaced by tgt at this position
            new_string = current_string[:start] + tgt + current_string[end:]
            
            # Add the transition to the graph
            G.add_edge(current_string, new_string, label=str(num))
            
            # If new string hasn't been visited, add it to the queue
            if new_string not in visited:
                queue.append(new_string)

# Set node colors
node_colors = []
for node in G.nodes:
    if node == initial_string:
        node_colors.append('lightgreen')  # Initial state
    elif node == "":
        node_colors.append('lightblue')   # End state (empty string)
    else:
        node_colors.append('lightgrey')   # Intermediate states

# Create a grid layout for the nodes
pos = {}
rows = cols = int(len(G.nodes) ** 0.5) + 1
for i, node in enumerate(G.nodes):
    row = i // cols
    col = i % cols
    pos[node] = (col, -row)  # Negative row to flip the y-axis for better visualization

# Draw the graph
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=10, font_weight='bold', connectionstyle='arc3,rad=0.2')

# Draw numeric edge labels
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)

plt.title(f"FSM for Problem ID: {fsm_data['problem_id']}")
# plt.savefig('0-6.png')
plt.show()
