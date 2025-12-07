#!/usr/bin/env python3
"""
build_agentic_ai.py
PyInstaller build script for AgenticAI Builder
Cross-platform, fully validated, production-ready
Includes OS check, library validation, recursive module inclusion, logging, progress bars, uninstall, backups, and post-build verification
"""

import os
import sys
import subprocess
import platform
import shutil
import datetime
import json
import time
from pathlib import Path
from tqdm import tqdm

# ---------------- CONFIGURATION ----------------

MAIN_SCRIPT = "agentic_ai_builder.py"
PROJECT_DIR = Path(__file__).parent.resolve()
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build"
SPEC_DIR = PROJECT_DIR / "specs"
LOG_FILE = PROJECT_DIR / "build.log"
UNINSTALL_FILE = PROJECT_DIR / "uninstall_record.json"

FOLDERS_TO_INCLUDE = ["app", "core", "assets", "templates", "outputs", "config"]
REQUIRED_LIBRARIES = ["tkinter", "Pillow", "rich", "tqdm"]
SUPPORTED_OSES = ["Windows", "Darwin", "Linux"]
ONEFILE = True
WINDOWED = True
DEBUG_MODE = False
BUILD_VERSION = "1.0.0"

# ---------------- LOGGING ----------------

def log(msg, level="INFO"):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# ---------------- OS CHECK ----------------

def check_supported_os():
    current_os = platform.system()
    log(f"Detected OS: {current_os}")
    if current_os not in SUPPORTED_OSES:
        log(f"Unsupported OS: {current_os}. Exiting.", "ERROR")
        sys.exit(1)

# ---------------- LIBRARY CHECK ----------------

def check_libraries():
    missing = []
    for lib in REQUIRED_LIBRARIES:
        try:
            __import__(lib)
        except ImportError:
            missing.append(lib)
    return missing

def prompt_install_missing(missing):
    log("Missing required Python libraries detected:", "WARN")
    for lib in missing:
        log(f" - {lib}", "WARN")
    ans = input("Install missing libraries now? (y/n): ").strip().lower()
    if ans == "y":
        for lib in missing:
            log(f"Installing {lib}...")
            subprocess.run([sys.executable, "-m", "pip", "install", lib])
    else:
        log("Cannot continue without required libraries. Exiting.", "ERROR")
        sys.exit(1)

# ---------------- CLEANUP ----------------

def backup_and_clean(path):
    if path.exists():
        backup_path = path.with_name(f"{path.name}_backup_{int(time.time())}")
        shutil.move(str(path), str(backup_path))
        log(f"Backed up {path} to {backup_path}")

def clean_previous_builds():
    for path in [DIST_DIR, BUILD_DIR, SPEC_DIR]:
        backup_and_clean(path)
    if LOG_FILE.exists():
        LOG_FILE.unlink()
        log(f"Removed old log file {LOG_FILE}")

# ---------------- ADD-DATA FLAGS ----------------

def format_add_data(folder):
    folder_path = PROJECT_DIR / folder
    if not folder_path.exists():
        return None
    if platform.system() == "Windows":
        return f"{folder};{folder}"
    else:
        return f"{folder}:{folder}"

def collect_add_data(folders):
    add_data_flags = []
    for folder in folders:
        flag = format_add_data(folder)
        if flag:
            add_data_flags.append(flag)
    return add_data_flags

# ---------------- RECURSIVE FILE SCAN ----------------

def scan_project_files(folders):
    files = []
    for folder in folders:
        folder_path = PROJECT_DIR / folder
        if folder_path.exists():
            for root, _, filenames in os.walk(folder_path):
                for f in filenames:
                    files.append(str(Path(root) / f))
    return files

# ---------------- UNINSTALL ----------------

def save_uninstall_record(exe_path, files_list):
    records = files_list + [str(exe_path)]
    with open(UNINSTALL_FILE, "w") as f:
        json.dump(records, f, indent=4)
    log(f"Saved uninstall record for {len(records)} files.")

def uninstall():
    if UNINSTALL_FILE.exists():
        with open(UNINSTALL_FILE, "r") as f:
            files = json.load(f)
        log("Starting uninstallation...")
        for file in tqdm(files, desc="Removing files"):
            path = Path(file)
            if path.exists():
                try:
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
                except Exception as e:
                    log(f"Failed to remove {path}: {e}", "ERROR")
        UNINSTALL_FILE.unlink()
        log("Uninstallation complete.")
        sys.exit(0)
    else:
        log("No uninstall record found.", "WARN")
        sys.exit(1)

# ---------------- BUILD EXECUTABLE ----------------

def construct_pyinstaller_cmd(add_data_flags):
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
    if DEBUG_MODE:
        cmd.append("--debug=all")
    for flag in add_data_flags:
        cmd.append(f"--add-data={flag}")
    return cmd

def build_executable():
    log("Collecting folders for inclusion...")
    add_data_flags = collect_add_data(FOLDERS_TO_INCLUDE)
    log(f"Found {len(add_data_flags)} folders to include.")

    log("Scanning project files...")
    all_files = scan_project_files(FOLDERS_TO_INCLUDE)
    for _ in tqdm(all_files, desc="Scanning files", ncols=100):
        time.sleep(0.001)

    cmd = construct_pyinstaller_cmd(add_data_flags)
    log("Running PyInstaller...")
    log(" ".join(cmd))

    with tqdm(total=1, desc="Building executable", ncols=100) as pbar:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pbar.update(1)

    if result.returncode != 0:
        log("ERROR: Build failed!", "ERROR")
        log(result.stderr, "ERROR")
        sys.exit(1)
    else:
        log("SUCCESS: Build completed!")

    exe_name = "agentic_ai_builder"
    if platform.system() == "Windows":
        exe_name += ".exe"
    exe_path = DIST_DIR / exe_name
    if exe_path.exists():
        log(f"Executable verified at {exe_path}")
        save_uninstall_record(exe_path, all_files)
    else:
        log("ERROR: Executable not found!", "ERROR")
        sys.exit(1)

# ---------------- MAIN ----------------

def main():
    log(f"AgenticAI Builder PyInstaller Build v{BUILD_VERSION} starting...")
    check_supported_os()

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
