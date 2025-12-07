# AgenticAI Builder: Build Script Documentation

## Overview

`build_agentic_ai.py` is the professional PyInstaller build and cross-platform installer workflow for **AgenticAI Builder**.  
It automates the creation of executable files and installers for **Windows, macOS, and Linux**, ensuring a consistent, repeatable, and fully professional build process.  

This script handles library validation, backups, OS detection, installer generation, logging, progress tracking, uninstall functionality, and post-build verification.

---

## Features

- **Cross-platform executable build** via PyInstaller  
- **Operating System Detection**:
  - Windows, macOS (Darwin), Linux  
  - Detects unsupported platforms and cloud environments (e.g., AWS EC2)  
- **Library Validation**:  
  - Checks for required Python libraries: `tkinter`, `Pillow`, `rich`, `tqdm`  
  - Prompts user to install missing libraries, optionally with proxy support  
- **Folder & Module Inclusion**:  
  - Automatically includes all project folders: `app/`, `core/`, `assets/`, `templates/`, `outputs/`, `config/`  
- **OS-Specific Installer Generation**:
  - **Windows**: NSIS installer with progress bars, shortcuts, uninstall functionality  
  - **macOS**: `.pkg` installer, optional `.dmg` for drag-and-drop installation  
  - **Linux**: `.deb` (Debian/Ubuntu) and `.rpm` (RedHat/Fedora) packages  
- **Backup & Cleanup**:  
  - Backs up previous builds before creating new ones  
  - Cleans old `build/`, `dist/`, and `specs/` folders  
- **Logging**:
  - Detailed logs with UTC timestamps to `build.log`  
  - Tracks all steps: scanning, building, installer creation  
- **Progress Bars**: Uses `tqdm` to visualize scanning, building, and installer creation  
- **Post-Build Verification**: Ensures all executables and installers exist and are complete  
- **Uninstall Support**: Tracks installed files in `uninstall_record.json` for developer removal  
- **Build Metadata & Versioning**: Embedded in logs, installer, and executable  
- **Error Handling & Retry Logic**: For missing libraries, build failures, or installer errors  

---

## Prerequisites

### Python
- Python 3.10+ installed and available in PATH

### Required Python Libraries
- `tkinter` (GUI library)  
- `Pillow` (image handling)  
- `rich` (enhanced logging)  
- `tqdm` (progress bars)  

### OS-Specific Tools
- **Windows**: NSIS (`makensis`)  
- **macOS**: `pkgbuild` and `productbuild` (optional `hdiutil` for dmg)  
- **Linux**: `dpkg-deb` for `.deb`, `rpmbuild` for `.rpm`  

---

## Detailed Build Steps

### 1. Library Validation
- Checks for required Python libraries  
- Prompts user to install missing libraries  
- Optional proxy prompt if network requires proxy  

### 2. OS Detection
- Detects current OS using `platform.system()`  
- Supported: `Windows`, `Darwin`, `Linux`  
- Aborts if OS unsupported  
- Detects AWS EC2 Linux environment and aborts  

### 3. Backup & Cleanup
- Previous `dist/`, `build/`, and `specs/` folders are backed up with timestamped names  
- Old `build.log` is removed to avoid confusion  

### 4. PyInstaller Executable Build
- Collects all project folders for `--add-data` flags  
- Constructs PyInstaller command with:  
  - `--onefile` / `--windowed`  
  - Hidden imports for all modules in `app/` and `core/`  
  - Add-data for assets, templates, and outputs  
- Runs PyInstaller with **progress bars**  
- Verifies executable exists in `dist/`  

### 5. OS-Specific Installer Creation
#### Windows (NSIS)
- Generates `.exe` installer with:  
  - Progress bars  
  - Desktop and Start menu shortcuts  
  - Version info embedded  
  - Uninstall functionality  

#### macOS (pkg/dmg)
- Generates `.pkg` installer using `pkgbuild`  
- Optionally generates `.dmg` for drag-and-drop install  
- Installs to `/Applications` by default  
- Embeds version info  

#### Linux (deb/rpm)
- Packages executable into `.deb` and `.rpm` formats  
- Requires properly structured package folder and spec/control files  

### 6. Post-Build Verification
- Confirms existence of executable and installers  
- Saves list of all installed files to `uninstall_record.json` for uninstall  

### 7. Logging & Progress
- **Log File**: `build.log` in project root  
- **Console Output**: optional verbose logging  
- **Progress Bars**: `tqdm` displays progress for scanning, building, and installer creation  

### 8. Uninstall Functionality
- Use `python build_agentic_ai.py uninstall` to remove all files tracked in `uninstall_record.json`  
- Ensures clean removal of executables, installers, and related resources  

---

## Advanced Options
- `DEBUG_MODE = True` enables PyInstaller debug build  
- Customize build paths with `DIST_DIR`, `BUILD_DIR`, `SPEC_DIR`  
- Modify included folders via `FOLDERS_TO_INCLUDE`  
- Embed build version and timestamp in logs and installer metadata  

---

## Example Outputs

**Windows**
- Executable: `dist/agentic_ai_builder.exe`  
- Installer: `dist/AgenticAI_Builder_Setup.exe`  

**macOS**
- Executable: `dist/agentic_ai_builder.app`  
- Installer: `dist/AgenticAI_Builder.pkg`  
- Optional dmg: `dist/AgenticAI_Builder.dmg`  

**Linux**
- Executable: `dist/agentic_ai_builder`  
- Packages: `dist/AgenticAI_Builder.deb`, `dist/AgenticAI_Builder.rpm`  

---

## Troubleshooting
- **Missing libraries**: Follow prompts to install or run `pip install <lib>`  
- **Unsupported OS**: Only Windows, macOS, and Linux are supported  
- **AWS EC2/Linux virtual environments**: Build will abort  
- **Build failures**: Check `build.log` for errors  
- **Installer failures**: Verify NSIS, pkgbuild, dpkg-deb, rpmbuild are installed  

---

## Developer Notes
- Maintain consistency by keeping all project folders listed in `FOLDERS_TO_INCLUDE`  
- Update hidden imports when adding new modules to `app/` or `core/`  
- Backups of previous builds are kept in the project root with timestamps  
- Post-build verification ensures production-ready installers and executables  

---

## License
This build script is part of the **AgenticAI Builder** project and follows the same licensing as the repository.
