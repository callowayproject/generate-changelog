"""Shell commands for processing."""
from typing import Optional

import os
import subprocess
import tempfile

from generate_changelog.actions import register_builtin


@register_builtin
def bash(script: str, environment: Optional[dict] = None):
    """Runs command-line programs using the bash's shell."""
    handle, script_path = tempfile.mkstemp(suffix=".sh")
    try:
        with os.fdopen(handle, "w") as f:
            f.write(script)

        command = ["bash", "--noprofile", "--norc", "-eo", "pipefail", script_path]

        result = subprocess.run(
            command,
            env=environment,
            encoding="utf-8",
            capture_output=True,
        )
    finally:
        if script_path:
            os.remove(script_path)

    return result.stdout if result else ""
