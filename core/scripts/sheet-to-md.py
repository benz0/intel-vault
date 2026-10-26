#!/usr/bin/env python3
"""
Convert a spreadsheet (.xlsx / .xlsm / .csv) to markdown tables.

Output is a CACHE, not a source of truth. The spreadsheet stays authoritative.
Always write into a _derived/ folder and never hand-edit the result.

Usage:
    python3 _system/scripts/sheet-to-md.py <input> [output.md]
    python3 _system/scripts/sheet-to-md.py --newest <folder> <output.md>

--newest picks the most recently dated file matching *.xlsx in the folder,
using the date in the filename (YYYY-MM-DD) and falling back to mtime.

Requires: openpyxl  (pip install openpyxl --break-system-packages)
"""
import sys, os, re, csv, glob, datetime

HEADER = """> **Generated file, do not edit.** Regenerate with `_system/scripts/sheet-to-md.py`.
> Source: `{src}`
> Generated: {when}
> The spreadsheet is authoritative. If this file and the spreadsheet disagree, the spreadsheet wins.
"""

def cell(v):
    if v is None:
        return ""
    s = str(v)
    if isinstance(v, (datetime.datetime, datetime.date)):
        s = v.strftime("%Y-%m-%d")
    return s.replace("|", "\\|").replace("\n", " ").strip()

def table(rows):
    rows = [r for r in rows if any(c.strip() for c in r)]
    if not rows:
        return ["_empty_", ""]
    width = max(len(r) for r in rows)
    rows = [(r + [""] * width)[:width] for r in rows]
    hdr, body = rows[0], rows[1:]
    out = ["| " + " | ".join(hdr) + " |", "|" + "---|" * width]
    out += ["| " + " | ".join(r) + " |" for r in body]
    out.append("")
    out.append(f"_{len(body)} rows_")
    out.append("")
    return out

def convert(path):
    out = []
    if path.lower().endswith(".csv"):
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
            out += table([[cell(c) for c in r] for r in csv.reader(fh)])
    else:
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        for ws in wb.worksheets:
            out.append(f"\n## {ws.title}\n")
            out += table([[cell(c) for c in r] for r in ws.iter_rows(values_only=True)])
    return "\n".join(out)

def newest(folder):
    best, best_key = None, None
    for f in glob.glob(os.path.join(folder, "*.xls*")):
        if os.path.basename(f).startswith(("~", ".")):
            continue
        m = re.search(r"(20\d\d)-(\d\d)-(\d\d)", os.path.basename(f))
        key = (1, m.group(0)) if m else (0, str(os.path.getmtime(f)))
        if best_key is None or key > best_key:
            best, best_key = f, key
    return best

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    if args[0] == "--newest":
        src = newest(args[1])
        if not src:
            print(f"no spreadsheet found in {args[1]}"); sys.exit(1)
        dest = args[2] if len(args) > 2 else None
    else:
        src, dest = args[0], (args[1] if len(args) > 1 else None)

    body = convert(src)
    doc = HEADER.format(src=os.path.abspath(src),
                        when=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" + body

    if dest:
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(doc)
        print(f"wrote {dest}")
        print(f"source: {os.path.basename(src)}")
        print(f"size: {len(doc):,} chars, approx {len(doc)//4:,} tokens")
    else:
        print(doc)

if __name__ == "__main__":
    main()
