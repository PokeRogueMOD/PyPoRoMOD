from pathlib import Path
import re

# Directory paths
_DIR = Path(__file__).resolve().parent
_OUT = _DIR / "out"
_SRC = _DIR / "src"


# Src: https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def camel_to_snake(s):
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def parse_typescript_enum(ts_enum: str):
    lines = iter(ts_enum.splitlines())
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

        # Skip empty lines and import lines
        if not line or line.startswith("import"):
            continue

        # Extract the enum name
        if line.startswith("export enum "):
            enum_name = line.split()[2]
            continue

        # Handle multiline comments
        if line.startswith("/*") and not line.endswith("*/"):
            inside_multiline_comment = True
            comment_lines = []
            comment_lines.append(line)
            continue

        if inside_multiline_comment:
            comment_lines.append(line)
            if line.endswith("*/"):
                inside_multiline_comment = False

                # Add comments above the enum field if present
                if comment_lines:
                    if is_dict:
                        python_dict += '    """\n'
                        for comment_line in comment_lines:
                            python_dict += f"    {comment_line.strip('/* ').strip()}\n"
                        python_dict += '    """\n'
                    else:
                        python_enum += '    """\n'
                        for comment_line in comment_lines:
                            python_enum += f"    {comment_line.strip('/* ').strip()}\n"
                        python_enum += '    """\n'
                    comment_lines = []  # Reset comment lines after adding them

            continue

        # Handle single-line comments
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

        # Handle enum fields and their values
        if line.startswith("}"):
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
                python_dict += f"{camel_to_snake(enum_name)} = {{\n"
            else:
                python_enum += f"class {enum_name}(Enum):\n"
            enum_started = True

        # Add comments above the enum field if present
        if comment_lines:
            if is_dict:
                for comment_line in comment_lines:
                    python_dict += (
                        f"    \"\"\" {comment_line.strip('/* ').strip()} \"\"\"\n"
                    )
            else:
                for comment_line in comment_lines:
                    python_enum += (
                        f"    \"\"\" {comment_line.strip('/* ').strip()} \"\"\"\n"
                    )
            comment_lines = []  # Reset comment lines after adding them

        if is_dict:
            python_dict += f'    "{field}": {value},\n'
        else:
            python_enum += f"    {field} = {value}\n"
        current_value += 1

    if is_dict:
        python_dict = python_dict.rstrip(",\n") + "\n}\n"
        return python_dict, enum_name
    else:
        return python_enum, enum_name


def process_typescript_files(src_path):
    for ts_file in src_path.glob("*.ts"):
        with open(ts_file, "r", encoding="utf-8") as file:
            content = file.read()
            python_code, enum_name = parse_typescript_enum(content)

            if python_code:
                output_file = _OUT / f"{camel_to_snake(enum_name)}.py"

                with open(output_file, "w", encoding="utf-8") as py_file:
                    py_file.write(python_code)

                print(f"Generated {output_file}")


# Ensure the output directory exists
_OUT.mkdir(parents=True, exist_ok=True)

# Process all TypeScript files in the specified directory
process_typescript_files(_SRC)
