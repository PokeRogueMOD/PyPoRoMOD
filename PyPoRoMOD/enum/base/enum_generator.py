from pathlib import Path
from typing import List
from typescript_parser import TypescriptParser
from enum import Enum


class EnumGenerator:
    HEADER = '''"""
BSD 3-Clause License

Copyright (c) 2024, Philipp Reuter
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions, and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions, and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

'''

    def __init__(self, src_dir: Path, out_dir: Path) -> None:
        self.src_dir = src_dir
        self.out_dir = out_dir
        self.invalid_dir = out_dir / "invalid"
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.invalid_dir.mkdir(parents=True, exist_ok=True)

    def process_typescript_files(self) -> List[Path]:
        """
        Process all TypeScript files in the source directory and generate Python files.

        Returns:
            List of generated valid Python file paths.
        """
        generated_files = []
        for ts_file in self.src_dir.glob("**/*.ts"):
            parser = TypescriptParser(ts_file)
            parsed_data = parser.parse_file()

            for python_code, enum_name in parsed_data:
                if python_code and enum_name:
                    # Skip saving empty dictionaries
                    if python_code.strip() == f"{enum_name} = {{\n}}\n":
                        continue

                    if self.is_valid_python_code(python_code):
                        output_file = (
                            self.out_dir / f"{parser.camel_to_snake(enum_name)}.py"
                        )
                        with open(output_file, "w", encoding="utf-8") as py_file:
                            py_file.write(self.add_copyright_header(python_code))
                        generated_files.append(output_file)
                        print(f"Generated {output_file}")
                    else:
                        invalid_output_file = (
                            self.invalid_dir / f"{parser.camel_to_snake(enum_name)}.py"
                        )
                        with open(
                            invalid_output_file, "w", encoding="utf-8"
                        ) as py_file:
                            py_file.write(self.add_copyright_header(python_code))
                        print(f"Invalid Python code. Moved to {invalid_output_file}")

        return generated_files

    @staticmethod
    def is_valid_python_code(code: str) -> bool:
        """
        Check if the Python code string is valid by attempting to evaluate it.

        Args:
            code (str): The Python code string.

        Returns:
            bool: True if the Python code is valid, False otherwise.
        """
        try:
            if code.endswith(" = {\n}\n"):
                return False

            exec(code, {"__builtins__": None, "Enum": Enum}, {})
            return True
        except (SyntaxError, ValueError) as e:
            return False
        except Exception as e:
            return False

    def add_copyright_header(self, python_code: str) -> str:
        """
        Add the copyright header to the generated Python code.

        Args:
            python_code (str): The generated Python code.

        Returns:
            str: The Python code with the copyright header.
        """
        return self.HEADER + python_code

    def create_init_py(self, generated_files: List[Path]) -> None:
        """
        Create an __init__.py file with import statements for each generated Python file.

        Args:
            generated_files (List[Path]): List of generated Python file paths.
        """
        with open(self.out_dir / "__init__.py", "w", encoding="utf-8") as init_file:
            init_file.write(self.HEADER)
            for py_file in generated_files:
                module_name = py_file.stem
                class_name = "".join(word.title() for word in module_name.split("_"))
                init_file.write(f"from .{module_name} import {class_name}\n")

    def run(self) -> None:
        """
        Run the enum generation process.
        """
        generated_files = self.process_typescript_files()
        self.create_init_py(generated_files)
