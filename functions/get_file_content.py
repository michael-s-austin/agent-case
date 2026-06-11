import os

from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file within the working directory, up to a defined number of characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path and name of a file to be read",
            ),
        },
    ),
)


def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Reads the content of a file within the working directory, up to a defined number of characters
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        else:
            try:
                with open(target_file, mode="r") as f:
                    file_content = f.read(MAX_CHARS)
                    if f.read(1):
                        file_content += (
                            f'[...File "{file_path}" truncated at 10,000 characters]'
                        )
                return file_content

            except Exception as e:
                return f"Error: {e}"

    except Exception as e:
        return f"Error: {e}"
