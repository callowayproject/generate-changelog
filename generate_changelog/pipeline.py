"""Simple pipeline workflow processing."""
from typing import Any, Callable, Optional, Union

from dataclasses import dataclass, field

from generate_changelog.configuration import StrOrCallable
from generate_changelog.processors import BUILT_INS, load_builtins

load_builtins()


def noop_func(**kwargs):
    """A function that does nothing when called."""
    pass


class Pipeline:
    """A collection of actions to perform on an input."""

    actions: tuple
    """The actions to perform on the input."""

    context: dict
    """The current state of the pipeline initialized by keyword arguments."""

    def __init__(
        self,
        actions: Union[list, tuple],
        **kwargs,
    ):
        self.actions = tuple(actions)
        self.context = kwargs.copy()

    def run(self, input_value: Optional[str] = None):
        """Run the pipeline using input_value as the starting point."""
        result = current_input = input_value
        for step, action in enumerate(self.actions):
            result = action.run(self.context.copy(), current_input)
            step_key = action.id or f"result_{step}"
            self.context[step_key] = current_input = result
        return result


class Action:
    """An action to perform in a pipeline."""

    _action_str: str
    """A python path to a function or name of a built-in action."""

    id: Optional[str] = None
    """Identifier for the action."""

    _args: list
    """Arguments to instantiate the action."""

    _kwargs: dict
    """Keyword arguments to instantiate the action."""

    commit_metadata_func: Optional[Callable]
    """Function the action can call to set metadata about the commit."""

    version_metadata_func: Optional[Callable]
    """Function the action can call to set metadata about the version a commit belongs to."""

    def __init__(
        self,
        action: str,
        id_: Optional[str] = None,
        args: Optional[Union[list, tuple]] = None,
        kwargs: Optional[dict] = None,
        commit_metadata_func: Optional[Callable] = None,
        version_metadata_func: Optional[Callable] = None,
    ):
        self._action_str = action
        self.id = id_
        self._args = args or []
        self._kwargs = kwargs or {}
        self.commit_metadata_func = commit_metadata_func or noop_func
        self.version_metadata_func = version_metadata_func or noop_func

        if action in BUILT_INS:
            self.action_function = BUILT_INS[action]
        else:
            self.action_function = import_function(action)

    def run(self, context: dict, input_value: str) -> str:
        """Perform the action on the input."""
        from generate_changelog.templating import pipeline_env

        # render string args, and kwarg-values using jinja2
        new_args = [
            pipeline_env.from_string(arg, globals=context).render() if isinstance(arg, str) else arg
            for arg in self._args
        ]

        new_kwargs = {
            key: pipeline_env.from_string(val, globals=context).render() if isinstance(val, str) else val
            for key, val in self._kwargs.items()
        }

        # replace any kwarg values requesting a metadata function with the real thing
        for key, val in new_kwargs.items():
            if val == "save_commit_metadata":
                new_kwargs[key] = self.commit_metadata_func
            elif val == "save_version_metadata":
                new_kwargs[key] = self.version_metadata_func

        # passed in arguments or keyword arguments indicate we must instantiate the action_function
        if new_args or new_kwargs:
            action_function = self.action_function(*new_args, **new_kwargs)
        else:
            action_function = self.action_function

        return action_function(input_value)


def import_function(function_path: str) -> Any:
    """Import a function from a dotted path."""
    from importlib import import_module

    bits = function_path.split(".")
    function_name = bits[-1]
    module = import_module(".".join(bits[:-1]))
    return getattr(module, function_name)


def pipeline_factory(
    action_list: list,
    commit_metadata_func: Optional[Callable] = None,
    version_metadata_func: Optional[Callable] = None,
    **kwargs,
) -> Pipeline:
    """Create a Pipeline from a list of configured actions."""
    actions = [
        Action(
            action=a["action"],
            id_=a.get("id"),
            args=a.get("args"),
            kwargs=a.get("kwargs"),
            commit_metadata_func=commit_metadata_func,
            version_metadata_func=version_metadata_func,
        )
        for a in action_list
    ]
    return Pipeline(actions=actions, **kwargs)
