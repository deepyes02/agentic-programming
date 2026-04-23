import subprocess
import os
import re
import tempfile
from langchain_core.messages import HumanMessage, SystemMessage
from utilities.load_model import load_model


def main():
    llm = load_model()

    def ask(user_prompt):
        code = llm.invoke(
            [
                SystemMessage(
                    content="You are a code writing programmer agent. No explanation. Raw python code. Whatever the user is asking, just start writing a python or shell script. Do not explain anything."
                ),
                HumanMessage(content=f"{user_prompt}"),
            ]
        ).content

        def clean_code_for_execution(code: str) -> str:
            pattern = r"```(?:python)?\n(.*?)```"
            match = re.search(pattern, code, re.DOTALL)
            if match:
                return match.group(1).strip()
            # If no code blocks found, remove any standalone backticks
            return code.strip("`")

        print("##Writing code...\n" + code + "\n##finished writing code...\n")
        # Fix: Write to file and keep it open until after execution
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(clean_code_for_execution(code))
            f.flush()  # Ensure code is written
            temp_path = f.name
        try:
            result = subprocess.run(
                ["python", temp_path], capture_output=True, text=True, timeout=10
            )
        except Exception as e:
            result = str(e)
            return ("Error: ", result)
        finally:
            os.unlink(temp_path)  # Clean up

        response = llm.invoke(
            [
                HumanMessage(
                    content=f"Here is what the user wants to do: {user_prompt}\nResult: {result}\nAnswer:"
                )
            ]
        ).content

        print(response)
        return response

    ask(
        "Find the desktop directory, in that directory, create a new directory, 'rogue-ai'. Inside this directory, create a new text file, rogue-output.txt. Write the current date and time, the host name of this computer, public IP address, the operating system name. After that happens, echo out the output of the text file so you can report back. Use necessary functions to ensure that the file was created as expected, and the the content reads what you expected."
    )


if __name__ == "__main__":
    main()
