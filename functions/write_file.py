import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path and name being written to"),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written"),
            },
        ),
    )

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:      
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file):
            return f'Error: "Cannot write to "{file_path}" as it is a directory' 
                     
        else:
            try:
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                with open(target_file, mode='w') as f:
                    f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

            except Exception as e:
                return f"Error: {e}"
  
    except Exception as e:
        return f"Error: {e}"