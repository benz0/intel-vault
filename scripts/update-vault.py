#!/usr/bin/env python3
"""
Update an existing vault's _system/ from this repo.

Replaces core rules, workflows, templates, scripts, adapters, and the files of
every pack listed in config `packs`. Never touches:
  - _system/config.md
  - _system/local/          (your own rules and workflows)
  - anything outside _system/ (except export folders, via export-agent-files.py, if configured)

Usage:
    python3 scripts/update-vault.py <vault> [--dry-run] [--add-pack NAME]
"""
import argparse
import filecmp
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "core", "scripts"))
import vaultlib  # noqa: E402


def plan_copy(src, dst, skip_top=()):
    """Return list of (src_file, dst_file, status) where status is new|changed|same."""
    out = []
    for cur, dirs, files in os.walk(src):
        rel = os.path.relpath(cur, src)
        top = rel.split(os.sep)[0]
        if top in skip_top:
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in files:
            if f.endswith(".pyc") or (rel == "." and f in skip_top):
                continue
            s = os.path.join(cur, f)
            d = os.path.join(dst, rel, f)
            if not os.path.exists(d):
                out.append((s, d, "new"))
            elif not filecmp.cmp(s, d, shallow=False):
                out.append((s, d, "changed"))
            else:
                out.append((s, d, "same"))
    return out


def orphans(src, dst, skip_top=()):
    """Files in dst that no longer exist in src."""
    out = []
    if not os.path.isdir(dst):
        return out
    for cur, dirs, files in os.walk(dst):
        rel = os.path.relpath(cur, dst)
        if rel.split(os.sep)[0] in skip_top:
            dirs[:] = []
            continue
        for f in files:
            if rel == "." and f in skip_top:
                continue
            if not os.path.exists(os.path.join(src, rel, f)):
                out.append(os.path.join(dst, rel, f))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--add-pack", action="append", default=[])
    a = ap.parse_args()

    vault = os.path.abspath(a.vault)
    cfg_path = os.path.join(vault, "_system", "config.md")
    if not os.path.isfile(cfg_path):
        sys.exit(f"No _system/config.md in {vault}. Use scripts/new-vault.py for a new vault.")
    cfg = vaultlib.read_config(vault)
    packs = vaultlib.as_list(cfg.get("packs"))
    for p in a.add_pack:
        if not os.path.isdir(os.path.join(REPO, "packs", p)):
            sys.exit(f"Unknown pack: {p}")
        if p not in packs:
            packs.append(p)

    sysdir = os.path.join(vault, "_system")
    jobs = [(os.path.join(REPO, "core"), sysdir, ("local", "config.md", "config.example.md", "packs", "adapters", "VERSION")),
            (os.path.join(REPO, "adapters"), os.path.join(sysdir, "adapters"), ())]
    jobs += [(os.path.join(REPO, "packs", p), os.path.join(sysdir, "packs", p), ()) for p in packs]

    actions, stale = [], []
    for src, dst, skip in jobs:
        actions += plan_copy(src, dst, skip)
        stale += orphans(src, dst, skip)

    new = [x for x in actions if x[2] == "new"]
    changed = [x for x in actions if x[2] == "changed"]
    print(f"{'Would update' if a.dry_run else 'Updating'} {vault}")
    print(f"  new: {len(new)}  changed: {len(changed)}  unchanged: {len(actions) - len(new) - len(changed)}")
    for s, d, st in new + changed:
        print(f"  {'+' if st == 'new' else '~'} {os.path.relpath(d, vault)}")
    if stale:
        print(f"  Files no longer in the repo (left in place; delete by hand if unused): {len(stale)}")
        for d in stale:
            print(f"  ? {os.path.relpath(d, vault)}")

    if a.dry_run:
        return
    for s, d, st in new + changed:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
    try:
        with open(os.path.join(REPO, "VERSION"), encoding="utf-8") as fh:
            ver = fh.read()
        with open(os.path.join(sysdir, "VERSION"), "w", encoding="utf-8") as fh:
            fh.write(ver)
    except OSError:
        pass
    if a.add_pack:
        with open(cfg_path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        lines = [("packs: [" + ", ".join(packs) + "]") if ln.startswith("packs:") else ln for ln in lines]
        with open(cfg_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"  packs in config: {', '.join(packs)}  (add the pack's config keys from its pack.md)")

    if vaultlib.export_dirs(cfg):
        print("Running export-agent-files.py ...")
        subprocess.call([sys.executable, os.path.join(sysdir, "scripts", "export-agent-files.py"), vault])


if __name__ == "__main__":
    main()
