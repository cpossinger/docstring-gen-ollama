import multiprocessing
import os
import re
from ast import (
    AsyncFunctionDef,
    ClassDef,
    FunctionDef,
    NodeTransformer,
    get_docstring,
    parse,
    unparse,
)

from ollama import generate

PROMPT = "rewrite this python code inside ``` with a google styled docstring if it's a function write the docstring just for that function if it's a class write docstrings for the class methods too do not change the original code just add a docstring: \n"


class DocstringGenerator(NodeTransformer):

    def extract_code(self, text: str) -> str | None:
        pattern = r"```(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        return matches[0] if matches else None

    def add_docstring(self, node):
        prompt = PROMPT + unparse(node)
        response = generate(model="llama3", prompt=prompt)
        code_with_docstring = self.extract_code(response["response"])
        print(f"CODE BEFORE DOCSTRING: {unparse(node)}")
        print(f"CODE AFTER DOCSTRING: {code_with_docstring}")
        new_tree = parse(code_with_docstring)

        new_node = FunctionDef(
            name=node.name,
            args=node.args,
            body=new_tree.body[0].body,
            decorator_list=node.decorator_list,
            returns=node.returns,
        )

        return new_node

    def visit(self, node):
        match node:
            case FunctionDef() | AsyncFunctionDef() if not get_docstring(node):
                return self.generic_visit(self.add_docstring(node))
            case ClassDef() if not get_docstring(node):
                return self.add_docstring(node)
            case _:
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
