from typing import TypedDict


# State for jokes
class State(TypedDict):
    joke: str
    topic: str
    feedback: str
    funny_or_not: str
