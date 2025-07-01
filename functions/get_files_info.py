import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    try:
        if directory == None:
            directory = "."
            
        full_dir = os.path.join(working_directory, directory)

        bInDirectory = in_directory(full_dir, working_directory)

        if directory == ".":
            # set the full dir to the working dir for the special case
            full_dir = working_directory
            str_header = "Result for current directory:\n\n"
        else:
            str_header = f"Result for '{directory}' directory:\n\n"
        
        if not bInDirectory:
            return f'{str_header}Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_dir):
            return f'{str_header}Error: "{directory}" is not a directory'  
        
        
        return f"{str_header}{print_dir_contents(full_dir)}"
    except Exception as e:
        print("Error: error combining directory paths")

def in_directory(file_path, working_directory):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(file_path) 
        if abs_file_path.startswith(abs_working_dir):  
            return True
        return False
    except Exception as e:
        print("Error: error encountered checking directory structure")

def print_dir_contents(directory):
    try:
        dir_contents = os.listdir(path=directory)

        str_contents = list()

        for curr_dir in dir_contents:
            sub_path = os.path.join(directory, curr_dir)
            str_contents.append(print_file_data(curr_dir, sub_path))

        return "\n\n".join(str_contents)
    except Exception as e:
        print("Error: error listing directory contents")

def print_file_data(file_name, file_path):
    try:
        file_size = os.path.getsize(file_path)
        is_dir = os.path.isfile(file_path)

        return f"- {file_name} file-size={file_size}, is_dir={is_dir}"
    except Exception as e:
        print("Error: error processing file attributes")