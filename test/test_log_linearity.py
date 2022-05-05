from pathlib import Path

from git import Actor

from generate_changelog import templating
from generate_changelog.configuration import get_default_config

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_tags_on_multiple_branches(bare_git_repo, capsys):
    """
    Make a bunch of default commits to a temporary bare git repo.

    Target tree:

    $ git log --all --pretty=tformat:%s\ %d --graph
    *   Merge branch 'develop' into master (HEAD -> master, tag: 0.0.4)
    |\
    | * new: some new commit
    | * fix: hotfix on master (tag: 0.0.3)
    * | 'new: second commit on develop branch' (develop)
    * | new: first commit on develop branch (tag: 0.0.2)
    |/
    * new: first commit (tag: 0.0.1)
    """
    # Branch: master
    idx = bare_git_repo.index
    idx.commit(
        message="commit 1 on master", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 10:00:00"
    )
    bare_git_repo.create_tag("0.0.1")

    # Branch: develop
    develop = bare_git_repo.create_head("develop", "HEAD")
    bare_git_repo.head.reference = develop
    assert not bare_git_repo.head.is_detached

    idx.commit(
        message="commit 2 on develop",
        committer=Actor("Alice", "alice@example.com"),
        commit_date="2022-01-02 11:00:00",
    )
    bare_git_repo.create_tag("0.0.2")
    idx.commit(
        message="commit 3 on develop",
        committer=Actor("Charly", "charly@example.com"),
        commit_date="2022-01-03 12:00:00",
    )

    # Branch: master
    bare_git_repo.head.reference = bare_git_repo.heads.master
    idx.commit(
        message="commit 4 on master",
        committer=Actor("Bob", "bob@example.com"),
        commit_date="2022-01-04 13:00:00",
    )
    bare_git_repo.create_tag("0.0.3")
    idx.commit(
        message="commit 5 on master",
        committer=Actor("Bob", "bob@example.com"),
        commit_date="2022-01-05 13:00:00",
    )

    master = bare_git_repo.heads.master  # right-hand side is ahead of us, in the future
    merge_base = bare_git_repo.merge_base(develop, master)  # allows for a three-way merge
    idx.merge_tree(master, base=merge_base)  # write the merge result into index
    idx.commit("Merge branch 'develop' into master", parent_commits=(develop.commit, master.commit))

    bare_git_repo.create_tag("0.0.4")

    # print(bare_git_repo.git.log(all=True, pretty=r"tformat:%s %d", graph=True))

    changelog_config = get_default_config()
    changelog_config.update_from_file(FIXTURES_DIR / "std-out-config.yaml")
    context = templating.get_context_from_tags(bare_git_repo, changelog_config)
    assert len(context) == 5
    unreleased = context[0]
    ver004 = context[1]
    ver003 = context[2]
    ver002 = context[3]
    ver001 = context[4]
    assert len(unreleased.grouped_commits) == 0
    assert len(ver004.grouped_commits[0].commits) == 3
    assert ver004.grouped_commits[0].commits[0].summary == "Commit 5 on master."
    assert ver004.grouped_commits[0].commits[1].summary == "Commit 3 on develop."
    assert ver004.grouped_commits[0].commits[2].summary == "Commit 2 on develop."
    assert len(ver003.grouped_commits[0].commits) == 1
    assert ver003.grouped_commits[0].commits[0].summary == "Commit 4 on master."
    assert len(ver002.grouped_commits[0].commits) == 1
    assert ver002.grouped_commits[0].commits[0].summary == "Commit 2 on develop."
    assert len(ver001.grouped_commits[0].commits) == 1
    assert ver001.grouped_commits[0].commits[0].summary == "Commit 1 on master."
