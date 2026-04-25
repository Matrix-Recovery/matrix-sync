#!/usr/bin/env python3
import os
import re
import sys
import shutil
import tempfile
import subprocess
import argparse
from pathlib import Path

# --- ANSI Colors for CLI ---
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def log(msg, color=RESET):
    print(f"{color}{msg}{RESET}")

def parse_device_tree(directory):
    """Scans makefiles to find vendor, codename, and flavor."""
    vendor, codename, flavor = None, None, "matrix"
    
    # Priority 1: Scan for AndroidProducts.mk
    for mk in Path(directory).rglob("AndroidProducts.mk"):
        content = mk.read_text(errors='ignore')
        # Look for PRODUCT_MAKEFILES := $(LOCAL_DIR)/matrix_sweet.mk
        match = re.search(r'\$\(LOCAL_DIR\)/([a-zA-Z0-9_-]+)\.mk', content)
        if match:
            full_name = match.group(1)
            if "_" in full_name:
                flavor, codename = full_name.split("_", 1)
            break

    # Priority 2: Deep scan all .mk files for variables
    for mk in Path(directory).rglob("*.mk"):
        content = mk.read_text(errors='ignore')
        if not codename:
            m = re.search(r'PRODUCT_DEVICE\s*[:]?=\s*([a-zA-Z0-9_-]+)', content)
            if m: codename = m.group(1)
        if not vendor:
            m = re.search(r'PRODUCT_(?:MANUFACTURER|BRAND)\s*[:]?=\s*([a-zA-Z0-9_-]+)', content)
            if m: vendor = m.group(1)
            
    return vendor, codename, flavor

def main():
    parser = argparse.ArgumentParser(description="Matrix Recovery Device Tree Cloner")
    parser.add_argument("url", help="Git URL of the device tree")
    parser.add_argument("-p", "--path", default=".", help="Workspace path (default: current dir)")
    parser.add_argument("-b", "--branch", help="Git branch to clone")
    args = parser.parse_args()

    workspace = os.path.abspath(os.path.expanduser(args.path))
    
    # 1. Create Temp Directory
    tmp_dir = tempfile.mkdtemp(prefix="matrix_dt_")
    log(f"[*] Created temporary workspace: {tmp_dir}", BLUE)

    # 2. Git Clone
    clone_cmd = ["git", "clone", "--depth", "1"]
    if args.branch:
        clone_cmd += ["-b", args.branch]
    clone_cmd += [args.url, tmp_dir]

    log(f"[*] Cloning device tree from {args.url}...", YELLOW)
    try:
        subprocess.check_call(clone_cmd)
    except subprocess.CalledProcessError:
        log("[!] Git clone failed!", RED)
        shutil.rmtree(tmp_dir)
        sys.exit(1)

    # 3. Auto-Detect
    log("[*] Analyzing device tree structure...", YELLOW)
    vendor, codename, flavor = parse_device_tree(tmp_dir)

    # 4. Manual Fallback
    if not vendor or not codename:
        log("[!] Auto-detection failed or incomplete.", RED)
        if not vendor: vendor = input("    Enter Vendor Name (e.g. samsung): ").strip()
        if not codename: codename = input("    Enter Codename (e.g. a12s): ").strip()

    # 5. Final Path Resolution
    # Path: <workspace>/device/<vendor>/<codename>
    final_path = os.path.join(workspace, "device", vendor.lower(), codename.lower())
    
    log(f"[+] Detected Vendor: {vendor}", GREEN)
    log(f"[+] Detected Codename: {codename}", GREEN)
    log(f"[+] Final Path: {final_path}", BLUE)

    # 6. Move to Workspace
    if os.path.exists(final_path):
        confirm = input(f"{YELLOW}[?] Target path exists. Overwrite? (y/N): {RESET}").lower()
        if confirm == 'y':
            shutil.rmtree(final_path)
        else:
            log("[!] Operation aborted by user.", RED)
            shutil.rmtree(tmp_dir)
            sys.exit(0)

    try:
        os.makedirs(os.path.dirname(final_path), exist_ok=True)
        shutil.move(tmp_dir, final_path)
        log(f"\n{GREEN}✔ Successfully set up device/{vendor}/{codename}{RESET}")
        log(f"{GREEN}👉 To build: lunch {flavor}_{codename}-eng && mka recoveryimage{RESET}")
    except Exception as e:
        log(f"[!] Error moving files: {e}", RED)
        if os.path.exists(tmp_dir): shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    main()
