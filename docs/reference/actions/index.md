# Actions and Pipelines


## Introduction

Pipelines and actions are modeled after continuous integration systems such as GitHub Actions and Azure Pipelines, but simplified. A pipeline is a list of actions and actions are functions. It is easy to provide and specify custom actions.

## Actions

Actions are callables that will accept a string and typically return a string.

Two types:

- simple
- configurable

### Simple actions

A simple action is a function that accepts an argument and returns a value. Typically, both the argument and the return value are strings.

### Configurable Actions

A configurable action is a class whose instances are callable. You can pass positional or keyword arguments to the class. The __init__ method will store the arguments for use when the instance is called.

The postional and keyword argument values can be:

- Scalar values
- Template strings
- Pipelines or actions

### Specifying actions

A simple map in YAML. 

`action` **Required.** A python path to a function or name of a built-in action.

`id` An optional identifier for the results of this action in the pipeline context. While the pipeline passes the result of each action to the input of the next, subsequent actions can also retrieve the result of any previous action using this `id` or `result_<x>` where `<x>` is the 0-based index of the action.

`comment` A useful description of what this step does for the pipeline.

`args` A list of values to pass to the action as positional arguments to a configurable action.

`kwargs` A mapping of key-value pairs that are passed to the action to a configurable action.

### Metadata callbacks

Set the value of an argument to `save_commit_metadata` or `save_version_metadata`. Those values will be replaced with functions whose keyword arguments are aggregated into the commit or version's metadata, respectively.

## Pipelines

Pipelines are a list of one or more actions. The pipeline may be started with a string, which is passed as an argument to the first action in the pipeline.

### Context
