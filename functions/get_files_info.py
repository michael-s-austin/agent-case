import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["directory"],
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory' 

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
                
        else:
            file_list = os.listdir(target_dir)   
            parsed_list = []
            for file in file_list:
                file_name_path = os.path.join(target_dir, file)
                file_detail = f"- {file}: file_size={os.path.getsize(file_name_path)}, is_dir={os.path.isdir(file_name_path)}"
                parsed_list.append(file_detail)
            return '\n'.join(parsed_list)

    except Exception as e:
        return f"Error: {e}"


    
  


    
    
    
  