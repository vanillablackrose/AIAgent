import os
import subprocess
from .get_files_info import in_directory
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python script file located in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to execute, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    try:
        full_dir = os.path.join(working_directory, file_path)
        if not in_directory(full_dir, working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.exists(file_path):
           return f'Error: File "{file_path}" not found.'

        if file_path[-3:] != ".py":
           return f'Error: "{file_path}" is not a Python file.' 

    except Exception as e:
        print("Error: error checking valid filepaths ")

    try:
        # run the file
        completed_process = subprocess.run(["python3", file_path], timeout=30, capture_output=True, cwd=working_directory)

        std_out = completed_process.stdout.decode("utf-8")
        std_err = completed_process.stderr.decode("utf-8")
        rtn_code = completed_process.returncode

        if rtn_code != 0:
            return f"Process exited with code {rtn_code}"
        
        if std_out == None: 
            return "No output produced"
        
        output = f"STDOUT: {std_out}\n"

        if std_err != None and std_err != "":
            output += f"STDERR: {std_err}"
        
        return output
            

    except Exception as e:
        print(f"Error: executing Python file: {e}")