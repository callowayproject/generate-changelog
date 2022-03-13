"""Basic shell commands."""
from generate_changelog.actions import shell


def test_shell():
    """Running shell scripts."""
    env = {
        "FOO": "bar",
    }
    sh_script = shell.bash("echo ${FOO}", environment=env)
    assert sh_script == "bar\n"
