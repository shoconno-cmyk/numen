# History snapshots

The Story Report's AI Output view, its definitions appendix and its Pass 2
timing line are built from earlier states of the data. This repo has a
fresh history, so it carries those states here; `git_snapshots.py` reads
them in place of `git show`. `manifest.json` holds each file's SHA-256
hash, and the build stops if a file doesn't match.

Commit IDs (`7a6e69e`, the cold run; `e26724d` and `8079f93`, the Pass 2
run; `d294e1c`, the last commit before it) refer to the development
repository's history.
