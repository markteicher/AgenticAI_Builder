#!/usr/bin/env python3
"""
build_agentic_ai_full.py
Professional PyInstaller build script for AgenticAI Builder
Cross-platform (Windows, macOS, Linux)
"""

import os
import sys
import subprocess
import platform
import shutil
import datetime
from pathlib import Path
from tqdm import tqdm

# ---------------------- CONFIGURATION ----------------------
MAIN_SCRIPT = "agentic_ai_builder.py"
PROJECT_DIR = Path(__file__).parent.resolve()
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build"
SPEC_DIR = PROJECT_DIR / "specs"
LOG_FILE = PROJECT_DIR / "build.log"

FOLDERS_TO_INCLUDE = ["app", "core", "assets", "templates", "outputs", "config"]
REQUIRED_LIBRARIES = ["tkinter", "Pillow", "rich", "tqdm"]
ONEFILE = True
WINDOWED = True
BUILD_VERSION = "1.0.0"

# ---------------------- LOGGING ----------------------
def log(msg):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# ---------------------- LIBRARY CHECK ----------------------
def check_libraries():
    missing = []
    for lib in REQUIRED_LIBRARIES:
        try:
            __import__(lib)
        except ImportError:
            missing.append(lib)
    return missing

def prompt_install_missing(missing):
    log("Missing required libraries detected:")
    for lib in missing:
        log(f" - {lib}")
    ans = input("Install missing libraries now? (y/n): ").strip().lower()
    if ans == "y":
        for lib in missing:
            log(f"Installing {lib}...")
            subprocess.run([sys.executable, "-m", "pip", "install", lib])
    else:
        log("Cannot continue without required libraries. Exiting.")
        sys.exit(1)

# ---------------------- CLEAN PREVIOUS BUILDS ----------------------
def clean_previous_builds():
    for path in [DIST_DIR, BUILD_DIR, SPEC_DIR, LOG_FILE]:
        if path.exists():
            if path.is_dir():
                log(f"Cleaning directory {path}")
                shutil.rmtree(path)
            else:
                log(f"Removing file {path}")
                path.unlink()

# ---------------------- ADD-DATA FLAGS ----------------------
def format_add_data(folder):
    folder_path = PROJECT_DIR / folder
    if not folder_path.exists():
        return None
    if platform.system() == "Windows":
        return f"{folder};{folder}"
    else:
        return f"{folder}:{folder}"

# ---------------------- BUILD EXECUTABLE ----------------------
def build_executable():
    log("Starting PyInstaller build process...")
    cmd = [
        "pyinstaller",
        str(MAIN_SCRIPT),
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
        "--specpath", str(SPEC_DIR),
        "--noconfirm"
    ]
    if ONEFILE:
        cmd.append("--onefile")
    if WINDOWED:
        cmd.append("--windowed")

    # Add data folders
    for folder in FOLDERS_TO_INCLUDE:
        add_data_flag = format_add_data(folder)
        if add_data_flag:
            cmd.append(f"--add-data={add_data_flag}")

    log("Final PyInstaller command:")
    log(" ".join(cmd))

    # Execute with progress bar
    with tqdm(total=1, desc="Building executable", ncols=100) as pbar:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pbar.update(1)

    if result.returncode != 0:
        log("ERROR: Build failed!")
        log(result.stderr)
        sys.exit(1)
    else:
        log("SUCCESS: Build completed!")
        log(f"Executable available in '{DIST_DIR}'")

# ---------------------- MAIN ----------------------
def main():
    log(f"AgenticAI Builder PyInstaller Build v{BUILD_VERSION} starting...")
    missing = check_libraries()
    if missing:
        prompt_install_missing(missing)

    clean_previous_builds()
    DIST_DIR.mkdir(exist_ok=True)
    BUILD_DIR.mkdir(exist_ok=True)
    SPEC_DIR.mkdir(exist_ok=True)

    build_executable()
    log("Build process finished successfully.")

if __name__ == "__main__":
    main()
