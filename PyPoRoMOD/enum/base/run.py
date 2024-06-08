from pathlib import Path

from enum_generator import EnumGenerator
from source_manager import SourceManager


if __name__ == "__main__":
    # Directory paths
    _DIR = Path(__file__).resolve().parent
    _OUT = _DIR / "_base"
    _SRC = _DIR / "src"

    # Git repository URL
    REPO_URL = "https://github.com/pagefaultgames/pokerogue"

    # Manage the source code
    source_manager = SourceManager(REPO_URL, _SRC)
    source_manager.clone_or_pull_repo()

    # Generate enums
    generator = EnumGenerator(_SRC, _OUT)
    generator.run()
