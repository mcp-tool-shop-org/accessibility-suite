import os
import sys
import re

# Paths relative to the monorepo root
HANDBOOKS_DIR = "docs/handbooks"
REQUIRED_HANDBOOKS = [
    "A11Y-LINT.md",
    "A11Y-CI.md",
    "A11Y-MCP-TOOLS.md",
    "A11Y-ASSIST.md",
    "A11Y-EVIDENCE-ENGINE.md",
    "A11Y-DEMO-SITE.md",
    "ALLY-DEMO-PYTHON.md",
    "CURSORASSIST.md",
]
REDIRECT_REPOS = [
    "../a11y-lint",
    "../a11y-ci",
    "../a11y-assist",
    "../a11y-mcp-tools",
    "../a11y-evidence-engine",
    "../a11y-demo-site",
    "../ally-demo-python",
]

def check_file_exists(path):
    if not os.path.exists(path):
        print(f"FAILED: File not found: {path}")
        return False
    return True

def check_content(path, pattern, description):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        if not re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            print(f"FAILED: {path} missing {description} (Pattern: {pattern})")
            return False
    return True

def verify_handbooks():
    success = True
    print("Verifying Handbooks...")

    # 1. Check Index
    index_path = os.path.join(HANDBOOKS_DIR, "README.md")
    if check_file_exists(index_path):
        print(f"OK: {index_path} exists")
        # Check for links to required handbooks
        for hb in REQUIRED_HANDBOOKS:
            if not check_content(index_path, re.escape(hb), f"link to {hb}"):
                success = False
            else:
                print(f"OK: Index links to {hb}")
    else:
        success = False

    # 2. Check Tool Handbooks for Quickstart
    for hb in REQUIRED_HANDBOOKS:
        path = os.path.join(HANDBOOKS_DIR, hb)
        if check_file_exists(path):
            if not check_content(path, r"^## Quickstart", "Quickstart section"):
                success = False
            else:
                print(f"OK: {hb} has Quickstart")
        else:
            success = False

    # 3. Check Redirects (if repos exist in workspace)
    print("\nVerifying Redirects...")
    for repo_path in REDIRECT_REPOS:
        handbook_path = os.path.join(repo_path, "HANDBOOK.md")
        # Resolve relative to script execution location (assuming repo root)
        # Note: script will be run from repo root
        if os.path.exists(repo_path):
            if check_file_exists(handbook_path):
                 # Check for the correct redirect link
                 expected_link = "mcp-tool-shop-org/accessibility-suite"
                 if not check_content(handbook_path, re.escape(expected_link), "redirect link to monorepo"):
                     success = False
                 else:
                     print(f"OK: {repo_path} redirects correctly")
            else:
                print(f"WARNING: {repo_path} exists but HANDBOOK.md missing")
                # Not necessarily a failure if we haven't migrated everything, but good to know
        else:
            print(f"SKIP: Repo {repo_path} not found in workspace (external?)")

    return success

if __name__ == "__main__":
    # Ensure current directory is accessible
    # Expected execution: python scripts/verify_handbooks.py from repo root
    if not verify_handbooks():
        sys.exit(1)
    print("\nSUCCESS: All handbook checks passed.")
    sys.exit(0)
