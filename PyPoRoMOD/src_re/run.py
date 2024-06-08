import os
import shutil
import subprocess
import requests
from zipfile import ZipFile
from pathlib import Path

# Constants
REPO_URL = "https://github.com/pagefaultgames/pokerogue/archive/refs/heads/main.zip"
DIR = Path(__file__).resolve().parent
VERSION_FILE = DIR / "current_version.txt"
DOWNLOAD_DIR = DIR / "downloaded_repo"
REPO_DIR = DOWNLOAD_DIR / "pokerogue-main"
BUILD_DIR = REPO_DIR / "build"
DIST_DIR = REPO_DIR / "dist"
MASTER_TSCONFIG = DIR / "tsconfig.json"
MASTER_VITE_CONFIG = DIR / "vite.config.ts"


# Functions
def get_repo_version():
    url = "https://api.github.com/repos/pagefaultgames/pokerogue/commits/main"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["sha"]
    return None


def download_repo():
    response = requests.get(REPO_URL)
    if response.status_code == 200:
        with open("repo.zip", "wb") as f:
            f.write(response.content)
        with ZipFile("repo.zip", "r") as zip_ref:
            zip_ref.extractall(DOWNLOAD_DIR)
        os.remove("repo.zip")
        return True
    return False


def compile_ts_to_js():
    subprocess.run(["npm", "run", "build"], check=True, cwd=REPO_DIR, shell=True)


def save_version(version):
    with open(VERSION_FILE, "w") as f:
        f.write(version)


def load_version():
    if VERSION_FILE.exists():
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    return None


def copy_master_files():
    shutil.copy(MASTER_TSCONFIG, REPO_DIR / "tsconfig.json")
    shutil.copy(MASTER_VITE_CONFIG, REPO_DIR / "vite.config.ts")


# Main logic
if __name__ == "__main__":
    new_version = get_repo_version()
    # current_version = load_version()

    # if new_version != current_version:
    # print("New version detected. Updating...")

    # if DOWNLOAD_DIR.exists():
    #     shutil.rmtree(DOWNLOAD_DIR)
    # if BUILD_DIR.exists():
    #     shutil.rmtree(BUILD_DIR)
    # if DIST_DIR.exists():
    #     shutil.rmtree(DIST_DIR)

    # download_repo()
    copy_master_files()

    # print("Installing dependencies...")
    # subprocess.run(
    #     [
    #         "npm",
    #         "install",
    #         "vite",
    #         "rollup",
    #         "@rollup/plugin-node-resolve rollup-plugin-terser",
    #         "--save-dev",
    #     ],
    #     check=True,
    #     cwd=REPO_DIR,
    #     shell=True,
    # )

    print("Compiling TypeScript to JavaScript...")
    compile_ts_to_js()

    save_version(new_version)
    print("Update complete.")
    # else:
    #     print("No new updates.")
