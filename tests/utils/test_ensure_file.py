import pytest
from pathlib import Path
from src.utils.ensure_file import ensure_file


def test_ensure_file_creates_file(tmp_path, capsys):
    file_path = tmp_path / "testfile.txt"
    assert not file_path.exists()
    result = ensure_file(file_path)
    assert file_path.exists()
    assert result == file_path
    captured = capsys.readouterr()
    assert (
        f"File not found. Created `{file_path.name}` instead at `{file_path.parent}`"
        in captured.out
    )


def test_ensure_file_returns_existing_file(tmp_path, capsys):
    file_path = tmp_path / "existing.txt"
    file_path.write_text("hello")
    assert file_path.exists()
    result = ensure_file(file_path)
    assert result == file_path
    captured = capsys.readouterr()
    assert "File not found" not in captured.out


def test_ensure_file_raises_on_non_path():
    with pytest.raises(AssertionError) as excinfo:
        ensure_file("not_a_path")
    assert "Expected Path type" in str(excinfo.value)
