import os

def get_file_content(working_directory, file_path):
    wd = os.path.abspath(working_directory)
    fp = os.path.abspath(os.path.join(wd, file_path))
    common = os.path.commonpath([wd, fp])

    if not fp.startswith(wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(fp):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(fp, "r") as f:
        contents = f.read()

    
    if len(contents) > 10000:
        contents = contents[:10000]
        contents += f'\n[...File "{file_path}" truncated at 10000 characters]'

    return contents

