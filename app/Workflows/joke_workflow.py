from typing import Callable, Mapping

from langchain_core.language_models import BaseChatModel
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing_extensions import Literal


def get_workflow(
    llm: BaseChatModel,
    get_nodes,
    get_edges: Callable[[None], list[str]],
    State: Mapping[str, object],
) -> StateGraph:
    # Schema for structured output to use in evaluation
    class Feedback(BaseModel):
        """Gives a rating and feedback"""

        grade: Literal["funny", "not funny"] = Field(
            description="Decide if the joke is funny or not."
        )
        feedback: str = Field(
            description="If the joke is not funny, provide feedback on how to improve it."
        )

    evaluator = llm.with_structured_output(Feedback)

    # Build workflow
    optimizer_builder = StateGraph(State)

    llm_call_generator, llm_call_evaluator = get_nodes(llm, evaluator)

    route_joke = get_edges()[0]

    # Add the nodes
    optimizer_builder.add_node("llm_call_generator", llm_call_generator)
    optimizer_builder.add_node("llm_call_evaluator", llm_call_evaluator)

    # Add edges to connect nodes
    optimizer_builder.add_edge(START, "llm_call_generator")
    optimizer_builder.add_edge("llm_call_generator", "llm_call_evaluator")
    optimizer_builder.add_conditional_edges(
        "llm_call_evaluator",
        route_joke,
        {  # Name returned by route_joke : Name of next node to visit
            "Accepted": END,
            "Rejected + Feedback": "llm_call_generator",
        },
    )

    return optimizer_builder
