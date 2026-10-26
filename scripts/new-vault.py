#!/usr/bin/env python3
"""
Create a new intel vault.

Usage:
    python3 scripts/new-vault.py <destination folder> [options]

Options:
    --packs cse[,se,...]      packs to install (default: none, core only)
    --owner "Jordan Lee"      owner name
    --initials JL
    --role "Customer Success Engineer"
    --org "Acme Corp"
    --manager "Pat Smith"
    --tz America/New_York     IANA timezone
    --agents claude,copilot   AI tools that will work in the vault
    --no-em-dash              add U+2014 to forbidden_chars

The destination may exist but must not already contain _system/.
Nothing outside the destination is touched.
"""
import argparse
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "core", "scripts"))
import vaultlib  # noqa: E402


def version():
    try:
        with open(os.path.join(REPO, "VERSION"), encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return "unknown"


def copy_tree(src, dst, skip=()):
    for cur, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in ("__pycache__",)]
        rel = os.path.relpath(cur, src)
        if any(rel == s or rel.startswith(s + os.sep) for s in skip):
            continue
        os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in files:
            if f.endswith(".pyc"):
                continue
            shutil.copy2(os.path.join(cur, f), os.path.join(dst, rel, f))


def install_system(vault, packs):
    sysdir = os.path.join(vault, "_system")
    copy_tree(os.path.join(REPO, "core"), sysdir, skip=())
    os.remove(os.path.join(sysdir, "config.example.md"))
    copy_tree(os.path.join(REPO, "adapters"), os.path.join(sysdir, "adapters"))
    for p in packs:
        src = os.path.join(REPO, "packs", p)
        if not os.path.isdir(src):
            sys.exit(f"Unknown pack: {p}. Available: {', '.join(sorted(os.listdir(os.path.join(REPO, 'packs'))))}")
        copy_tree(src, os.path.join(sysdir, "packs", p))
    with open(os.path.join(sysdir, "VERSION"), "w", encoding="utf-8") as fh:
        fh.write(version() + "\n")


def fill(text, values):
    for k, v in values.items():
        text = text.replace("{" + k + "}", v)
    return text


def set_key(text, key, value):
    out = []
    for line in text.splitlines():
        if line.startswith(key + ":"):
            comment = ""
            if "#" in line:
                comment = "  " + line[line.index("#"):]
            line = f"{key}: {value}".ljust(22) + comment if comment else f"{key}: {value}"
        out.append(line)
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Create a new intel vault.")
    ap.add_argument("dest")
    ap.add_argument("--packs", default="")
    ap.add_argument("--owner", default="")
    ap.add_argument("--initials", default="")
    ap.add_argument("--role", default="")
    ap.add_argument("--org", default="")
    ap.add_argument("--manager", default="")
    ap.add_argument("--tz", default="")
    ap.add_argument("--agents", default="claude")
    ap.add_argument("--no-em-dash", action="store_true")
    a = ap.parse_args()

    vault = os.path.abspath(a.dest)
    if os.path.exists(os.path.join(vault, "_system")):
        sys.exit(f"{vault} already has _system/. Use scripts/update-vault.py to update it.")
    os.makedirs(vault, exist_ok=True)
    packs = [p.strip() for p in a.packs.split(",") if p.strip()]
    agents = [x.strip() for x in a.agents.split(",") if x.strip()]

    install_system(vault, packs)
    sysdir = os.path.join(vault, "_system")

    # config.md
    with open(os.path.join(REPO, "core", "config.example.md"), encoding="utf-8") as fh:
        cfg = fh.read()
    for key, val in [("owner_name", a.owner), ("owner_initials", a.initials), ("owner_role", a.role),
                     ("organization", a.org), ("manager", a.manager), ("timezone", a.tz),
                     ("packs", "[" + ", ".join(packs) + "]"), ("agents", "[" + ", ".join(agents) + "]")]:
        if val:
            cfg = set_key(cfg, key, val)
    if a.no_em_dash:
        cfg = set_key(cfg, "forbidden_chars", "[U+2014]")
    # pack config keys, appended inside the frontmatter
    extra = []
    for p in packs:
        fm, _ = vaultlib.read_frontmatter(os.path.join(REPO, "packs", p, "pack.md"))
        keys = fm.get("config_keys") or {}
        if keys:
            extra.append(f"\n# {p} pack")
            for k, v in keys.items():
                extra.append(f"{k}: {('[' + ', '.join(v) + ']') if isinstance(v, list) else v}")
    if extra:
        head, sep, rest = cfg[3:].partition("\n---")
        cfg = "---" + head.rstrip("\n") + "\n" + "\n".join(extra) + "\n" + sep + rest
    with open(os.path.join(sysdir, "config.md"), "w", encoding="utf-8") as fh:
        fh.write(cfg)

    conf = vaultlib.read_config(vault)
    values = {"owner_name": a.owner or "Owner", "Subject": "{Subject}"}
    tpl = os.path.join(sysdir, "templates")

    def write_from(template, dest_rel):
        dest = os.path.join(vault, dest_rel)
        if os.path.exists(dest):
            return
        os.makedirs(os.path.dirname(dest) or vault, exist_ok=True)
        with open(os.path.join(tpl, template), encoding="utf-8") as fh:
            text = fill(fh.read(), values)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(text)

    write_from("AGENTS.md", "AGENTS.md")
    write_from("task-list.md", conf.get("task_list") or "Open Actions.md")
    write_from("accomplishments.md", conf.get("accomplishments") or "_Internal/Accomplishments.md")
    write_from("feedback-received.md", conf.get("feedback_log") or "_Internal/Feedback Received.md")
    if not os.path.exists(os.path.join(vault, "AGENTS-Archive.md")):
        with open(os.path.join(vault, "AGENTS-Archive.md"), "w", encoding="utf-8") as fh:
            fh.write("# AGENTS.md archive\n\nRetired content from AGENTS.md, newest first.\n")

    for key in ("sessions_dir", "inbox_dir", "drafts_dir"):
        d = conf.get(key)
        if d:
            os.makedirs(os.path.join(vault, d), exist_ok=True)
    internal = conf.get("internal_dir") or "_Internal"
    for sub in ("1-1s", "Team Meetings", "Career", "Sources"):
        os.makedirs(os.path.join(vault, internal, sub), exist_ok=True)

    for p in packs:
        fm, _ = vaultlib.read_frontmatter(os.path.join(REPO, "packs", p, "pack.md"))
        for d in vaultlib.as_list(fm.get("subject_dirs")):
            os.makedirs(os.path.join(vault, d), exist_ok=True)
        if fm.get("portfolio_dir"):
            os.makedirs(os.path.join(vault, fm["portfolio_dir"]), exist_ok=True)

    example = os.path.join(sysdir, "local", "rules", "10-owner.md.example")
    if os.path.exists(example):
        shutil.copy2(example, os.path.join(sysdir, "local", "rules", "10-owner.md"))

    print(f"Created vault at {vault}")
    print(f"  packs: {', '.join(packs) or 'none'}   agents: {', '.join(agents)}")
    print("Next:")
    print("  1. Fill in _system/config.md and _system/local/rules/10-owner.md")
    print("  2. Connect your AI: see _system/adapters/ (Claude skill, or the any-LLM prompt)")
    print("     If your tool only reads its own rules folder, set export_*_dir in config.md and run")
    print("     python3 _system/scripts/export-agent-files.py")
    print("  Then say 'resume' to your AI.")


if __name__ == "__main__":
    main()
