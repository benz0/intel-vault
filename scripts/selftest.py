#!/usr/bin/env python3
"""
Self-test for intel-vault. Run before every commit:

    python3 scripts/selftest.py

Builds throwaway vaults in a temp folder (nothing outside it is touched) and checks:
  1. Every Python script compiles.
  2. new-vault.py builds a vault, and check-vault.py finds nothing wrong in it.
  3. export-agent-files.py writes every workflow, alias, and rule, and a second run
     changes nothing (idempotent).
  4. update-vault.py on a fresh vault reports nothing to change.
  5. new-vault.py --adopt writes only _system/ and leaves existing notes byte-identical.
  6. email-to-md.py converts a sample .eml and names it without [EXTERNAL] or RE.
  7. check-vault.py catches a planted forbidden character and a broken link, resolves
     relative and .md links, and skips raw Sources/ for characters.
  8. The repo itself: no forbidden characters in tracked or new text files (except the
     signature divider), and none of the words in .git/info/banned-words, if that
     file exists. Keep that file out of the repo; it never gets committed.

Prints PASS or FAIL per check and exits 1 on any failure. Needs only Python 3.
"""
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
EM = chr(0x2014)  # never type the character itself in this file
SIGNATURE = f"{EM} {EM} {EM}"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))


def run(*args, cwd=None):
    p = subprocess.run([PY, *args], cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def set_config(vault, **values):
    path = os.path.join(vault, "_system", "config.md")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    for key, val in values.items():
        text, n = re.subn(rf"(?m)^{key}:.*$", f"{key}: {val}", text, count=1)
        if not n:
            raise SystemExit(f"selftest: config key {key} not found in config.example.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def snapshot(folder):
    out = {}
    for d, _, files in os.walk(folder):
        for f in files:
            p = os.path.join(d, f)
            with open(p, "rb") as fh:
                out[os.path.relpath(p, folder)] = fh.read()
    return out


def main():
    tmp = tempfile.mkdtemp(prefix="intel-vault-selftest-")
    try:
        # 1. compile
        bad = []
        for d in ("core/scripts", "scripts"):
            for f in os.listdir(os.path.join(REPO, d)):
                if f.endswith(".py"):
                    try:
                        py_compile.compile(os.path.join(REPO, d, f), doraise=True, cfile=os.path.join(tmp, "x.pyc"))
                    except py_compile.PyCompileError as e:
                        bad.append(f"{f}: {e.msg}")
        check("1. scripts compile", not bad, "; ".join(bad))

        # 2. new vault, clean check
        v = os.path.join(tmp, "vault")
        code, out = run(os.path.join(REPO, "scripts", "new-vault.py"), v, "--packs", "cse", "--no-em-dash",
                        "--owner", "Test Owner", "--initials", "TO", "--tz", "America/New_York")
        check("2a. new-vault builds", code == 0 and os.path.isfile(os.path.join(v, "_system", "config.md")), out[-300:])
        code, out = run(os.path.join(v, "_system", "scripts", "check-vault.py"), "--quiet", v)
        check("2b. fresh vault checks clean", code == 0, out[-300:])

        # 3. export, twice
        write(os.path.join(v, "_system", "local", "tool-user-only.md"), "user_only: true\n")
        set_config(v, export_rules_dir=".tool/rules", export_skills_dir=".tool/skills",
                   export_commands_dir=".tool/commands", export_alias_skills="true",
                   export_user_only_frontmatter="_system/local/tool-user-only.md")
        exporter = os.path.join(v, "_system", "scripts", "export-agent-files.py")
        code, out = run(exporter, v)
        skills = set(os.listdir(os.path.join(v, ".tool", "skills")))
        need = {"resume", "wrap", "intake", "prep", "risk", "cs-update", "gainsight", "meeting-intake"}
        check("3a. export writes workflows and alias skills", code == 0 and need <= skills,
              f"missing {sorted(need - skills)}" if code == 0 else out[-300:])
        alias = os.path.join(v, ".tool", "skills", "gainsight", "SKILL.md")
        ok = os.path.isfile(alias) and "user_only: true" in open(alias, encoding="utf-8").read()
        check("3b. alias skills carry the user-only frontmatter", ok)
        code, out = run(exporter, v)
        check("3c. second export changes nothing", code == 0 and out.startswith("Wrote 0 files"), out[:200])

        # 4. update on a fresh vault
        code, out = run(os.path.join(REPO, "scripts", "update-vault.py"), v, "--dry-run")
        m = re.search(r"new: (\d+)\s+changed: (\d+)", out)
        check("4. update-vault finds nothing to change", code == 0 and m and m.groups() == ("0", "0"), out[-300:])

        # 5. adopt leaves notes alone
        a = os.path.join(tmp, "existing")
        write(os.path.join(a, "Accounts", "Acme", "Current State.md"), f"# Acme\nOld note {EM} untouched.\n")
        write(os.path.join(a, "Tasks.md"), "- [ ] something\n")
        before = snapshot(a)
        code, out = run(os.path.join(REPO, "scripts", "new-vault.py"), a, "--adopt", "--packs", "cse",
                        "--task-list", "Tasks.md")
        after = {k: val for k, val in snapshot(a).items() if not k.startswith("_system" + os.sep)}
        check("5. adopt writes only _system/", code == 0 and before == after, out[-300:])

        # 6. email conversion
        inbox = os.path.join(tmp, "inbox")
        write(os.path.join(inbox, "sample.eml"),
              "From: Pat Doe <pat@example.com>\nTo: Test Owner <owner@example.com>\n"
              "Subject: [EXTERNAL] RE: Renewal timing\nDate: Mon, 26 Oct 2026 10:00:00 -0400\n"
              "Content-Type: text/plain; charset=utf-8\n\nHello,\nThe renewal moves to November.\n")
        code, out = run(os.path.join(v, "_system", "scripts", "email-to-md.py"), inbox)
        mds = [f for f in os.listdir(inbox) if f.endswith(".md")]
        ok = code == 0 and len(mds) == 1 and "EXTERNAL" not in mds[0] and " RE " not in mds[0] \
            and "Renewal timing" in mds[0] and os.path.isfile(os.path.join(inbox, "sample.eml"))
        check("6. email-to-md converts and names cleanly", ok, f"{mds} {out[-200:]}")

        # 7. checker catches and resolves
        acct = os.path.join(v, "Accounts", "Acme")
        write(os.path.join(acct, "Account Overview.md"), "# Acme\n")
        write(os.path.join(acct, "Stakeholders", "Customer", "Pat Doe.md"), "# Pat Doe\n")
        write(os.path.join(acct, "Sources", "raw.md"), f"raw {EM} text\n")
        write(os.path.join(acct, "Meetings", "note.md"),
              f"[[Account Overview.md]] [[../Stakeholders/Customer/Pat Doe]] [[No Such File]] bad {EM} here\n")
        code, out = run(os.path.join(v, "_system", "scripts", "check-vault.py"), "--quiet", acct)
        ok = code == 1 and "Forbidden characters: 1 " in out and "Broken links: 1 " in out
        check("7. checker finds 1 character and 1 broken link, resolves the rest", ok, out[-300:])

        # 8. repo hygiene
        # tracked files plus new files not yet added (so a check before "git add" still sees them)
        files = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                               cwd=REPO, capture_output=True, text=True).stdout.split("\n")
        banned_path = os.path.join(REPO, ".git", "info", "banned-words")
        banned = []
        if os.path.isfile(banned_path):
            banned = [w.strip().lower() for w in open(banned_path, encoding="utf-8") if w.strip() and not w.startswith("#")]
        char_hits, word_hits = [], []
        for f in filter(None, files):
            p = os.path.join(REPO, f)
            if not os.path.isfile(p) or os.path.splitext(f)[1] not in (".md", ".py", ".txt", ".yaml", ".yml", ""):
                continue
            text = open(p, encoding="utf-8", errors="replace").read()
            if EM in text.replace(SIGNATURE, ""):
                char_hits.append(f)
            low = text.lower()
            for w in banned:
                if re.search(rf"\b{re.escape(w)}\b", low) or w in f.lower():
                    word_hits.append(f"{f}: {w}")
        check("8a. no forbidden characters in the repo", not char_hits, ", ".join(char_hits[:10]))
        check(f"8b. no banned words in the repo ({len(banned)} words listed)", not word_hits, ", ".join(word_hits[:10]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    failed = results.count(False)
    print(f"\n{len(results) - failed}/{len(results)} passed.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
