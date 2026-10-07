"""
git_snapshots.py -- files as they stood at an earlier commit.

The Story Report's AI Output view, its definitions appendix and its Pass 2
timing line are built from earlier states of the data (the cold run,
7a6e69e; the Pass 2 run, e26724d and 8079f93; the last commit before it,
d294e1c). In the development repo they are read with git. The public
repo has a fresh history without those commits, so it carries the few
files it needs in history_snapshots/, with a manifest of their SHA-256
hashes; when that folder holds a file, it is read from there instead.

Commit IDs in the pages and records refer to the development repo's
history.
"""
import hashlib
import json
import os
import subprocess
import sys
import types

ROOT = os.path.dirname(os.path.abspath(__file__))
SNAP_DIR = os.path.join(ROOT, "history_snapshots")
MANIFEST = os.path.join(SNAP_DIR, "manifest.json")


def _manifest():
    if not os.path.exists(MANIFEST):
        return None
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def _snapshot(name):
    """A snapshot file's bytes, checked against the manifest, or None."""
    m = _manifest()
    if m is None or name not in m["files"]:
        return None
    with open(os.path.join(SNAP_DIR, name), "rb") as f:
        data = f.read()
    if hashlib.sha256(data).hexdigest() != m["files"][name]["sha256"]:
        sys.exit(f"ABORT: history_snapshots/{name} does not match its manifest hash")
    return data


def _git(*args):
    out = subprocess.run(["git", *args], capture_output=True, cwd=ROOT)
    if out.returncode:
        sys.exit(f"ABORT: git {' '.join(args)} failed: {out.stderr.decode(errors='replace')}")
    return out.stdout


def show(commit, path):
    """The bytes of `path` at `commit`."""
    data = _snapshot(f"{commit}/{path}")
    return data if data is not None else _git("show", f"{commit}:{path}")


def show_json(commit, path):
    return json.loads(show(commit, path).decode("utf-8"))


def definitions(commit):
    """BIG_SEVEN_DEFINITIONS as tagging_schema.py held them at `commit`."""
    data = _snapshot(f"{commit}/BIG_SEVEN_DEFINITIONS.json")
    if data is not None:
        return json.loads(data.decode("utf-8"))
    mod = types.ModuleType("tagging_schema_at_" + commit)
    exec(compile(show(commit, "tagging_schema.py").decode("utf-8"), mod.__name__, "exec"), mod.__dict__)
    return dict(mod.BIG_SEVEN_DEFINITIONS)


def first_commit_touching(since, until, path):
    """The first commit after `since`, up to `until`, that changed `path`."""
    m = _manifest()
    key = f"{since}..{until}:{path}"
    if m is not None and key in m.get("first_commit_touching", {}):
        return m["first_commit_touching"][key]
    return _git("rev-list", "--reverse", "--abbrev-commit", f"{since}..{until}", "--", path).decode().split()[0]
