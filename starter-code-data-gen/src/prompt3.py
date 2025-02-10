import os
import json
import google.generativeai as genai

# Configure the API key
# genai.configure(api_key='AIzaSyCSG8x8XEEu23_0n_u1970Xt-LI66UbaoQ')
# genai.configure(api_key='AIzaSyA-N32yR44YV5Fj1rezq7dZVJqXCxDy6Is')
genai.configure(api_key='AIzaSyAcRplauQsKtpaCPlnMAW-KoEHJC9_pGLA')

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
        # Few-Shot Prompt:
        message = f"""
        I will guide you through solving a `sed`-style text manipulation problem. Follow these steps carefully:

        Example 1:
        Initial String: "CBAAD", Transitions: [CB→A, AA→C, CAD→""]
        Steps:
        1. Apply the first transition (replace "CB" with "A"): "CBAAD" → "AAAD"
        2. Apply the second transition (replace "AA" with "C"): "AAAD" → "CAD"
        3. Apply the third transition (replace "CAD" with ""): "CAD" → ""

        Solution: [0, 1, 2]

        Example 2:
        Initial String: "ABAB", Transitions: [AB→"", BA→X]
        Steps:
        1. Apply the first transition (replace "AB" with ""): "ABAB" → "AB"
        2. Apply the first transition again (replace "AB" with ""): "AB" → ""

        Solution: [0, 0]

        Now solve:

        Problem ID: {problem["problem_id"]}
        Initial String: {initial_string}
        Transitions: {transitions}

        Format your solution as a list of indices corresponding to the transitions applied in the correct order, without any extra text. Example: [0, 1, 2]

        Make sure you choose transitions carefully and apply them in the right order to reach the empty string. If the problem involves repeating transitions, apply them in the correct sequence.

        Solution:
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

