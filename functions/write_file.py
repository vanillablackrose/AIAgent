import os
from .get_files_info import in_directory
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, creating it if necessary.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string content to write to the file."
            )
        }
    )
)

def write_file(working_directory, file_path, content):
    try:
        full_dir = os.path.join(working_directory, file_path)
        if not in_directory(full_dir, working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    except Exception as e:
        print("Error: error checking valid filepaths ")

    try:
        #overwrite the file!
        if not os.path.exists(file_path):
            #create the directory
            dir_names = os.path.dirname(file_path)
            if dir_names != "":
                os.makedirs(dir_names)
            with open(file_path, "x") as f:
                f.write(content)        
        else:
            with open(file_path, "w") as f:
                f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print("Error: error overwriting the file")