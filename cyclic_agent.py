from typing import TypedDict, List
import os
from langgraph.graph import StateGraph, END


### STATE
class FileWriterState(TypedDict):
    file_path: str
    lines_written: int
    task_complete: bool
    messages: List[str]


def create_file_node(state: FileWriterState) -> FileWriterState:
    print("\n## Starting create node")
    file_path = state["file_path"]
    messages = state.get("messages", []).copy()

    if not os.path.exists(file_path):
        with open(file_path, "w"):
            pass
        os.chmod(file_path, 0o644)
        messages.append(f"Created file: {file_path}")
    else:
        messages.append(f"File already exists: {file_path}")

    # Return updated state (don't mutate original)
    return {**state, "messages": messages}


def write_line_node(state: FileWriterState) -> FileWriterState:
    print("\n## Starting write node")
    file_path = state["file_path"]
    messages = state["messages"].copy()
    lines_written = state["lines_written"]

    try:
        with open(file_path, "a") as f:
            f.write("Hello world\n")
        lines_written += 1
        messages.append(f"Wrote line {lines_written}")
    except Exception as e:
        messages.append(f"Error writing to file: {e}")

    # Return updated state
    return {**state, "lines_written": lines_written, "messages": messages}


def check_lines_node(state: FileWriterState) -> FileWriterState:
    print("\n## Starting check node")
    print(f"   Current lines: {state['lines_written']}")

    # Set task_complete if we've written 5 lines
    task_complete = state["lines_written"] == 5

    # Return updated state
    return {**state, "task_complete": task_complete}


def confirm_node(state: FileWriterState) -> FileWriterState:
    print("\n## Starting confirm node")
    messages = state["messages"].copy()

    if state["task_complete"]:
        messages.append("✅ Task complete! Successfully wrote 5 lines.")
    else:
        messages.append(
            f"❌ Task incomplete. Only wrote {state['lines_written']} lines."
        )

    return {**state, "messages": messages}


# ========== ROUTING FUNCTION ==========
def router_after_check(state: FileWriterState) -> str:
    """Determine next step after checking"""
    if state["task_complete"]:
        return "complete"
    return "continue"


def build_a_graph():
    print("\n## Building a graph")
    workflow = StateGraph(FileWriterState)

    # Add nodes
    workflow.add_node("create", create_file_node)
    workflow.add_node("write", write_line_node)
    workflow.add_node("check", check_lines_node)
    workflow.add_node("confirm", confirm_node)

    # Set entry point
    workflow.set_entry_point("create")

    # Define edges
    workflow.add_edge("create", "write")  # create → write
    workflow.add_edge("write", "check")  # write → check (THIS WAS MISSING!)

    # Conditional edge from check
    workflow.add_conditional_edges(
        "check",  # From check node
        router_after_check,  # Router function (returns string)
        {
            "continue": "write",  # If not complete, go back to write
            "complete": "confirm",  # If complete, go to confirm
        },
    )

    workflow.add_edge("confirm", END)

    return workflow.compile()


# Run the agent
initialize_state = {
    "file_path": "test.txt",
    "lines_written": 0,
    "task_complete": False,
    "messages": [],
}

app = build_a_graph()

print("\n🚀 Starting agent...")
print("=" * 50)

final_state = app.invoke(initialize_state)

print("\n" + "=" * 50)
print("FINAL STATE:")
print(f"File: {final_state['file_path']}")
print(f"Lines written: {final_state['lines_written']}")
print(f"Task complete: {final_state['task_complete']}")
print("\nMessage History:")
for i, msg in enumerate(final_state["messages"], 1):
    print(f"  {i}. {msg}")

# Verify file content
print("\n📄 Actual file content:")
with open("test.txt", "r") as f:
    content = f.read()
    print(content, end="")
