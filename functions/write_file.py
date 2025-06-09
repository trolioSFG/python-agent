import os

def write_file(working_directory, file_path, content):
    wd = os.path.abspath(working_directory)
    fp = os.path.join(wd, file_path)
    common = os.path.commonpath([wd, fp])
    if not common.startswith(wd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'


    with open(fp, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)}) characters written)'

