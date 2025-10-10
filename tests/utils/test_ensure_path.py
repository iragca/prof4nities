from src.utils import ensure_path
from pathlib import Path


def test_ensure_path():
    # Given a non-existing directory path
    new_dir = Path().resolve() / "new_directory"

    # When ensure_path is called
    result_path = ensure_path(new_dir)

    assert isinstance(result_path, Path)
    # Then the directory should be created
    assert result_path.exists()
    assert result_path.is_dir()
    assert result_path == new_dir

    # Cleanup
    new_dir.rmdir()
