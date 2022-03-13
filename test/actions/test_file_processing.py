"""Tests of the file readers and writers."""
from pathlib import Path

import click
import pytest

from generate_changelog.actions import file_processing

fixture_dir = Path(__file__).parent.parent / "fixtures"


def test_file_reading():
    """Should read the contents of a file."""
    example_path = fixture_dir / "example.txt"
    example_callable = lambda: example_path

    reader = file_processing.ReadFile(example_path)
    assert reader() == "This is example text in an example file.\n"

    reader = file_processing.ReadFile(example_callable)
    assert reader() == "This is example text in an example file.\n"


def test_reading_misssing_file(capsys):
    """Reading a missing file should generate an error."""
    missing_file_path = fixture_dir / "missing.txt"
    reader = file_processing.ReadFile(missing_file_path, create_if_missing=False)
    expected_err_msg = f"The file '{missing_file_path}' does not exist.\n"
    with pytest.raises(click.exceptions.Exit):
        reader()

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == expected_err_msg


def test_writing_file(tmp_path):
    """Writing a file should work!"""
    text = "This is example text in an example file.\n"
    output_path_1 = tmp_path / "output1.txt"
    output_path_2 = tmp_path / "output2.txt"
    output_callable = lambda: output_path_2

    writer = file_processing.WriteFile(output_path_1)
    writer(text)
    assert output_path_1.read_text() == text

    writer = file_processing.WriteFile(output_callable)
    writer(text)
    assert output_path_2.read_text() == text


def test_stdout(capsys):
    """Writing to stdout goes out."""
    text = "This is example text in an example file.\n"
    file_processing.stdout(text)
    captured = capsys.readouterr()
    assert captured.out == text + "\n"
    assert captured.err == ""


def test_incremental_file_insert(tmp_path):
    """Test inserting text into a file."""

    temp_file = tmp_path / "output.txt"
    test_file = fixture_dir / "pipeline_dag_test.md"
    temp_file.write_text(test_file.read_text())

    writer = file_processing.IncrementalFileInsert(str(temp_file), r"(?im)^## \d+\.\d+\.\d+")
    writer("This is new\n")

    assert temp_file.read_text() == "This is new\n\n## 0.0.1 (2022-01-01)\n\nThis stuff stays.\n"


def test_incremental_file_insert_missing_file(tmp_path):
    """Test inserting text into a file."""

    temp_file = tmp_path / "output.txt"

    writer = file_processing.IncrementalFileInsert(str(temp_file), r"(?im)^## \d+\.\d+\.\d+")
    writer("This is new\n")

    assert temp_file.read_text() == "This is new\n"
