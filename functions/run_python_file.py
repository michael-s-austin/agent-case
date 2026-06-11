import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to be run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass to the script",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    """
    Runs a file within the working directory
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        try:
            command = ["python", target_file]
            output = ""
            if args is not None:
                command.extend(args)

            completed_process = subprocess.run(
                command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
            )

            if completed_process.returncode != 0:
                output += f"Process exited with code {completed_process.returncode}\n"

            if not completed_process.stdout and not completed_process.stderr:
                return f"No output produced"

            if completed_process.stdout:
                output += f"STDOUT: {completed_process.stdout}"

            if completed_process.stderr:
                output += f"STDERR: {completed_process.stderr}"

            return output

        except Exception as e:
            return f"Error: executing Python file: {e}"

    except Exception as e:
        return f"Error: {e}"
