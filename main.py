import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    funcs = {
            "get_files_info": get_files_info,
            "get_file_content": get_file_content,
            "write_file": write_file,
            "run_python_file": run_python_file,
    }


    res = funcs.get(function_call_part.name, lambda: 'Invalid')("./calculator", **function_call_part.args)


    if res == 'Invalid':
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    reponse={"error": f"Unknown function: {function_call_part.name}"}
                )
            ],
        )

    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": res},
                )
            ],
    )



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
verbose = False

if len(sys.argv) < 2:
    print("Missing prompt")
    exit(1)
elif len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    verbose = True

contents = sys.argv[1]



# system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself. In that case the directory would be '.'",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of the file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read, relative to the working directory.",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Read the contents of the file specified, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write, relative to the working directory. Create if it does not exist, overwrite it otherwise",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file"
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the python script specified, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read, relative to the working directory",
            )
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


MAX_ITERATIONS = 20

messages = [
        types.Content(role="user", parts=[types.Part(text=contents)])
]

for i in range(MAX_ITERATIONS):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )

    for j in range(len(response.candidates)):
        # print(f"Candidate {j}: {response.candidates[j].content}")
        messages.append(response.candidates[j].content)


    """
    print("Parts:", type(messages[0].parts))
    for i in range(len(messages[0].parts)):
          print(messages[0].parts[i])
    """

    if verbose:
        print("User prompt:", messages[0].parts)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


    if response.function_calls is not None:
        for called in response.function_calls:
            # print(f"Calling function: {called.name}({called.args})")
            r = call_function(called, verbose=False)
            # print(f"-> {r.parts[0].function_response.response}")
            messages.append(r)

    else:
        print(response.text)
        break

