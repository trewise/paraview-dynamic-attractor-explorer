from pathlib import Path

required_dirs = [
    "src",
    "scripts",
    "tools",
    "tests",
    "docs",
    "docs/roadmap",
    "datasets/attractors",
    "paraview/python_scripts",
    "paraview/state_files",
    "paraview/camera_paths",
    "portfolio/screenshots",
    "portfolio/videos",
]

required_files = [
    "README.md",
    "PROJECT_STATUS.md",
    "PROJECT_LOG.md",
    ".github/workflows/python-tests.yml",
]

missing = []

for item in required_dirs + required_files:
    if not Path(item).exists():
        missing.append(item)

if missing:
    print("Missing required project items:")
    for item in missing:
        print(f"- {item}")
    raise SystemExit(1)

print("Repository structure validation passed.")
