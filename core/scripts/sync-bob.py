#!/usr/bin/env python3
"""
Generate IBM Bob's .bob/ folder from _system/.

Bob auto-loads .bob/rules/ on every message and offers .bob/skills/ and
.bob/commands/. _system/ is the source of truth; this script writes copies.

What it writes (every file starts with a GENERATED banner):
  .bob/rules/00-readme-for-ai.md      _system/README-for-AI.md
  .bob/rules/01-config.md             _system/config.md
  .bob/rules/NN-{origin}-{name}.md    every rule: core, then packs, then local
  .bob/skills/{name}/SKILL.md         every workflow (local overrides pack overrides core)
  .bob/commands/{name}.md             one per workflow name and one-word alias

Safety:
  - Never overwrites a file that lacks the GENERATED banner. Reports it as a conflict.
  - Removes generated files whose source no longer exists, if the filesystem allows deletes;
    otherwise lists them.
  - Leaves everything else in .bob/ alone (custom_modes.yaml, your own skills).

Usage:
    python3 _system/scripts/sync-bob.py [vault]          write
    python3 _system/scripts/sync-bob.py --dry-run [vault]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib  # noqa: E402


def is_generated(path):
    try:
        with open(path, encoding="utf-8") as fh:
            head = fh.read(4000)
    except OSError:
        return False
    return vaultlib.BANNER in head


def with_banner(text, source_rel):
    note = f"{vaultlib.BANNER}\n<!-- Source: {source_rel} -->\n\n"
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm_end = end + 4
            return text[:fm_end] + "\n" + note + text[fm_end:].lstrip("\n")
    return note + text


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    vault = vaultlib.find_vault_root(args[0] if args else os.getcwd())
    if not vault:
        print("No vault found (need _system/config.md).")
        sys.exit(2)
    cfg = vaultlib.read_config(vault)
    bob = os.path.join(vault, ".bob")
    planned = {}  # dest path -> (content, source rel)

    def rel(p):
        return os.path.relpath(p, vault)

    def add(dest, src_path, text=None):
        if text is None:
            with open(src_path, encoding="utf-8") as fh:
                text = fh.read()
        planned[dest] = with_banner(text, rel(src_path))

    sysdir = os.path.join(vault, "_system")
    add(os.path.join(bob, "rules", "00-readme-for-ai.md"), os.path.join(sysdir, "README-for-AI.md"))
    add(os.path.join(bob, "rules", "01-config.md"), os.path.join(sysdir, "config.md"))

    # Rules: keep every file, in layer order. Name = NN-origin-rest.
    for origin, path in vaultlib.layered(vault, "rules", cfg):
        fname = os.path.basename(path)
        m = re.match(r"(\d+)-(.*)", fname)
        num, rest = (m.group(1), m.group(2)) if m else ("90", fname)
        add(os.path.join(bob, "rules", f"{num}-{origin}-{rest}"), path)

    # Workflows: last layer wins per name.
    workflows = {}
    for origin, path in vaultlib.layered(vault, "workflows", cfg):
        fm, _ = vaultlib.read_frontmatter(path)
        name = fm.get("name") or os.path.splitext(os.path.basename(path))[0]
        workflows[name] = (path, fm)

    for name, (path, fm) in sorted(workflows.items()):
        add(os.path.join(bob, "skills", name, "SKILL.md"), path)
        desc = fm.get("description", "").replace('"', "'")
        hint = fm.get("argument-hint", "")
        cmd_names = [name] + [a for a in vaultlib.as_list(fm.get("aliases")) if re.fullmatch(r"[a-z0-9\-]+", a)]
        for cmd in cmd_names:
            body = (f"---\ndescription: \"{desc}\"\nargument-hint: \"{hint}\"\n---\n"
                    f"Use the `{name}` skill. Arguments: $1 $2 $3\n\n"
                    f"Read `_system/README-for-AI.md` if you have not this session, and follow the workflow exactly.\n")
            planned[os.path.join(bob, "commands", f"{cmd}.md")] = with_banner(body, rel(path))

    written, unchanged, conflicts = [], [], []
    for dest, content in sorted(planned.items()):
        if os.path.exists(dest):
            if not is_generated(dest):
                conflicts.append(rel(dest))
                continue
            with open(dest, encoding="utf-8") as fh:
                if fh.read() == content:
                    unchanged.append(rel(dest))
                    continue
        written.append(rel(dest))
        if not dry:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as fh:
                fh.write(content)

    stale, stale_left = [], []
    for sub in ("rules", "skills", "commands"):
        d = os.path.join(bob, sub)
        if not os.path.isdir(d):
            continue
        for cur, _, files in os.walk(d):
            for f in files:
                p = os.path.join(cur, f)
                if p not in planned and f.endswith(".md") and is_generated(p):
                    stale.append(rel(p))
                    if not dry:
                        try:
                            os.remove(p)
                        except OSError:
                            stale_left.append(rel(p))

    label = "Would write" if dry else "Wrote"
    print(f"{label} {len(written)} files, {len(unchanged)} unchanged.")
    for p in written:
        print(f"  + {p}")
    if stale:
        print(f"Generated files with no source any more: {len(stale)}" + (" (not removed, dry run)" if dry else ""))
        for p in stale:
            print(f"  - {p}")
    if stale_left:
        print("Could not delete these (filesystem refused). Delete them by hand:")
        for p in stale_left:
            print(f"  ! {p}")
    if conflicts:
        print(f"CONFLICTS: {len(conflicts)} files exist without the GENERATED banner and were left alone.")
        print("Move them into _system/local/ (rules or workflows), delete the .bob copy, and re-run:")
        for p in conflicts:
            print(f"  ? {p}")
        sys.exit(1)
    rules_dir = os.path.join(bob, "rules")
    if os.path.isdir(rules_dir):
        hand = [f for f in sorted(os.listdir(rules_dir))
                if f.endswith(".md") and not is_generated(os.path.join(rules_dir, f))]
        if hand:
            print("Note: hand-written rules in .bob/rules/ that other AI tools will not see. "
                  "Move them to _system/local/rules/ so every agent follows them:")
            for f in hand:
                print(f"  * .bob/rules/{f}")


if __name__ == "__main__":
    main()
