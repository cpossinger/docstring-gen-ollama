import multiprocessing
import os
import re
from ast import (
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

from ollama import generate

PROMPT = 'write a google styled docstring inside """ for this python code: \n '


class DocstringGenerator(NodeTransformer):

    def extract_docstring(self, text: str) -> str | None:
        pattern = r'"""(.*?)"""'
        matches = re.findall(pattern, text, re.DOTALL)
        return matches[0] if matches else None

    def add_docstring(self, node):
        prompt = PROMPT + unparse(node)
        response = generate(model="llama3", prompt=prompt)

        docstring = Expr(
            value=Constant(value=self.extract_docstring(response["response"]))
        )
        node.body.insert(0, docstring)
        return node

    def visit(self, node):
        if isinstance(
            node, (ClassDef, FunctionDef, AsyncFunctionDef)
        ) and not get_docstring(node):
            return self.generic_visit(self.add_docstring(node))
        else:
            return self.generic_visit(node)


def handle_python_file(file_path):
    with open(file_path) as file:
        tree = parse(file.read())
    new_tree = DocstringGenerator().visit(tree)
    with open(file_path, "w") as file:
        file.write(unparse(new_tree))


def create_and_start_process(file_path):
    process = multiprocessing.Process(target=handle_python_file, args=(file_path,))
    process.start()
    return process


def main():
    processes = [
        create_and_start_process(os.path.join(root, file))
        for root, _, files in os.walk(".", topdown=True)
        for file in files
        if file.endswith(".py") and not file.startswith("__")
    ]

    [process.join() for process in processes]


if __name__ == "__main__":
    main()
