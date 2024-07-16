import argparse
import multiprocessing
import os
import re
from ast import (
    AST,
    AsyncFunctionDef,
    ClassDef,
    Constant,
    Expr,
    FunctionDef,
    NodeTransformer,
    get_docstring,
    iter_child_nodes,
    parse,
    unparse,
)
from typing import NamedTuple, Union

from ollama import generate
from tqdm import tqdm


class PythonFile(NamedTuple):
    """
    Represents a Python file with its metadata.

    Attributes:
        relative_path (str): The relative path to the Python file.
        model (str): The name of the machine learning model used in this file.
        prompt (str): A prompt or description for the file.
        position (int): The position or ranking of the file within a directory or project.

    """

    relative_path: str
    model: str
    prompt: str
    position: int


def count_nodes(node: AST) -> int:
    """Counts the number of nodes with no docstrings.

    This function takes an Abstract Syntax Tree (AST) node as input, and returns
    the count of child nodes that are either ClassDef, FunctionDef or AsyncFunctionDef,
    and have no docstring. This can be useful for identifying nodes in the AST that
    don't have a corresponding docstring in the code.

    Parameters:
        node: The Abstract Syntax Tree (AST) node to examine.

    Returns:
        An integer representing the count of child nodes with no docstrings.
    """
    return sum(
        (
            isinstance(child, (ClassDef, FunctionDef, AsyncFunctionDef))
            and (not get_docstring(child))
            for child in iter_child_nodes(node)
        )
    )


class DocstringGenerator(NodeTransformer):
    """
    A NodeTransformer that generates and adds docstrings to Python nodes.

    Attributes:
      model (str): The language model used to generate docstrings.
      prompt (str): The prompt used to generate docstrings.
      pbar (tqdm): A progress bar used to track the generation of docstrings.

    Methods:
      extract_docstring(text: str) -> str:
          Extracts a docstring from a given text using regular expressions.

      add_docstring(node: Union[ClassDef, FunctionDef, AsyncFunctionDef]) -> Union[ClassDef, FunctionDef, AsyncFunctionDef]:
          Adds a generated docstring to the given node and updates the progress bar.

      visit(self, node: AST) -> AST:
          Visits a node in an Abstract Syntax Tree (AST) and adds a docstring if it doesn't already have one.
    """

    def __init__(self, model: str, prompt: str, pbar: tqdm):
        """
        Initializes the class with a given `model`, `prompt`, and `pbar`.

        Args:
          - model (str): The name of the model.
          - prompt (str): The text to be used as a prompt for generation.
          - pbar (tqdm): A progress bar object to track generation progress.

        Returns:
          None
        """
        self.model = model
        self.prompt = prompt
        self.pbar = pbar

    def extract_docstring(self, text: str) -> str:
        """
        Extracts the Google-style docstring from a given block of text.

        Args:
            self (object): This parameter is required but not used in this function.
            text (str): The input text that may contain a docstring.

        Returns:
            str: The extracted docstring, or an empty string if no docstring was found.
        """
        pattern = '"""(.*?)"""'
        matches = re.findall(pattern, text, re.DOTALL)
        return matches[0] if matches else ""

    def add_docstring(
        self, node: Union[ClassDef, FunctionDef, AsyncFunctionDef]
    ) -> Union[ClassDef, FunctionDef, AsyncFunctionDef]:
        """
        Adds a generated docstring to the specified AST node.

        Args:
          self: The current instance of the class.
          node: The AST node to add the docstring to. Can be a ClassDef, FunctionDef, or AsyncFunctionDef.

        Returns:
          The modified AST node with the added docstring.
        """
        prompt = self.prompt + unparse(node)
        response = generate(model=self.model, prompt=prompt)
        docstring = Expr(
            value=Constant(value=self.extract_docstring(response["response"]))
        )
        node.body.insert(0, docstring)
        self.pbar.update()
        return node

    def visit(self, node: AST) -> AST:
        """
        Visit a node in an Abstract Syntax Tree (AST) and add a docstring if necessary.

        Args:
          self: The current visitor object.
          node: An Abstract Syntax Tree (AST) node to visit.

        Returns:
          An AST node, possibly with a new docstring added.
        """
        if isinstance(node, (ClassDef, FunctionDef, AsyncFunctionDef)) and (
            not get_docstring(node)
        ):
            return self.generic_visit(self.add_docstring(node))
        else:
            return self.generic_visit(node)


def handle_python_file(python_file: PythonFile) -> None:
    """
    Handles a Python file by parsing its contents, generating Docstrings,
    and writing them back to the original file.

    Args:
        python_file (PythonFile): The Python file to be handled.
            This should contain information about the relative path
            and position of the file.

    Returns:
        None: No return value is expected.

    Side effects:
        Writes the parsed and processed content to the original file.
        Creates a progress bar with a description that indicates the file being processed.
    """
    with open(python_file.relative_path) as file:
        source = file.read()
        tree = parse(source)
    pbar = tqdm(total=count_nodes(tree), position=python_file.position)
    pbar.set_description(f"Processing {python_file.relative_path}")
    new_tree = DocstringGenerator(python_file.model, python_file.prompt, pbar).visit(
        tree
    )
    with open(python_file.relative_path, "w") as file:
        file.write(unparse(new_tree))
    pbar.close()


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


if __name__ == "__main__":
    main()

