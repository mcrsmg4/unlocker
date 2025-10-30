# macOS Unlocker V3.0 for VMware Workstation
===========================================

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> ⚠️ **Note:** This version has **not been tested on VMware Workstation 16 or 17**. Use with caution on these versions.

---

## 📌 Read This First

**WINDOWS USERS:**  
Get the tool from the **Releases** section. You will get a bundled Python distribution that avoids virus warnings and “Python not found” errors.  

**LINUX USERS:**  
No bundled Python is provided. Make sure you have **Python 3.0+** installed.  
If you get errors like *"Python not supported"* but Python is installed, edit `lnx-install.sh` and replace `python xxxxxxx.py` with `python3.7 xxxxxxx.py` (or `python3` for other versions).  

---

## ⚠️ Important
Always uninstall the previous version of the Unlocker before using a new version. Failure to do so could render VMware unusable.

---

## 1. Introduction
Unlocker 3 is designed for VMware Workstation 11-15 and Player 7-15.  

If you are using an earlier product, continue using Unlocker 1.

Version 3 has been tested against:

* Workstation 11/12/14/15 on Windows and Linux  
* Workstation Player 7/12/14/15 on Windows and Linux

### What it does
* Fix `vmware-vmx` and derivatives to allow macOS to boot  
* Fix `vmwarebase.dll` or `.so` to allow Apple to be selected during VM creation  
* Download the latest VMware Tools for macOS  

> Not all products recognize `darwin.iso` via the “Install Tools” menu. You may need to mount it manually.  
> Make sure VMware is **not running** and all background guests are shutdown.

The code is written in Python.

---

## 2. Prerequisites
* **Linux:** Python 2.7+ is required. Most distros ship with a compatible version.  
* **Windows:** Bundled Python script (via PyInstaller) requires **no Python installation**.

---

## 3. Limitations
* VMware Player or Workstation on Windows may produce a core dump on new VM creation.  
* Latest Linux products are OK and do **not** show this problem.

### ⚠️ Workarounds
1. Change the VM to **Hardware Version 10** (no performance impact).  
2. Edit the VMX file and add:
```text
smc.version = "0"

4. Windows Usage

Run cmd.exe as Administrator or right-click the command file and select Run as administrator.

win-install.cmd – patches VMware

win-uninstall.cmd – restores VMware

win-update-tools.cmd – retrieves the latest macOS guest tools

5. Linux Usage

Run scripts as root or with sudo. Ensure execute permissions:
chmod +x lnx-install.sh lnx-uninstall.sh lnx-update-tools.sh

6. Thanks

Special thanks to:

Pablo Projects – original script

Zenith432 – C++ unlocker

Mac Son of Knife (MSoK) – testing and support

Sam B – ESXi patching, Python 3 modifications, debugging

History

27/09/18 – 3.0.0 – First release

02/10/18 – 3.0.1 – Fixed gettools.py for Python 3, download darwinPre15.iso

10/10/18 – 3.0.2 – Fixed false positives in Windows executables, allow Python 2 and 3 in Bash scripts

© 2011-2018 Dave Parsons, (updated to Python 3 and modern standards by https://github.com/mcrsmg4 
