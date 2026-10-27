#!/usr/bin/env python3
"""
Export copies of the spec for AI tools that only read their own folders.

Some tools load rules, skills, or slash commands from a tool-specific folder
instead of reading _system/. _system/ stays the source of truth; this script
writes copies to the folders named in _system/config.md:

  export_rules_dir:     {dir}/00-readme-for-ai.md, {dir}/01-config.md,
                        {dir}/NN-{origin}-{name}.md for every rule (core, packs, local)
  export_skills_dir:    {dir}/{name}/SKILL.md for every workflow (local > pack > core)
  export_commands_dir:  {dir}/{name}.md for every workflow name and one-word alias

  export_user_only: [names]           workflows the tool should run only when asked
  export_user_only_frontmatter: path  YAML lines (in your tool's syntax) added to those
                                      skills' frontmatter, e.g. a "do not auto-invoke" flag

Leave a key blank to skip that export. Every exported file carries a GENERATED banner.

Safety:
  - Never overwrites a file that lacks the GENERATED banner. Reports it as a conflict.
  - Removes generated files whose source no longer exists, if the filesystem allows deletes;
    otherwise lists them.
  - Leaves every other file in those folders alone.

Usage:
    python3 _system/scripts/export-agent-files.py [vault]
    python3 _system/scripts/export-agent-files.py --dry-run [vault]
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


def source_of(path):
    try:
        with open(path, encoding="utf-8") as fh:
            m = re.search(r"<!-- Source: (.+?) -->", fh.read(4000))
    except OSError:
        return None
    return m.group(1).strip() if m else None


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
    targets = {k: cfg.get(f"export_{k}_dir") for k in ("rules", "skills", "commands")}
    targets = {k: os.path.join(vault, v) for k, v in targets.items() if isinstance(v, str) and v}
    if not targets:
        print("Nothing to export: set export_rules_dir, export_skills_dir, or export_commands_dir in _system/config.md.")
        return
    planned = {}  # dest path -> (content, source rel)

    def rel(p):
        return os.path.relpath(p, vault)

    def add(dest, src_path, text=None):
        if text is None:
            with open(src_path, encoding="utf-8") as fh:
                text = fh.read()
        planned[dest] = with_banner(text, rel(src_path))

    sysdir = os.path.join(vault, "_system")
    if "rules" in targets:
        rd = targets["rules"]
        add(os.path.join(rd, "00-readme-for-ai.md"), os.path.join(sysdir, "README-for-AI.md"))
        add(os.path.join(rd, "01-config.md"), os.path.join(sysdir, "config.md"))
        # Rules: keep every file, in layer order. Name = NN-origin-rest.
        for origin, path in vaultlib.layered(vault, "rules", cfg):
            fname = os.path.basename(path)
            m = re.match(r"(\d+)-(.*)", fname)
            num, rest = (m.group(1), m.group(2)) if m else ("90", fname)
            add(os.path.join(rd, f"{num}-{origin}-{rest}"), path)

    # Workflows: last layer wins per name.
    workflows = {}
    for origin, path in vaultlib.layered(vault, "workflows", cfg):
        fm, _ = vaultlib.read_frontmatter(path)
        name = fm.get("name") or os.path.splitext(os.path.basename(path))[0]
        workflows[name] = (path, fm)

    # Optional: mark some skills "only when the owner asks" in the tool's own syntax.
    user_only = set(vaultlib.as_list(cfg.get("export_user_only")))
    extra_fm = ""
    fm_file = cfg.get("export_user_only_frontmatter")
    if isinstance(fm_file, str) and fm_file:
        with open(os.path.join(vault, fm_file), encoding="utf-8") as fh:
            extra_fm = fh.read().strip("\n") + "\n"

    for name, (path, fm) in sorted(workflows.items()):
        if "skills" in targets:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            if (name in user_only or fm.get("invocation") == "user") and extra_fm and text.startswith("---"):
                end = text.find("\n---", 3)
                text = text[:end + 1] + extra_fm + text[end + 1:]
            add(os.path.join(targets["skills"], name, "SKILL.md"), path, text)
        if "commands" not in targets:
            continue
        desc = fm.get("description", "").replace('"', "'")
        hint = fm.get("argument-hint", "")
        cmd_names = [name] + [a for a in vaultlib.as_list(fm.get("aliases")) if re.fullmatch(r"[a-z0-9\-]+", a)]
        for cmd in cmd_names:
            body = (f"---\ndescription: \"{desc}\"\nargument-hint: \"{hint}\"\n---\n"
                    f"Use the `{name}` skill. Arguments: $1 $2 $3\n\n"
                    f"Read `_system/README-for-AI.md` if you have not this session, and follow the workflow exactly.\n")
            planned[os.path.join(targets["commands"], f"{cmd}.md")] = with_banner(body, rel(path))

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

    # A generated file this run did not plan is removed only when its source is gone.
    # If the source still exists, another tool probably derived the file from one of
    # ours (for example a tool that turns commands into skills): leave it and report it.
    stale, stale_left, derived = [], [], []
    for d in targets.values():
        if not os.path.isdir(d):
            continue
        for cur, _, files in os.walk(d):
            for f in files:
                p = os.path.join(cur, f)
                if p not in planned and f.endswith(".md") and is_generated(p):
                    src = source_of(p)
                    if src and os.path.exists(os.path.join(vault, src)):
                        derived.append(rel(p))
                        continue
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
    if derived:
        print(f"Left in place: {len(derived)} files carry our banner but were not written by this run; "
              "their source still exists, so another tool likely derived them:")
        for p in derived:
            print(f"  = {p}")
    if stale_left:
        print("Could not delete these (filesystem refused). Delete them by hand:")
        for p in stale_left:
            print(f"  ! {p}")
    if conflicts:
        print(f"CONFLICTS: {len(conflicts)} files exist without the GENERATED banner and were left alone.")
        print("Move them into _system/local/ (rules or workflows), delete the exported copy, and re-run:")
        for p in conflicts:
            print(f"  ? {p}")
        sys.exit(1)
    rules_dir = targets.get("rules")
    if rules_dir and os.path.isdir(rules_dir):
        hand = [f for f in sorted(os.listdir(rules_dir))
                if f.endswith(".md") and not is_generated(os.path.join(rules_dir, f))]
        if hand:
            print(f"Note: hand-written rules in {rel(rules_dir)}/ that other AI tools will not see. "
                  "Move them to _system/local/rules/ so every agent follows them:")
            for f in hand:
                print(f"  * {rel(rules_dir)}/{f}")


if __name__ == "__main__":
    main()
