from pathlib import Path


def ensure_file(file: Path) -> Path:
    """
    Ensure that the given file is a Path object.
    If the file does not exist, it will create an empty file.

    Args:
        file (str): The path to be converted.

    Returns:
        Path: A Path object representing the given file.
    """
    assert isinstance(file, Path), f"Expected Path type, got {type(file)}"

    if not file.exists():
        file.touch()
        print(f"File not found. Created `{file.name}` instead at `{file.parent}`")

    return file
