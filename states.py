#so now we are creating a graph
#and the first thing you create is a state

import os

#1) types DICT(Most Common Approach)

from typing import TypedDict

class State(TypedDict):
    topic : str
    summary : str
    score : str

#2) using pydantic model
# it is good at data validation and type checking at runtime

from pydantic import BaseModel, field_validator

class State(BaseModel):
    topic : str
    summary : str = ""
    score : int

    @field_validator
    def score_positive(cls, v):
        if v < 0:
            raise ValueError("score must be positive")
        
# 3)python dataclasses
#standard python dataclass but it is used rarely

from dataclasses import dataclass, field

@dataclass
class State:
    topic : str = ""
    summary : str = ""
    messages : list = field(default_factory=list)

# 4) messages field is already included with add_messages reducer
# just add your extra fields
from langgraph.graph import MessageState

class State(MessageState):
    user_name: str
    language: str


