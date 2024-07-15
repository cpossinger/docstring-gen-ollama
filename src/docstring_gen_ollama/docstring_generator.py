import argparse
import logging
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
    parse,
    unparse,
)
from typing import Any, Optional, Union

from ollama import generate


class DocstringGenerator(NodeTransformer):

    def __init__(self, model: str, prompt: str):
        self.model = model
        self.prompt = prompt

    def extract_docstring(self, text: str) -> Optional[str]:
        pattern = r'"""(.*?)"""'
        matches = re.findall(pattern, text, re.DOTALL)
        return matches[0] if matches else None

    def add_docstring(
        self, node: Union[ClassDef, FunctionDef, AsyncFunctionDef]
    ) -> Union[ClassDef, FunctionDef, AsyncFunctionDef]:
        prompt = self.prompt + unparse(node)
        response = generate(model=self.model, prompt=prompt)

        docstring = Expr(
            value=Constant(value=self.extract_docstring(response["response"]))
        )
        node.body.insert(0, docstring)
        return node

    def visit(self, node: AST) -> AST:
        if isinstance(
            node, (ClassDef, FunctionDef, AsyncFunctionDef)
        ) and not get_docstring(node):
            return self.generic_visit(self.add_docstring(node))
        else:
            return self.generic_visit(node)


def handle_python_file(file_path: str, model: str, prompt: str) -> None:
    with open(file_path) as file:
        tree = parse(file.read())
    new_tree = DocstringGenerator(model, prompt).visit(tree)
    with open(file_path, "w") as file:
        file.write(unparse(new_tree))


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

    parser = argparse.ArgumentParser(
        description="Generate docstrings for Python files."
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
        default='write an accurate google styled docstring inside """ for this python code: \n ',
        help="The prompt to use for generating docstrings.",
    )
    args = parser.parse_args()

    with multiprocessing.Pool() as pool:
        python_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(".", topdown=True)
            for file in files
            if file.endswith(".py") and not file.startswith("__")
        ]
        for file in python_files:
            logging.info(f"Processing file: {file}")
            pool.apply(handle_python_file, (file, args.model, args.prompt))

    logging.info("All files processed successfully.")


if __name__ == "__main__":
    main()

