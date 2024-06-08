from pathlib import Path
from typing import List, Tuple
import subprocess


class SourceManager:
    def __init__(self, repo_url: str, src_dir: Path) -> None:
        self.repo_url = repo_url
        self.src_dir = src_dir

    def clone_or_pull_repo(self) -> None:
        """
        Clone the repository if it does not exist, otherwise pull the latest changes.
        """
        if not self.src_dir.exists():
            self._clone_repo()
        else:
            self._pull_repo()

    def _clone_repo(self) -> None:
        """
        Clone the repository from the specified URL.
        """
        subprocess.run(["git", "clone", self.repo_url, str(self.src_dir)], check=True)

    def _pull_repo(self) -> None:
        """
        Pull the latest changes from the repository.
        """
        subprocess.run(["git", "-C", str(self.src_dir), "pull"], check=True)


class TypescriptParser:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    @staticmethod
    def camel_to_snake(name: str) -> str:
        """
        Convert CamelCase to snake_case.

        Args:
            name (str): The CamelCase string.

        Returns:
            str: The converted snake_case string.
        """
        return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip(
            "_"
        )

    @staticmethod
    def parse_typescript_enum(ts_enum: str) -> List[Tuple[str, str]]:
        """
        Parse a TypeScript enum string and convert it to Python enum or dictionary.

        Args:
            ts_enum (str): The TypeScript enum string.

        Returns:
            List[Tuple[str, str]]: The Python code and the enum name.
        """
        lines = iter(ts_enum.splitlines())
        enums = []
        enum_name = ""
        python_enum = "from enum import Enum\n\n\n"
        python_dict = ""
        current_value = 0
        enum_started = False
        is_dict = False
        comment_lines = []
        inside_multiline_comment = False

        for line in lines:
            line = line.strip()

            if not line or line.startswith("import"):
                continue

            if line.startswith("export enum "):
                if enum_started:
                    if is_dict:
                        python_dict = python_dict.rstrip(",\n") + "\n}\n"
                        enums.append((python_dict, enum_name))
                    else:
                        enums.append((python_enum, enum_name))
                    python_enum = "from enum import Enum\n\n\n"
                    python_dict = ""
                    enum_started = False
                    is_dict = False
                    current_value = 0

                enum_name = line.split()[2]
                continue

            if line.startswith("/*") and not line.endswith("*/"):
                inside_multiline_comment = True
                comment_lines = [line]
                continue

            if inside_multiline_comment:
                comment_lines.append(line)
                if line.endswith("*/"):
                    inside_multiline_comment = False
                    comment_block = "\n".join(
                        line.strip("/* ").strip() for line in comment_lines
                    )
                    comment_lines = []
                continue

            if line.startswith("/**"):
                comment_lines = []
                try:
                    while line and not line.endswith("*/"):
                        comment_lines.append(line)
                        line = next(lines).strip()
                    comment_lines.append(line)
                except StopIteration:
                    pass
                continue

            if line.startswith("}"):
                if enum_started:
                    if is_dict:
                        python_dict = python_dict.rstrip(",\n") + "\n}\n"
                        enums.append((python_dict, enum_name))
                    else:
                        enums.append((python_enum, enum_name))
                break

            parts = line.split("=")
            field = parts[0].strip().rstrip(",")
            if len(parts) > 1:
                value = parts[1].strip().rstrip(",").strip('"')
                try:
                    current_value = int(value)
                except ValueError:
                    is_dict = True
                    value = f'"{value}"'
            else:
                value = current_value

            if not enum_started:
                if is_dict:
                    python_dict += f"{enum_name} = {{\n"
                else:
                    python_enum += f"class {enum_name}(Enum):\n"
                enum_started = True

            if is_dict:
                if comment_lines:
                    comment_block = "\n".join(
                        line.strip("/* ").strip() for line in comment_lines
                    )
                    python_dict += f'    "{field}": {value},  # {comment_block}\n'
                    comment_lines = []
                else:
                    python_dict += f'    "{field}": {value},\n'
            else:
                if comment_lines:
                    comment_block = "\n".join(
                        line.strip("/* ").strip() for line in comment_lines
                    )
                    python_enum += f"    {field} = {value}\n"
                    python_enum += f'    """{comment_block}"""\n'
                    comment_lines = []
                else:
                    python_enum += f"    {field} = {value}\n"

            current_value += 1

        if enum_started:
            if is_dict:
                python_dict = python_dict.rstrip(",\n") + "\n}\n"
                enums.append((python_dict, enum_name))
            else:
                enums.append((python_enum, enum_name))

        return enums

    def parse_file(self) -> List[Tuple[str, str]]:
        """
        Parse the TypeScript file and return a list of Python code and enum names.

        Returns:
            List[Tuple[str, str]]: List of tuples containing Python code and enum names.
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            content = file.read()
            return self.parse_typescript_enum(content)


class EnumGenerator:
    def __init__(self, src_dir: Path, out_dir: Path) -> None:
        self.src_dir = src_dir
        self.out_dir = out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def process_typescript_files(self) -> List[Path]:
        """
        Process all TypeScript files in the source directory and generate Python files.

        Returns:
            List[Path]: List of generated Python file paths.
        """
        generated_files = []
        for ts_file in self.src_dir.glob("**/*.ts"):
            parser = TypescriptParser(ts_file)
            parsed_data = parser.parse_file()

            for python_code, enum_name in parsed_data:
                if python_code and enum_name:
                    output_file = (
                        self.out_dir / f"{parser.camel_to_snake(enum_name)}.py"
                    )
                    generated_files.append(output_file)

                    with open(output_file, "w", encoding="utf-8") as py_file:
                        py_file.write(self.add_copyright_header(python_code))

                    print(f"Generated {output_file}")
        return generated_files

    def add_copyright_header(self, python_code: str) -> str:
        """
        Add the copyright header to the generated Python code.

        Args:
            python_code (str): The generated Python code.

        Returns:
            str: The Python code with the copyright header.
        """
        header = '''"""
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
        return header + python_code

    def create_init_py(self, generated_files: List[Path]) -> None:
        """
        Create an __init__.py file with import statements for each generated Python file.

        Args:
            generated_files (List[Path]): List of generated Python file paths.
        """
        header = '''"""
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
        with open(self.out_dir / "__init__.py", "w", encoding="utf-8") as init_file:
            init_file.write(header)
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


if __name__ == "__main__":
    # Directory paths
    _DIR = Path(__file__).resolve().parent
    _OUT = _DIR / "out"
    _SRC = _DIR / "src"

    # Git repository URL
    REPO_URL = "https://github.com/pagefaultgames/pokerogue"

    # Manage the source code
    source_manager = SourceManager(REPO_URL, _SRC)
    source_manager.clone_or_pull_repo()

    # Generate enums
    generator = EnumGenerator(_SRC, _OUT)
    generator.run()
