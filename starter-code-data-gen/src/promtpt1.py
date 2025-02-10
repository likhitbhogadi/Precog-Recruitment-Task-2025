import os
import json
import google.generativeai as genai

# Configure the API key
genai.configure(api_key='AIzaSyA-N32yR44YV5Fj1rezq7dZVJqXCxDy6Is')

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Function to load problems from a JSON file
def load_problems(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Main function to process problems
def process_problems(problems):
    chat_session = model.start_chat(history=[])

    for problem in problems:
        initial_string = problem["initial_string"]
        transitions = problem["transitions"]
        
        # Prepare the message for the chat session
        message = f"""
        Given a string and a list of transitions, find a sequence of transition indices that, when applied in order, reduces the string to empty.

        Rules:
        1. Start with the given string.
        2. Each transition replaces the first occurrence of src with tgt.
        3. Return any valid sequence of transition indices that results in an empty string.

        Problem ID: {problem["problem_id"]}
        Initial String: {initial_string}
        Transitions: {transitions}
        Format: [index1, index2, ...] (only numbers, no extra text or code)
        """
        # Send the message and get the response
        response = chat_session.send_message(message)
        # Assuming response has a method to get the content as a dictionary
        response_dict = response.to_dict()  # or response.content if it's an attribute
       
        # # Extract the text part
        # text_part = response_dict["candidates"][0]["content"]["parts"][0]["text"]
        # print(f"Response for Problem ID {problem['problem_id']}: {text_part}")
        # # print(text_part)

        # Extract the text part
        text_part = response_dict["candidates"][0]["content"]["parts"][0]["text"]
        # solution = json.loads(text_part.strip())

        try:
            solution = json.loads(text_part.strip())
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON for Problem ID {problem['problem_id']}, text_part: {text_part.strip()}: {e}")
            continue

        # Create the solution dictionary
        solution_dict = {
            "problem_id": problem["problem_id"],
            "solution": solution
        }

        # Write the solution to a JSON file in the solutions folder
        solution_filename = f"../sample-data/solutions/{problem['problem_id']}.json"
        with open(solution_filename, 'w') as solution_file:
            json.dump(solution_dict, solution_file, indent=4)

        print(f"Solution for Problem ID {problem['problem_id']} written to {solution_filename}")

# Load problems from the JSON file
problems = load_problems('../sample-data/puzzles/problems.json')
print(problems)

# Process the loaded problems
process_problems(problems)

