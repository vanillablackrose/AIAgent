import os
from .get_files_info import in_directory
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the contents of a file, capped at 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        full_dir = os.path.join(working_directory, file_path)
        if not in_directory(full_dir, working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    
        if not os.path.isfile(full_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        print("Error: error checking valid filepaths ")
    
    try:
        MAX_CHARS = 10000

        with open(full_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        # 1 byte is ~ 1 character so if a file is > 10000 bytes, 
        # we truncated the read
        file_size = os.path.getsize(full_dir)

        if file_size > 10000:
            file_content_string += f'\n[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string
    except Exception as e:
        print("Error: error reading file contents")
