# Metadata Actions

## ParseTrailers

### Arguments

commit_metadata

In Git, trailers are key-value pairs written inside of commit messages that, make things like issue references programmatically accessible. For example, the following commit message:

```
Awesome new feature

Some details about this commit

Closes: #1234
```

The last line is an example for a trailer. It consists of a token (`Closes`), a separator (`:`), and a value (`#1234`).



This action will convert the above commit message to:

```
Awesome new feature

Some details about this commit
```

And add set `metadata.trailers.Closes` to `#1234` for easy reference in the template.

More info

https://git.wiki.kernel.org/index.php/CommitMessageConventions

https://lore.kernel.org/git/60ad75ac7ffca_2ae08208b@natae.notmuch/
