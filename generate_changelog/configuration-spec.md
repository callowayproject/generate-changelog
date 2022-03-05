## Actions

- action: (string) what runs python path to a function or known function 
- comment: (string) Description of the action
- id (optional string-id) A referencible id to refer to it 
- args: (optional list) Arguments to instantiate the function
- kwargs (optional dict) Keyword arguments to instantiate the function

## Built-in actions: 

- AppendString
- append_dot
- capitalize
- dataclass
- eval_if_callable
- FirstRegExMatch
- InsertAtRegEx
- noop
- Optional
- PrefixLines
- PrefixString
- prefix_caret
- ReadFile
- RegExCommand
- RegexSub
- SetDefault
- StrOrCallable
- Strip
- strip_spaces
- WrapParagraphs
- WriteFile

Python path. For example: "mymod.changelogging.func"

### `id`

Optional string value

Valid characters: A-Z, a-z, 0-9, -, _

### `args`

Optional list of arguments to pass to a callable instance function.

Arguments can be references to variables or the result of a previous action

### `kwargs`

Optional mapping of key-values to pass to a callable instance function.

Values can be references to variables or the result of a previous action

## Metadata collecting functions

There are two special values for ``kwargs``: `save_commit_metadata` and `save_version_metadata`.

These values are swapped with a callable function that stores keyword arguments into metadata for either the commit or the verson.

For example:

```yaml
body_pipeline:
- action: "ParseTrailers"
- comment: "Parse the trailers into metadata."
- kwargs: 
    commit_metadata: "save_commit_metadata"
```

internally calls ``self.commit_metadata(trailers=trailers)`` which adds a "trailer" key to the commit's metadata property in the template context.
