import re
from pathlib import Path
from typing import List, Tuple


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
    def parse_typescript_object(ts_object: str) -> List[Tuple[str, str]]:
        """
        Parse a TypeScript object string and convert it to a Python dictionary.

        Args:
            ts_object (str): The TypeScript object string.

        Returns:
            List[Tuple[str, str]]: The Python code and the object name.
        """
        lines = ts_object.strip().splitlines()
        parsed_objects = []
        object_name = None
        python_dict = ""

        for line in lines:
            line = line.strip()
            if line.startswith("const "):
                if python_dict:
                    python_dict = python_dict.rstrip(",\n") + "\n}\n"
                    parsed_objects.append((python_dict, object_name))
                object_name = re.findall(r"const (\w+)", line)
                if not object_name:
                    continue
                object_name = object_name[0]
                python_dict = f"{object_name} = {{\n"
            elif line.endswith("};"):
                python_dict = python_dict.rstrip(",\n") + "\n}\n"
                parsed_objects.append((python_dict, object_name))
                python_dict = ""
            elif ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                python_dict += f'    "{key}": {value},\n'

        if python_dict:
            python_dict = python_dict.rstrip(",\n") + "\n}\n"
            parsed_objects.append((python_dict, object_name))

        # Filter out empty dictionaries
        return [
            obj for obj in parsed_objects if obj[0].strip() != f"{obj[1]} = {{\n}}\n"
        ]

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

            if line.startswith("const "):
                object_code_list = TypescriptParser.parse_typescript_object(
                    "\n".join([line] + list(lines))
                )
                enums.extend(object_code_list)
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
            parsed_data = self.parse_typescript_enum(content)
            parsed_data += self.parse_typescript_object(content)
            return parsed_data
