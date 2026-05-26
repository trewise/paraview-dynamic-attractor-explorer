from pathlib import Path

required_paths = [
    "README.md",
    "QUICKSTART.md",
    "requirements.txt",
    "src",
    "scripts",
    "data",
    "paraview",
    "docs",
]

missing = [p for p in required_paths if not Path(p).exists()]

if missing:
    print("Missing required paths:")
    for p in missing:
        print(f"- {p}")
    raise SystemExit(1)

print("Repository structure validation passed.")
