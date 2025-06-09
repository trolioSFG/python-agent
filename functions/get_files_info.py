import os

def get_files_info(working_directory, directory=None):
    print(f"Working directory: {working_directory} Directory: {directory}\n")
    dir = os.path.join(working_directory, directory)
    if not os.path.isdir(dir):
        return f'Error: "{directory}" is not a directory'
    
    wd = os.path.abspath(working_directory)
    dir = os.path.abspath(dir)

    common = os.path.commonpath([wd, dir])
    if not common.startswith(wd):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    result = ""
    print(f"listdir({dir}):\n\n")

    """
    for f in os.listdir(dir):
        result += f"- {f}: file_size={os.stat(f).st_size} bytes, is_dir={os.path.isdir(f)}\n"
    
    """

    with os.scandir(dir) as d:
        for entry in d:
            result += f"- {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}\n"


    return result
