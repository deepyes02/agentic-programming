from typing import TypedDict, List
from langchain.tools import tool


class FileManagerState(TypedDict):
    dir_path: str
    file_name: str
    os: str
    task_complete: bool
    messages: List[str]


@tool
def manage_files_and_directories():
    

