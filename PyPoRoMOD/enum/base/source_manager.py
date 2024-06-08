from pathlib import Path
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
