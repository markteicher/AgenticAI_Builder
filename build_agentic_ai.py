import os
import platform
import subprocess
import sys

# ----------------------------
# Configuration
# ----------------------------
APP_NAME = "AgenticAI Builder"
SCRIPT_NAME = "agentic_ai_builder.py"  # Path to main GUI script
ASSETS_DIR = "assets"                   # Optional assets folder
ICON_FILE = os.path.join(ASSETS_DIR, "icon.ico")  # Windows icon
MAC_ICON_FILE = os.path.join(ASSETS_DIR, "icon.icns")  # macOS icon

DIST_DIR = "dist"
BUILD_DIR = "build"

# ----------------------------
# Detect platform
# ----------------------------
current_os = platform.system()
print(f"Building {APP_NAME} for {current_os}...")

# ----------------------------
# Construct PyInstaller command
# ----------------------------
cmd = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--name", APP_NAME,
    "--distpath", DIST_DIR,
    "--workpath", BUILD_DIR,
    SCRIPT_NAME
]

# Add icon if exists
if current_os == "Windows" and os.path.exists(ICON_FILE):
    cmd += ["--icon", ICON_FILE]
elif current_os == "Darwin" and os.path.exists(MAC_ICON_FILE):
    cmd += ["--icon", MAC_ICON_FILE]

# Include assets folder if it exists
if os.path.exists(ASSETS_DIR):
    sep = ";" if current_os == "Windows" else ":"
    cmd += ["--add-data", f"{ASSETS_DIR}{sep}{ASSETS_DIR}"]

# Hidden imports
cmd += ["--hidden-import", "PIL"]

print("Running PyInstaller command:")
print(" ".join(cmd))

# ----------------------------
# Run PyInstaller
# ----------------------------
try:
    subprocess.check_call(cmd)
    print(f"PyInstaller build complete. Executable in {DIST_DIR}")
except subprocess.CalledProcessError as e:
    print(f"Error during PyInstaller build: {e}")
    sys.exit(1)

# ----------------------------
# Instructions for installer creation
# ----------------------------
if current_os == "Windows":
    print("\nWindows Installer (NSIS):")
    print(f" - Use NSIS to wrap {os.path.join(DIST_DIR, APP_NAME+'.exe')} into an installer")
    print(f" - Default install path: C:\\Program Files\\{APP_NAME}")
elif current_os == "Darwin":
    print("\nmacOS Installer:")
    print(f" - To create .pkg: pkgbuild --root {os.path.join(DIST_DIR, APP_NAME+'.app')} --identifier com.company.agenticai --version 1.0 {APP_NAME}.pkg")
    print(f" - To create .dmg: hdiutil create -volname '{APP_NAME}' -srcfolder {os.path.join(DIST_DIR, APP_NAME+'.app')} -ov -format UDZO {APP_NAME}.dmg")
elif current_os == "Linux":
    print("\nLinux Installer:")
    sh_file = os.path.join(DIST_DIR, f"install_{APP_NAME.lower().replace(' ', '_')}.sh")
    with open(sh_file, "w") as f:
        f.write(f"""#!/bin/bash
INSTALL_DIR="/opt/{APP_NAME.replace(' ', '')}"
mkdir -p "$INSTALL_DIR"
cp "{os.path.join(DIST_DIR, APP_NAME)}" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/{APP_NAME}"
echo "Installation complete. Run $INSTALL_DIR/{APP_NAME}"
""")
    os.chmod(sh_file, 0o755)
    print(f" - Linux installer script generated: {sh_file}")

print("\nBuild process complete. Executables and installer instructions ready.")
