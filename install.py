#!/usr/bin/env python3
"""
macOS Unlocker V3.0 - Universal Installer
------------------------------------------
This script simplifies the unlocker setup for both Linux and Windows.

Usage:
    python3 install.py [install|uninstall|update]

Features:
- Detects OS (Linux/Windows)
- Detects VMware Workstation version and warns if untested
- Auto-downloads latest macOS VMware Tools (darwin.iso)
- Runs installer/uninstaller/update scripts
- Checks Python 3+
- Verifies VMware is installed

(c) 2011-2018 Dave Parsons
Updated 2025 by MCRSMG4, for Python 3, and serverside stuff for Darwin Tools
"""

import os
import sys
import platform
import subprocess
import shutil
import re
import urllib.request

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
DARWIN_ISO_URL = "https://github.com/your-repo/macOS-VMware-Tools/raw/main/darwin.iso"
TOOLS_DIR = "tools"

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def check_python_version():
    if sys.version_info < (3, 0):
        sys.exit("❌ Python 3.0 or higher is required. Exiting.")
    print(f"✅ Python version OK: {platform.python_version()}")

def check_vmware_installed():
    system = platform.system()
    vm_version = None

    if system == "Linux":
        if shutil.which("vmware") or os.path.exists("/usr/bin/vmware"):
            result = subprocess.run(["vmware", "-v"], capture_output=True, text=True)
            vm_version = parse_vmware_version(result.stdout)
            print("✅ VMware Workstation detected.")
        else:
            sys.exit("❌ VMware Workstation not found. Install it before running the unlocker.")

    elif system == "Windows":
        vmware_path = os.path.expandvars(r"%ProgramFiles(x86)%\VMware\VMware Workstation\vmware.exe")
        if os.path.exists(vmware_path):
            result = subprocess.run([vmware_path, "-v"], capture_output=True, text=True, shell=True)
            vm_version = parse_vmware_version(result.stdout)
            print("✅ VMware Workstation detected.")
        else:
            sys.exit("❌ VMware Workstation not found. Please install it first.")

    else:
        sys.exit("❌ Unsupported operating system.")

    # Warn for untested versions
    if vm_version:
        major = int(vm_version.split('.')[0])
        print(f"ℹ️ Detected VMware Workstation version: {vm_version}")
        if major > 15:
            print("⚠️ Warning: This Unlocker has NOT been tested on VMware Workstation 16 or 17.")

    return system

def parse_vmware_version(output):
    match = re.search(r'(\d+\.\d+(?:\.\d+)?)', output)
    return match.group(1) if match else None

def run_script(command):
    """Runs a shell or batch script with elevated privileges where possible."""
    try:
        print(f"⚙️ Running: {command}")
        subprocess.run(command, shell=True, check=True)
        print("✅ Operation completed successfully.")
    except subprocess.CalledProcessError:
        sys.exit("❌ The command failed. Check permissions or script errors.")

def download_tools():
    """Downloads darwin.iso if not already present."""
    os.makedirs(TOOLS_DIR, exist_ok=True)
    iso_path = os.path.join(TOOLS_DIR, "darwin.iso")
    if os.path.exists(iso_path):
        print(f"ℹ️ darwin.iso already exists: {iso_path}")
        return iso_path

    print(f"⬇️ Downloading darwin.iso from {DARWIN_ISO_URL} ...")
    try:
        urllib.request.urlretrieve(DARWIN_ISO_URL, iso_path)
        print(f"✅ Download complete: {iso_path}")
    except Exception as e:
        sys.exit(f"❌ Failed to download darwin.iso: {e}")
    return iso_path

# ----------------------------------------------------------------------
# Main logic
# ----------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 install.py [install|uninstall|update]")
        sys.exit(1)

    action = sys.argv[1].lower()
    check_python_version()
    system = check_vmware_installed()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Automatically download VMware Tools if installing or updating
    if action in ("install", "update"):
        download_tools()

    # Linux
    if system == "Linux":
        scripts = {
            "install": "lnx-install.sh",
            "uninstall": "lnx-uninstall.sh",
            "update": "lnx-update-tools.sh"
        }

        script = scripts.get(action)
        if not script:
            sys.exit("❌ Unknown action. Use install, uninstall, or update.")

        full_path = os.path.join(script_dir, script)
        if not os.path.exists(full_path):
            sys.exit(f"❌ Script not found: {full_path}")

        # Ensure executable permissions
        subprocess.run(["chmod", "+x", full_path], check=False)
        run_script(f"sudo {full_path}")

    # Windows
    elif system == "Windows":
        scripts = {
            "install": "win-install.cmd",
            "uninstall": "win-uninstall.cmd",
            "update": "win-update-tools.cmd"
        }

        script = scripts.get(action)
        if not script:
            sys.exit("❌ Unknown action. Use install, uninstall, or update.")

        full_path = os.path.join(script_dir, script)
        if not os.path.exists(full_path):
            sys.exit(f"❌ Script not found: {full_path}")

        # Run as administrator
        run_script(f'cmd /c "{full_path}"')

    else:
        sys.exit("❌ Unsupported OS.")

# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
