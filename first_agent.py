from asyncio import subprocess
import tempfile
import os
import re
from langgraph.graph import add_messages
from typing import TypedDict, List, Annotated

# from langchain.tools import tool
# from langgraph.prebuilt import ToolNode
from utilities.load_model import load_model


class FileManagerState(TypedDict):
    user_request: str
    # working state
    current_dir: str
    target_path: str
    operation_result: str
    attempts: int
    # code
    generated_code: str
    execution_output: str
    # tracking
    task_complete: bool
    verification_result: str
    messages: Annotated[List, add_messages]


llm = load_model()


### Tool for executing the python code ###
def execute_python_code(code: str) -> tuple[str, str]:
    """Execute the python code and return the output and error.
    Args:
        code (str): The python code to execute.
    Returns:
        tuple[str, str]: The output and error of the python code.
    """
    pattern = r"```(?:python)?\n(.*?)```"
    match = re.search(pattern, code, re.DOTALL)
    if match:
        code = match.group(1).strip()
    else:
        code = code.strip("`")
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()
            temp_path = f.name
            result = subprocess.run(
                "python", temp_path, capture_output=True, text=True, timeout=10
            )
            return result.stdout, result.stderr
    finally:
        os.unlink(temp_path)


### NODES ###


def code_generator_node(state: FileManagerState) -> FileManagerState:
    """Generate python code for the user request."""
