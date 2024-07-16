# SPDX-FileCopyrightText: 2024-present 164182 <camden.possinger@delta.com>
#
# SPDX-License-Identifier: MIT

import argparse
import multiprocessing
import os

from docstring_gen_ollama.docstring_generator import PythonFile, handle_python_file


def main() -> None:
    """
    Generates docstrings for Python files using the provided model and prompt.

    Args:
        --path (str): The path to use for generating docstrings. Defaults to '.'.
        --model (str): The model to use for generating docstrings. Defaults to 'llama3'.
        --prompt (str): The prompt to use for generating docstrings. Defaults to 'write a google styled docstring inside triple quotes for this python code: \\n '.

    Returns:
    None
    """
    parser = argparse.ArgumentParser(
        description="Generate docstrings for Python files."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The path to use for generating docstrings.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="llama3",
        help="The model to use for generating docstrings.",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="write a google styled docstring inside triple quotes for this python code: \n ",
        help="The prompt to use for generating docstrings.",
    )
    args = parser.parse_args()
    with multiprocessing.Pool() as pool:
        python_files = [
            PythonFile(os.path.join(root, file), args.model, args.prompt, position)
            for root, _, files in os.walk(args.path, topdown=True)
            for position, file in enumerate(files)
            if file.endswith(".py") and (not file.startswith("__"))
        ]
        for _ in pool.imap_unordered(handle_python_file, python_files):
            pass
