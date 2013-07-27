Date: 2013-06-17
Title: Experimenting with Git Hooks
Category: Software
Tags: bash, git

I have been trying to follow a more disciplined approach to branching in my
projects to allow easier tracking and regression. For example, I learnt that
it's a good idea to prefix branch names with category tokens, such as
`feature/`, `bug/`, or `chore/`. This allows us to use wildcards when listing
branches:

    $> git branch --list bug/*
    $> git branch --list feature/*
    feature/X49972617


Since I use Pivotal Tracker, I name my branches `<type>/X<story-id>`, and then
use a simple hook to prepend all of my commit messages with the story ID.

<script src="https://gist.github.com/jimjh/5798168.js"></script>

    $> git commit
    [#49972617]
    # Please enter the commit message for your changes. Lines starting
    # with '#' will be ignored, and an empty message aborts the commit.
    # On branch feature/X49972617
