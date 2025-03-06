import os
from dataclasses import dataclass
from typing import Any

from ..types_ import (
    BashCommand,
    ContextSave,
    FileEdit,
    FileWriting,
    Initialize,
    ReadFiles,
    ReadImage,
    WriteIfEmpty,
)

with open(os.path.join(os.path.dirname(__file__), "diff-instructions.txt")) as f:
    diffinstructions = f.read()


@dataclass
class Prompts:
    inputSchema: dict[str, Any]
    name: str
    description: str


TOOL_PROMPTS = [
    Prompts(
        inputSchema=Initialize.model_json_schema(),
        name="Initialize",
        description="""
- Always call this at the start of the conversation before using any of the shell tools from wcgw.
- Use `any_workspace_path` to initialize the shell in the appropriate project directory.
- If the user has mentioned a workspace or project root or any other file or folder use it to set `any_workspace_path`.
- If user has mentioned any files use `initial_files_to_read` to read, use absolute paths only (~ allowed)
- By default use mode "wcgw"
- In "code-writer" mode, set the commands and globs which user asked to set, otherwise use 'all'.
- Use type="first_call" if it's the first call to this tool.
- Use type="user_asked_mode_change" if in a conversation user has asked to change mode.
- Use type="reset_shell" if in a conversation shell is not working after multiple tries.
- Use type="user_asked_change_workspace" if in a conversation user asked to change workspace
""",
    ),
    Prompts(
        inputSchema=BashCommand.model_json_schema(),
        name="BashCommand",
        description="""
- Execute a bash command. This is stateful (beware with subsequent calls).
- Status of the command and the current working directory will always be returned at the end.
- The first or the last line might be `(...truncated)` if the output is too long.
- Always run `pwd` if you get any file or directory not found error to make sure you're not lost.
- Run long running commands in background using screen instead of "&".
- Do not use 'cat' to read files, use ReadFiles tool instead
- In order to check status of previous command, use `status_check` with empty command argument.
- Only command is allowed to run at a time. You need to wait for any previous command to finish before running a new one.
- Programs don't hang easily, so most likely explanation for no output is usually that the program is still running, and you need to check status again.
- Do not send Ctrl-c before checking for status till 10 minutes or whatever is appropriate for the program to finish.
""",
    ),
    Prompts(
        inputSchema=ReadFiles.model_json_schema(),
        name="ReadFiles",
        description="""
- Read full file content of one or more files.
- Provide absolute paths only (~ allowed)
""",
    ),
    Prompts(
        inputSchema=ReadImage.model_json_schema(),
        name="ReadImage",
        description="Read an image from the shell.",
    ),
    Prompts(
        inputSchema=FileWriting.model_json_schema(),
        name="FileWriting",
        description="""
- Writes or edits a file based on the percentage of changes.
- Use absolute path only (~ allowed).
- First write down percentage of lines to be changed in the file (100 if it doesn't exist, or 0-100) in percentage_to_change
- If percentage_to_change > 50, provide full file content in file_content_or_search_replace_blocks
- If percentage_to_change <= 50, file_content_or_search_replace_blocks should be search/replace blocks.

"""
        + diffinstructions,
    ),
    Prompts(
        inputSchema=ContextSave.model_json_schema(),
        name="ContextSave",
        description="""
Saves provided description and file contents of all the relevant file paths or globs in a single text file.
- Provide random unqiue id or whatever user provided.
- Leave project path as empty string if no project path""",
    ),
]
