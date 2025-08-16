from typing import Callable, Mapping

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage


def get_nodes(
    llm: BaseChatModel, evaluator: BaseChatModel
) -> list[Callable[[Mapping[str, object]], Mapping[str, object]]]:
    def llm_call_generator(state: Mapping[str, object]) -> Mapping[str, object]:
        """LLM generates a joke"""

        messages = [
            SystemMessage(
                content="You are a helpful AI that shares everything you know. Talk in English."
            )
        ]

        if state.get("feedback"):
            messages.append(
                HumanMessage(
                    content=f"Write a joke about {state['topic']} but take into account the feedback: {state['feedback']}"
                )
            )

            msg = llm.invoke(messages)
        else:
            messages.append(
                HumanMessage(content=f"Write a joke about {state['topic']}")
            )

            msg = llm.invoke(messages)
        return {"joke": msg.content}

    def llm_call_evaluator(state: Mapping[str, object]) -> Mapping[str, object]:
        """LLM evaluates the joke"""
        messages = [
            SystemMessage(
                content="You are a helpful AI that shares everything you know. Talk in English."
            ),
            HumanMessage(content=f"Grade the joke {state['joke']}"),
        ]

        grade = evaluator.invoke(messages)
        return {"funny_or_not": grade.grade, "feedback": grade.feedback}

    return [llm_call_generator, llm_call_evaluator]


def get_edges() -> list[str]:
    # Conditional edge function to route back to joke generator or end based upon feedback from the evaluator
    def route_joke(state: Mapping[str, object]) -> str:
        """Route back to joke generator or end based upon feedback from the evaluator"""

        if state["funny_or_not"] == "funny":
            return "Accepted"
        elif state["funny_or_not"] == "not funny":
            return "Rejected + Feedback"

    return [route_joke]
