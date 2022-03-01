"""Testing pipelines and actions."""

from clgen import pipeline


def test_action_builtin():
    """Actions run correctly."""
    action = pipeline.Action("noop")
    assert action.run({}, "foo") == "foo"


def test_action_import():
    """Actions run correctly."""
    action = pipeline.Action("clgen.processors.text_processing.capitalize")
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
