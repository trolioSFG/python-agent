import os
import subprocess


def run_python_file(working_directory, file_path):
    wd = os.path.abspath(working_directory)
    fp = os.path.abspath(os.path.join(wd, file_path))
    common = os.path.commonpath([wd, fp])

    if not common.startswith(wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(fp):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'


    try:
        proc = subprocess.run(["python3", fp], timeout = 30, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
    except subprocess.TimeoutExpired:
        print("Timeout!")
    except subprocess.CalledProcessError as e:
        return f'Error: executing Python file: {e}'
        print(e.output)

    if len(proc.stdout) == 0:
        print("No output produced.")
    else:
        print(f"STDOUT:{proc.stdout}")

    print(f"STDERR:{proc.stderr}")

    if proc.returncode != 0:
        print(f"Process exited with code {proc.returncode}")

