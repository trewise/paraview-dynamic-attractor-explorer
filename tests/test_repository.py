from pathlib import Path


def test_required_directories_exist():
    required = [
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
    for path in required:
        assert Path(path).exists(), path


def test_required_project_files_exist():
    required = [
        "README.md",
        "PROJECT_STATUS.md",
        "PROJECT_LOG.md",
        ".github/workflows/python-tests.yml",
    ]
    for path in required:
        assert Path(path).exists(), path


def test_paraview_state_files_exist():
    assert len(list(Path("paraview/state_files").glob("*.pvsm"))) >= 3


def test_portfolio_screenshots_exist():
    assert len(list(Path("portfolio/screenshots").glob("*.png"))) >= 3


def test_portfolio_videos_exist():
    assert len(list(Path("portfolio/videos").glob("*.mp4"))) >= 3


def test_no_python_cache_tracked_artifacts_required():
    assert not Path(".pytest_cache").exists()
