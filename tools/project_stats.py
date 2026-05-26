from pathlib import Path

IGNORE = {".git", ".venv", "__pycache__", ".pytest_cache"}

def keep(path: Path) -> bool:
    return not any(part in IGNORE for part in path.parts)

root = Path(".")

py_files = [p for p in root.rglob("*.py") if keep(p)]
png_files = [p for p in root.rglob("*.png") if keep(p)]
gif_files = [p for p in root.rglob("*.gif") if keep(p)]
mp4_files = [p for p in root.rglob("*.mp4") if keep(p)]
pvsm_files = [p for p in root.rglob("*.pvsm") if keep(p)]

print("===== PROJECT STATS =====")
print(f"Python files : {len(py_files)}")
print(f"PVSM files   : {len(pvsm_files)}")
print(f"PNG images   : {len(png_files)}")
print(f"GIF files    : {len(gif_files)}")
print(f"MP4 videos   : {len(mp4_files)}")
