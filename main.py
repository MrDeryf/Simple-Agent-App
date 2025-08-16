from app.Workflows.joke_workflow import get_workflow
from app.Models.gigachat_model import get_model
from app.Nodes.joke_nodes import get_edges, get_nodes
from app.States.joke_state import State
from app.api.simple_api import agent_app


llm = get_model()
optimizer_builder = get_workflow(llm, get_nodes, get_edges, State)
optimizer_workflow = optimizer_builder.compile()

# Show the workflow
# print(optimizer_workflow.get_graph().draw_mermaid())

# Invoke
""" state = optimizer_workflow.invoke({"topic": "Cats"})
print(state["joke"])
print(state["feedback"]) """


@agent_app.post("/generate_joke")
def generate(topic: str):
    response = optimizer_workflow.invoke({"topic": topic})
    return {"response": response["joke"]}



