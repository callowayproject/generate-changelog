import textwrap
from pathlib import Path

import pytest
from git import Actor

from generate_changelog import configuration, templating

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def conv_commit_repo(bare_git_repo, faker):
    """Make a bunch of default commits to a temporary bare git repo."""
    idx = bare_git_repo.index
    idx.commit(
        message="feat: first implementation of telnet server",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-04-25 05:54:00",
    )
    idx.commit(
        message="chore(release): 1.0.0",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-04-25 05:54:00",
    )
    bare_git_repo.create_tag("1.0.0")
    idx.commit(
        message="feat: docker",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-04-25 08:54:00",
    )
    idx.commit(
        message="fix: crash on connection reset",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-04-25 08:55:00",
    )
    idx.commit(
        message="feat: readme",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-04-25 09:18:00",
    )
    idx.commit(
        message="chore(release): 1.1.0",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-04-25 09:18:00",
    )
    bare_git_repo.create_tag("1.1.0")
    idx.commit(
        message="fix: typo in readme",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-04-25 09:22:00",
    )
    idx.commit(
        message="chore(release): 1.1.1",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-04-25 09:23:00",
    )
    bare_git_repo.create_tag("1.1.1")
    idx.commit(
        message="fix: no port in readme",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-04-25 11:20:00",
    )
    idx.commit(
        message="fix: close connection after write all message",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-05-02 02:31:00",
    )
    idx.commit(
        message="chore(release): 1.1.2",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-05-02 02:32:00",
    )
    bare_git_repo.create_tag("1.1.2")

    branch1 = bare_git_repo.create_head("branch1", "HEAD")

    branch2 = bare_git_repo.create_head("branch2", "HEAD")

    branch3 = bare_git_repo.create_head("branch3", "HEAD")

    # Checkout branch branch1
    bare_git_repo.head.reference = branch1
    idx.commit(
        message=textwrap.dedent(
            """
            chore(dep): bump lodash.template from 4.4.0 to 4.5.0

            Bumps [lodash.template](https://github.com/lodash/lodash) from 4.4.0 to 4.5.0.
            - [Release notes](https://github.com/lodash/lodash/releases)
            - [Commits](https://github.com/lodash/lodash/compare/4.4.0...4.5.0)
            """
        ).strip(),
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-07-11 06:34:00",
    )

    # merge branch branch1 into master
    master = bare_git_repo.heads.master  # right-hand side is ahead of us, in the future
    merge_base = bare_git_repo.merge_base(branch1, master)  # allows for a three-way merge
    idx.merge_tree(master, base=merge_base)  # write the merge result into index
    idx.commit("Merge branch branch1 into master", parent_commits=(branch1.commit, master.commit))

    branch4 = bare_git_repo.create_head("branch4", "HEAD")

    # Checkout branch branch2
    bare_git_repo.head.reference = branch2
    idx.commit(
        message=textwrap.dedent(
            """
            chore(dep): bump lodash from 4.17.11 to 4.17.14

            Bumps [lodash](https://github.com/lodash/lodash) from 4.17.11 to 4.17.14.
            - [Release notes](https://github.com/lodash/lodash/releases)
            - [Commits](https://github.com/lodash/lodash/compare/4.17.11...4.17.14)
            """
        ).strip(),
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-07-17 15:23:00",
    )

    # merge branch branch2 into master
    master = bare_git_repo.heads.master  # right-hand side is ahead of us, in the future
    merge_base = bare_git_repo.merge_base(branch2, master)  # allows for a three-way merge
    idx.merge_tree(master, base=merge_base)  # write the merge result into index
    idx.commit("Merge branch branch2 into master", parent_commits=(branch2.commit, master.commit))

    # Checkout branch branch3
    bare_git_repo.head.reference = branch3
    idx.commit(
        message=textwrap.dedent(
            """
            chore(dep): bump eslint-utils from 1.3.1 to 1.4.2

            Bumps [eslint-utils](https://github.com/mysticatea/eslint-utils) from 1.3.1 to 1.4.2.
            - [Release notes](https://github.com/mysticatea/eslint-utils/releases)
            - [Commits](https://github.com/mysticatea/eslint-utils/compare/v1.3.1...v1.4.2)
            """
        ).strip(),
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-08-26 18:07:00",
    )

    # merge branch branch3 into master
    master = bare_git_repo.heads.master  # right-hand side is ahead of us, in the future
    merge_base = bare_git_repo.merge_base(branch3, master)  # allows for a three-way merge
    idx.merge_tree(master, base=merge_base)  # write the merge result into index
    idx.commit("Merge branch branch3 into master", parent_commits=(branch3.commit, master.commit))

    # Checkout branch branch4
    bare_git_repo.head.reference = branch4
    idx.commit(
        message=textwrap.dedent(
            """
            chore(dep): bump mixin-deep from 1.3.1 to 1.3.2

            Bumps [mixin-deep](https://github.com/jonschlinkert/mixin-deep) from 1.3.1 to 1.3.2.
            - [Release notes](https://github.com/jonschlinkert/mixin-deep/releases)
            - [Commits](https://github.com/jonschlinkert/mixin-deep/compare/1.3.1...1.3.2)
            """
        ).strip(),
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-10-10 08:10:00",
    )

    # merge branch branch4 into master
    master = bare_git_repo.heads.master  # right-hand side is ahead of us, in the future
    merge_base = bare_git_repo.merge_base(branch4, master)  # allows for a three-way merge
    idx.merge_tree(master, base=merge_base)  # write the merge result into index
    idx.commit("Merge branch branch4 into master", parent_commits=(branch4.commit, master.commit))

    branch5 = bare_git_repo.create_head("branch5", "HEAD")

    branch6 = bare_git_repo.create_head("branch6", "HEAD")

    # Checkout branch branch5
    bare_git_repo.head.reference = branch5
    idx.commit(
        message=textwrap.dedent(
            """
            chore(dep): bump handlebars from 4.1.2 to 4.5.3

            Bumps [handlebars](https://github.com/wycats/handlebars.js) from 4.1.2 to 4.5.3.
            - [Release notes](https://github.com/wycats/handlebars.js/releases)
            - [Changelog](https://github.com/wycats/handlebars.js/blob/master/release-notes.md)
            - [Commits](https://github.com/wycats/handlebars.js/compare/v4.1.2...v4.5.3)
            """
        ).strip(),
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2019-12-28 01:55:00",
    )

    # Checkout branch branch6
    bare_git_repo.head.reference = branch6
    idx.commit(
        message=textwrap.dedent(
            """
            chore(dep): bump acorn from 6.1.1 to 6.4.1

            Bumps [acorn](https://github.com/acornjs/acorn) from 6.1.1 to 6.4.1.
            - [Release notes](https://github.com/acornjs/acorn/releases)
            - [Commits](https://github.com/acornjs/acorn/compare/6.1.1...6.4.1)
            """
        ).strip(),
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2020-03-14 08:39:00",
    )

    # merge branch branch6 into master
    master = bare_git_repo.heads.master  # right-hand side is ahead of us, in the future
    merge_base = bare_git_repo.merge_base(branch6, master)  # allows for a three-way merge
    idx.merge_tree(master, base=merge_base)  # write the merge result into index
    idx.commit("Merge branch branch6 into master", parent_commits=(branch6.commit, master.commit))

    branch7 = bare_git_repo.create_head("branch7", "HEAD")

    # Checkout branch branch7
    bare_git_repo.head.reference = branch7
    idx.commit(
        message=textwrap.dedent(
            """
            chore(dep): bump lodash from 4.17.14 to 4.17.19

            Bumps [lodash](https://github.com/lodash/lodash) from 4.17.14 to 4.17.19.
            - [Release notes](https://github.com/lodash/lodash/releases)
            - [Commits](https://github.com/lodash/lodash/compare/4.17.14...4.17.19)
            """
        ).strip(),
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2020-07-16 18:38:00",
    )

    # Checkout branch master
    bare_git_repo.head.reference = master
    idx.commit(
        message="chore(dep): update dependencies",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2020-07-20 07:54:00",
    )
    idx.commit(
        message="doc: fix logo link",
        committer=Actor(faker.name(), faker.ascii_safe_email()),
        commit_date="2020-07-20 07:58:00",
    )

    # merge branch branch5 into master
    master = bare_git_repo.heads.master  # right-hand side is ahead of us, in the future
    merge_base = bare_git_repo.merge_base(branch5, master)  # allows for a three-way merge
    idx.merge_tree(master, base=merge_base)  # write the merge result into index
    idx.commit(
        "Merge branch branch5 into master",
        parent_commits=(branch5.commit, master.commit),
        commit_date="2020-07-20 07:58:00",
    )

    # merge branch branch7 into master
    master = bare_git_repo.heads.master  # right-hand side is ahead of us, in the future
    merge_base = bare_git_repo.merge_base(branch7, master)  # allows for a three-way merge
    idx.merge_tree(master, base=merge_base)  # write the merge result into index
    idx.commit(
        "Merge branch branch7 into master",
        parent_commits=(branch7.commit, master.commit),
        commit_date="2020-07-20 07:58:00",
    )

    return bare_git_repo


def test_conventional_commits(conv_commit_repo):
    config_file_path = FIXTURES_DIR / "conventional-commit.yaml"
    config = configuration.get_default_config()
    config.update_from_file(config_file_path)
    config.template_dirs = []

    output = templating.render(conv_commit_repo, config, None)
    expected = (FIXTURES_DIR / "rendered_conv_commit_repo.md").read_text()
    assert output.strip() == expected.strip()
