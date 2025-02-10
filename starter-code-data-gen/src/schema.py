import pydantic # Import pydantic module
from typing import List # Import List from typing module

class Transition(pydantic.BaseModel):   # Define Transition class
    src: str    # Define src attribute of type str
    tgt: str    # Define tgt attribute of type str

    def __str__(self):  # Define __str__ method
        return f"{self.src} -> {self.tgt}"  # Return the string representation of the object
    
    def __repr__(self): # Define __repr__ method
        return str(self)    # Return the string representation of the object
    
    # Check if transition is non-empty
    @pydantic.model_validator(mode="after")   # Decorator to validate the model after initialization
    def check_transition(self): # Define check_transition method
        if len(self.src) == 0 and len(self.tgt) == 0:   # Check if both src and tgt are empty
            raise ValueError("Transition is empty")   # Raise ValueError if transition is empty
        return self # Return the object
    

class Problem(pydantic.BaseModel):  # Define Problem class
    """
    {
        “problem_id”: “000”,
        "initial_string": "HELLOWORLD",
        "transitions": [
            {
                "src": "HELLO",
                "tgt": ""
            },
            {
                "src": "WORLD",
                "tgt": "”
            }
        ]
    }
    """
    problem_id: str # Define problem_id attribute of type str
    initial_string: str # Define initial_string attribute of type str
    transitions: List[Transition]   # Define transitions attribute of type List[Transition]

    # Check if the list is non-empty
    @pydantic.model_validator(mode="after")  # Decorator to validate the model after initialization
    def check_transitions(self):    # Define check_transitions method
        if not self.transitions:    # Check if transitions list is empty
            raise ValueError("Transitions list is empty")   # Raise ValueError if transitions list is empty
        return self # Return the object
        
    # Check if the initial string is non-empty
    @pydantic.model_validator(mode="after") # Decorator to validate the model after initialization
    def check_initial_string(self): # Define check_initial_string method
        if len(self.initial_string) == 0:   # Check if initial_string is empty
            raise ValueError("Initial string is empty")  # Raise ValueError if initial_string is empty
        return self # Return the object
        
    # Check if there exists a transition with an empty target
    @pydantic.model_validator(mode="after") # Decorator to validate the model after initialization
    def check_empty_target(self):   # Define check_empty_target method
        for transition in self.transitions: # Iterate through the transitions list
            if len(transition.tgt) == 0:    # Check if the target of the transition is empty
                return self # Return the object
        raise ValueError("No transition with empty target found")   # Raise ValueError if no transition with empty target is found

class Solution(pydantic.BaseModel): # Define Solution class
    """
    {
        “problem_id”: “000”,
        “solution”: [0, 1]
    }
    """
    problem_id: str # Define problem_id attribute of type str
    solution: List[int] # Define solution attribute of type List[int]

    # Check if the solution list is non-empty
    @pydantic.model_validator(mode="after") # Decorator to validate the model after initialization
    def check_solution(self):   # Define check_solution method
        if len(self.solution) == 0: # Check if solution list is empty
            raise ValueError("Solution list is empty")  # Raise ValueError if solution list is empty
        return self # Return the object