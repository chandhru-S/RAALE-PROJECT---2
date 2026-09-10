#!/usr/bin/env python3
"""
Portable Git Downloader & GitHub Pusher Script for ORRS Project.
Downloads MinGit portable binary without requiring Windows admin elevation,
initializes repository, stages project files, commits, and pushes to remote.
"""

import os
import sys
import subprocess
import urllib.request
import zipfile

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIT_BIN_DIR = os.path.join(PROJECT_DIR, ".git_bin")
GIT_EXE = os.path.join(GIT_BIN_DIR, "cmd", "git.exe")

MINGIT_URL = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/MinGit-2.43.0-64-bit.zip"
REMOTE_URL = "https://github.com/chandhrusubramani11-hue/hospital.git"

def ensure_git():
    if os.path.exists(GIT_EXE):
        print(f"Portable Git already downloaded at {GIT_EXE}")
        return GIT_EXE

    os.makedirs(GIT_BIN_DIR, exist_ok=True)
    zip_path = os.path.join(GIT_BIN_DIR, "mingit.zip")

    print(f"Downloading Portable MinGit from {MINGIT_URL}...")
    req = urllib.request.Request(MINGIT_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp, open(zip_path, 'wb') as out_file:
        out_file.write(resp.read())
    print("Download completed. Extracting MinGit...")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(GIT_BIN_DIR)

    if os.path.exists(zip_path):
        os.remove(zip_path)

    print(f"MinGit successfully extracted to {GIT_BIN_DIR}")
    return GIT_EXE

def run_git_cmd(git_path, args):
    cmd = [git_path] + args
    print(f"Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=PROJECT_DIR, text=True, capture_output=True)
    print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)
    return res.returncode

def main():
    git_path = ensure_git()

    # 1. Init
    run_git_cmd(git_path, ["init"])

    # 2. Configure user details if not set
    run_git_cmd(git_path, ["config", "user.name", "ORRS Developer"])
    run_git_cmd(git_path, ["config", "user.email", "orrs-dev@hospital.local"])

    # 3. Add files
    run_git_cmd(git_path, ["add", "."])

    # 4. Commit
    run_git_cmd(git_path, ["commit", "-m", "feat: complete Operating Room Readiness Synchroniser (ORRS) full-stack project"])

    # 5. Branch
    run_git_cmd(git_path, ["branch", "-M", "main"])

    # 6. Remote
    run_git_cmd(git_path, ["remote", "remove", "origin"])
    run_git_cmd(git_path, ["remote", "add", "origin", REMOTE_URL])

    # 7. Push
    print("\nPushing to GitHub repository...")
    code = run_git_cmd(git_path, ["push", "-u", "origin", "main"])

    if code == 0:
        print(f"\n✅ Project successfully pushed to {REMOTE_URL}")
    else:
        print("\nNotice: Push failed (likely requires GitHub personal access token authentication or SSH key).")

if __name__ == "__main__":
    main()
