#!/usr/bin/env python3
"""
Hygiene check for vault files. Reports real counts so nobody has to trust "clean".

Checks every .md file under the paths given (files or folders):
  1. Forbidden characters from `forbidden_chars` in _system/config.md (e.g. U+2014),
     ignoring exact strings listed in `forbidden_chars_allow` (e.g. a signature line)
  2. Wikilinks that resolve to no file
  3. Bare wikilinks that match more than one file (ambiguous)
  4. Links into a people folder whose display alias differs from the file name
     (a likely alias/target mismatch; review by hand)

Skips fenced code blocks, hidden folders, _system/, any export_*_dir folders, and any
folder listed in `check_exclude` in config (or passed with --exclude). An entry without a
slash matches a folder of that name anywhere (e.g. `_Backups`); one with a slash matches
that path from the vault root.

Raw source folders (`check_raw_dirs`, default [Sources]) are checked for links but not for
forbidden characters: sources are saved unedited by design, so their characters are not errors.

Links written with the extension (`[[Account Overview.md]]`) resolve like Obsidian resolves them.

Exit code 1 if anything is found.

Usage:
    python3 _system/scripts/check-vault.py [paths...]      (default: whole vault)
    python3 _system/scripts/check-vault.py --quiet [paths...]  counts only
    python3 _system/scripts/check-vault.py --exclude "_Claude project" --exclude _Backups
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib  # noqa: E402

LINK = re.compile(r"!?\[\[([^\]]+?)\]\]")
PEOPLE_DIRS = {"stakeholders", "people", "team", "customer", "internal"}
SKIP_DIRS = {"_system", ".git", ".obsidian", "node_modules"}


def excluded(rel_dir, name, skip_rel, skip_names):
    return (name in SKIP_DIRS or name.startswith(".") or name.lower() in skip_names
            or os.path.normpath(os.path.join(rel_dir, name)) in skip_rel)


def md_files(paths, root, skip_rel=(), skip_names=()):
    for p in paths:
        p = os.path.abspath(p)
        if os.path.isfile(p):
            if p.endswith(".md"):
                yield p
            continue
        for d, subdirs, files in os.walk(p):
            rel = os.path.relpath(d, root)
            subdirs[:] = [s for s in subdirs if not excluded(rel, s, skip_rel, skip_names)]
            for f in files:
                if f.endswith(".md"):
                    yield os.path.join(d, f)


def build_index(root):
    by_name = {}
    paths = set()
    for d, subdirs, files in os.walk(root):
        subdirs[:] = [s for s in subdirs if not s.startswith(".")]
        for f in files:
            full = os.path.join(d, f)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            paths.add(rel.lower())
            stem = f[:-3] if f.endswith(".md") else f
            by_name.setdefault(stem.lower(), []).append(rel)
            if not f.endswith(".md"):
                by_name.setdefault(f.lower(), []).append(rel)
    return by_name, paths


def strip_code(text):
    out, fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            out.append("")
            continue
        out.append("" if fence else re.sub(r"`[^`]*`", "", line))
    return out


def resolve(target, by_name, paths):
    t = target.strip().replace("\\", "")
    t = t.split("#", 1)[0].split("^", 1)[0].strip()
    if not t:
        return "ok", None
    if t.lower().endswith(".md"):
        t = t[:-3]
    if "/" in t:
        tl = t.lower()
        if tl in paths or (tl + ".md") in paths:
            return "ok", t
        # Obsidian also matches a path suffix
        hits = [p for p in paths if p.endswith("/" + tl) or p.endswith("/" + tl + ".md")]
        return ("ok", hits[0]) if len(hits) == 1 else ("missing", None) if not hits else ("ambiguous", None)
    hits = by_name.get(t.lower(), [])
    if not hits:
        return "missing", None
    if len(hits) > 1:
        return "ambiguous", None
    return "ok", hits[0]


def main():
    argv = sys.argv[1:]
    quiet = "--quiet" in argv
    cli_exclude, args, i = [], [], 0
    while i < len(argv):
        if argv[i] == "--exclude" and i + 1 < len(argv):
            cli_exclude.append(argv[i + 1])
            i += 2
            continue
        if argv[i] != "--quiet":
            args.append(argv[i])
        i += 1
    start = args[0] if args else os.getcwd()
    root = vaultlib.find_vault_root(start)
    if not root:
        print("No vault found (looked for _system/config.md above %s)" % start)
        sys.exit(2)
    cfg = vaultlib.read_config(root)
    bad_chars = vaultlib.forbidden_chars(cfg)
    allowed = vaultlib.allowed_strings(cfg)
    skip_rel = {os.path.normpath(d) for d in vaultlib.export_dirs(cfg)}
    skip_names, user_rel, shown = set(), set(), set()
    for d in vaultlib.as_list(cfg.get("check_exclude")) + cli_exclude:
        d = d.strip().strip("/")
        if not d:
            continue
        if "/" in d:
            skip_rel.add(os.path.normpath(d))
            user_rel.add(d)
        else:
            skip_names.add(d.lower())
            shown.add(d)
    raw_dirs = {d.strip().strip("/").lower() for d in
                (vaultlib.as_list(cfg.get("check_raw_dirs")) if cfg.get("check_raw_dirs") is not None
                 else ["Sources"]) if d.strip()}
    by_name, paths = build_index(root)
    targets = args or [root]

    counts = {"files": 0, "links": 0, "forbidden": 0, "missing": 0, "ambiguous": 0, "alias": 0, "raw": 0}
    findings = []
    for f in md_files(targets, root, skip_rel, skip_names):
        counts["files"] += 1
        rel = os.path.relpath(f, root)
        with open(f, encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        is_raw = bool(raw_dirs & {part.lower() for part in rel.split(os.sep)[:-1]})
        if is_raw:
            counts["raw"] += 1
        for n, line in enumerate([] if is_raw else raw.splitlines(), 1):
            for ok in allowed:
                line = line.replace(ok, "")
            for ch in bad_chars:
                c = line.count(ch)
                if c:
                    counts["forbidden"] += c
                    findings.append(f"{rel}:{n}: forbidden character U+{ord(ch):04X} x{c}")
        for n, line in enumerate(strip_code(raw), 1):
            for m in LINK.finditer(line):
                counts["links"] += 1
                inner = m.group(1).replace("\\|", "|")
                target, _, alias = inner.partition("|")
                status, hit = resolve(target, by_name, paths)
                if status == "missing":
                    counts["missing"] += 1
                    findings.append(f"{rel}:{n}: broken link [[{inner}]]")
                elif status == "ambiguous":
                    counts["ambiguous"] += 1
                    findings.append(f"{rel}:{n}: ambiguous bare link [[{inner}]] (use a full path)")
                elif hit and alias.strip():
                    parts = [p.lower() for p in hit.split("/")[:-1]]
                    stem = os.path.splitext(hit.split("/")[-1])[0]
                    if PEOPLE_DIRS & set(parts) and alias.strip().lower() != stem.lower():
                        counts["alias"] += 1
                        findings.append(f"{rel}:{n}: check alias [[{inner}]] points at '{stem}'")

    if not quiet:
        for line in findings:
            print(line)
        if findings:
            print()
    print("Checked {files} files ({raw} raw sources, links only), {links} wikilinks.".format(**counts))
    if skip_names or user_rel:
        print("Excluded folders: " + ", ".join(sorted(shown | user_rel)))
    print("Forbidden characters: {forbidden} | Broken links: {missing} | Ambiguous links: {ambiguous} | "
          "Alias mismatches to review: {alias}".format(**counts))
    if not bad_chars:
        print("Note: no forbidden_chars set in _system/config.md, so no character check ran.")
    sys.exit(1 if (counts["forbidden"] or counts["missing"] or counts["ambiguous"]) else 0)


if __name__ == "__main__":
    main()
