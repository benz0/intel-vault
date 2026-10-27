#!/usr/bin/env python3
"""
Publish a read-only copy of the vault for AI tools that cannot reach it directly.

Some assistants (for example Microsoft 365 Copilot) only read files in cloud
storage such as OneDrive or SharePoint. This script mirrors the vault one way
into `publish_dir` (set in _system/config.md), usually a folder your cloud
storage client syncs. The vault stays the only copy anyone edits.

  - Copies new and changed files, removes files that no longer exist in the vault.
  - Skips everything in `publish_exclude` (vault-relative paths), hidden folders,
    and the export_*_dir folders.
  - Writes _PUBLISHED.md at the top of the copy with the publish time.
  - publish_layout: mirror (default) keeps the folder tree. flat (experimental)
    puts every file at the top level, named "Accounts - Acme - Current State.md",
    for assistants that struggle with deep folders. Links between notes are not
    rewritten in flat mode.
  - Refuses to publish into a non-empty folder that it did not create (no
    _PUBLISHED.md marker), so a typo cannot wipe an unrelated folder.

Usage:
    python3 _system/scripts/publish-vault.py [vault]
    python3 _system/scripts/publish-vault.py --dry-run [vault]
"""
import datetime
import filecmp
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib  # noqa: E402

MARKER = "_PUBLISHED.md"


def excluded(rel, excludes):
    rel = rel.replace(os.sep, "/")
    for e in excludes:
        e = e.strip("/")
        if rel == e or rel.startswith(e + "/"):
            return True
    return any(part.startswith(".") for part in rel.split("/"))


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    vault = vaultlib.find_vault_root(args[0] if args else os.getcwd())
    if not vault:
        print("No vault found (need _system/config.md).")
        sys.exit(2)
    cfg = vaultlib.read_config(vault)
    dest = cfg.get("publish_dir")
    if not isinstance(dest, str) or not dest:
        print("Publishing is off: publish_dir is not set in _system/config.md.")
        return
    dest = os.path.abspath(os.path.expanduser(dest))
    if dest == vault or dest.startswith(vault + os.sep) or vault.startswith(dest + os.sep):
        sys.exit(f"publish_dir must be outside the vault, and must not contain it: {dest}")
    if os.path.isdir(dest) and os.listdir(dest) and not os.path.exists(os.path.join(dest, MARKER)):
        sys.exit(f"{dest} is not empty and was not created by this script (no {MARKER}). "
                 "Point publish_dir at an empty folder.")

    excludes = vaultlib.as_list(cfg.get("publish_exclude")) + vaultlib.export_dirs(cfg)
    layout = (cfg.get("publish_layout") or "mirror").strip().lower()
    if layout not in ("mirror", "flat"):
        sys.exit(f"publish_layout must be mirror or flat, not {layout}")

    wanted = {}
    for cur, dirs, files in os.walk(vault):
        rel_dir = os.path.relpath(cur, vault)
        rel_dir = "" if rel_dir == "." else rel_dir
        dirs[:] = [d for d in dirs if not excluded(os.path.join(rel_dir, d), excludes)]
        for f in files:
            rel = os.path.join(rel_dir, f)
            if f == ".DS_Store" or excluded(rel, excludes) or rel == MARKER:
                continue
            out = rel if layout == "mirror" else rel.replace(os.sep, " - ")
            wanted[out] = os.path.join(vault, rel)

    copied, removed = [], []
    for rel, src in sorted(wanted.items()):
        d = os.path.join(dest, rel)
        if os.path.exists(d) and filecmp.cmp(src, d, shallow=False):
            continue
        copied.append(rel)
        if not dry:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(src, d)

    if os.path.isdir(dest):
        for cur, dirs, files in os.walk(dest, topdown=False):
            for f in files:
                rel = os.path.relpath(os.path.join(cur, f), dest)
                if rel != MARKER and rel not in wanted:
                    removed.append(rel)
                    if not dry:
                        os.remove(os.path.join(cur, f))
            if not dry and cur != dest and not os.listdir(cur):
                os.rmdir(cur)

    now = datetime.datetime.now().astimezone()
    stamp = now.strftime("%Y-%m-%d %H:%M %Z")
    if not dry:
        os.makedirs(dest, exist_ok=True)
        with open(os.path.join(dest, MARKER), "w", encoding="utf-8") as fh:
            fh.write(
                "# Read-only copy of an intel vault\n\n"
                f"**Published:** {stamp}\n\n"
                "This folder is a one-way copy made by `_system/scripts/publish-vault.py`. "
                "**Edits made here are overwritten at the next publish.** The real vault lives elsewhere.\n\n"
                "**AI assistants reading this copy:** you are a reader, not a writer. "
                "Say how old this copy is when it matters, never claim to have updated a file, "
                "and when the owner gives you new information, answer with a capture note in the "
                "format in `_system/templates/capture.md`.\n\n"
                f"Files: {len(wanted)}. Layout: {layout}. Excluded paths: {', '.join(excludes) or 'none'}.\n"
            )
    label = "Would publish" if dry else "Published"
    print(f"{label} to {dest}: {len(copied)} copied, {len(removed)} removed, "
          f"{len(wanted) - len(copied)} unchanged, at {stamp}.")


if __name__ == "__main__":
    main()
