"""Testing pipelines and actions."""
from pathlib import Path

from generate_changelog import pipeline

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_action_builtin():
    """Actions run correctly."""
    action = pipeline.Action("noop")
    assert action.run({}, "foo") == "foo"


def test_action_import():
    """Actions run correctly."""
    action = pipeline.Action("generate_changelog.actions.text_processing.capitalize")
    assert action.run({}, "foo") == "Foo"


def test_action_args_kwargs():
    """Test actions with args and kwargs."""
    action = pipeline.Action("PrefixLines", args=("  ",), kwargs={"first_line": "- "})
    assert action.run({}, "foo\nbar") == "- foo\n  bar\n"


def test_pipeline_factory():
    """A pipeline factory should output a valid pipeline."""
    actions = [
        {"action": "strip_spaces"},
        {
            "action": "Strip",
            "comment": "Get rid of any periods so we don't get double periods",
            "kwargs": {"chars": "."},
        },
        {"action": "SetDefault", "args": ["no commit message"]},
        {"action": "capitalize"},
        {"action": "append_dot"},
    ]
    pipe = pipeline.pipeline_factory(actions)
    assert pipe.run("  this is a bad idea.   ") == "This is a bad idea."
    assert pipe.run() == "No commit message."


def test_pipelline_dag():
    """Make sure a typical DAG from YAML executes properly."""
    changelog_path = FIXTURES_DIR / "pipeline_dag_test.md"
    actions = [
        {
            "action": "AppendString",
            "comment": "Append the changelog from the last release heading on to the generated changelog",
            "kwargs": {
                "postfix": [
                    {
                        "action": "ReadFile",
                        "comment": "Read the existing changelog",
                        "kwargs": {"filename": str(changelog_path)},
                    },
                    {
                        "action": "Slice",
                        "comment": "Return just part of the file",
                        "kwargs": {
                            "start": [
                                {
                                    "action": "ReadFile",
                                    "comment": "Read the existing changelog",
                                    "kwargs": {"filename": str(changelog_path)},
                                },
                                {
                                    "action": "FirstRegExMatchPosition",
                                    "comment": "Find the position of the last release heading",
                                    "kwargs": {
                                        "pattern": r"(?im)^## [0-9]+\.[0-9]+(?:\.[0-9]+)?\s+\([0-9]+-[0-9]{2}-[0-9]{2}\)$"
                                    },
                                },
                            ]
                        },
                    },
                ]
            },
        },
    ]
    pipe = pipeline.pipeline_factory(actions)
    input_text = "This is new\n"
    expected = input_text + "## 0.0.1 (2022-01-01)\n\nThis stuff stays.\n"
    assert pipe.run(input_text) == expected
