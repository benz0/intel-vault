#!/usr/bin/env python3
"""
Convert saved emails (.eml or Outlook .msg) into markdown sources for intake.

Direction: email client -> vault. Save or drag a message out of your mail app
into the vault's inbox folder, then run this. The original file is kept next to
the markdown copy; intake moves both into the subject's Sources/ folder.

  .eml  Mac Outlook, Apple Mail, Thunderbird, Gmail "Download message".
        Python standard library only.
  .msg  Windows Outlook. Needs one extra package:
        pip install extract-msg   (add --break-system-packages on some systems)

Attachments are listed by name and size, never extracted or read.

Usage:
    python3 _system/scripts/email-to-md.py <file or folder> [--out <folder>]
    (a folder converts every .eml and .msg in it that has no .md yet)
"""
import datetime
import email
import email.policy
import html
import os
import re
import sys
from email.utils import getaddresses, parsedate_to_datetime


def html_to_text(s):
    s = re.sub(r"(?is)<(script|style).*?</\1>", "", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</(p|div|tr|li|h[1-6])>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def addr_list(value):
    if not value:
        return ""
    pairs = getaddresses([str(value)])
    return ", ".join(f"{n} <{a}>" if n else a for n, a in pairs if a or n)


def from_eml(path):
    with open(path, "rb") as fh:
        msg = email.message_from_binary_file(fh, policy=email.policy.default)
    body, html_body, attachments = None, None, []
    for part in msg.walk():
        if part.is_multipart():
            continue
        disp = part.get_content_disposition()
        if disp == "attachment" or (disp == "inline" and part.get_filename()):
            payload = part.get_payload(decode=True) or b""
            attachments.append((part.get_filename() or "unnamed", len(payload)))
            continue
        ctype = part.get_content_type()
        try:
            text = part.get_content()
        except Exception:
            text = (part.get_payload(decode=True) or b"").decode("utf-8", "replace")
        if ctype == "text/plain" and body is None:
            body = text
        elif ctype == "text/html" and html_body is None:
            html_body = text
    if body is None and html_body is not None:
        body = html_to_text(html_body)
    date = None
    try:
        date = parsedate_to_datetime(msg["Date"]) if msg["Date"] else None
    except (TypeError, ValueError):
        pass
    return {
        "subject": str(msg["Subject"] or "(no subject)"),
        "from": addr_list(msg["From"]),
        "to": addr_list(msg["To"]),
        "cc": addr_list(msg["Cc"]),
        "date": date,
        "body": (body or "").strip(),
        "attachments": attachments,
    }


def from_msg(path):
    try:
        import extract_msg  # type: ignore
    except ImportError:
        sys.exit("Reading .msg files needs the extract-msg package: pip install extract-msg")
    m = extract_msg.Message(path)
    try:
        date = m.date if isinstance(m.date, datetime.datetime) else None
        if date is None and m.date:
            try:
                date = parsedate_to_datetime(str(m.date))
            except (TypeError, ValueError):
                date = None
        body = m.body or ""
        if not body.strip() and getattr(m, "htmlBody", None):
            hb = m.htmlBody
            body = html_to_text(hb.decode("utf-8", "replace") if isinstance(hb, bytes) else hb)
        atts = []
        for a in m.attachments:
            name = getattr(a, "longFilename", None) or getattr(a, "shortFilename", None) or "unnamed"
            data = getattr(a, "data", b"") or b""
            atts.append((name, len(data) if isinstance(data, (bytes, bytearray)) else 0))
        return {
            "subject": m.subject or "(no subject)",
            "from": m.sender or "",
            "to": m.to or "",
            "cc": m.cc or "",
            "date": date,
            "body": body.strip(),
            "attachments": atts,
        }
    finally:
        m.close()


def clean(s):
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", str(s or ""))


def safe(s, n=60):
    s = clean(s)
    # drop leading tags like [EXTERNAL] and reply/forward prefixes, in any order
    s = re.sub(r"^((\[[^\]\s]{1,15}\]|\b(re|fw|fwd)\s*:)\s*)+", "", s.strip(), flags=re.I)
    s = re.sub(r"[\\/:*?\"<>|\r\n\t]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()[:n].strip() or "no subject"


def convert(path, out_dir):
    data = from_msg(path) if path.lower().endswith(".msg") else from_eml(path)
    data = {k: (clean(v) if isinstance(v, str) else v) for k, v in data.items()}
    d = data["date"]
    local = d.astimezone() if d else None
    day = local.strftime("%Y-%m-%d") if local else "undated"
    sender = data["from"].split("<")[0].strip().strip('"') or data["from"]
    who = safe(sender, 30) if clean(sender).strip() else "unknown sender"
    name = f"{day} Email {who} {safe(data['subject'])}.md"
    dest = os.path.join(out_dir, name)
    atts = "\n".join(f"- {n} ({s:,} bytes, not ingested)" for n, s in data["attachments"]) or "- none"
    when = local.strftime("%Y-%m-%d %H:%M %Z") if local else "unknown"
    text = (
        f"# Source: Email, {data['subject']}\n"
        f"# Date: {when}\n"
        f"# Type: email\n"
        f"# Captured by: saved from the mail client; converted by email-to-md.py\n"
        f"# Original file: {os.path.basename(path)}\n\n"
        f"**From:** {data['from']}\n"
        f"**To:** {data['to']}\n"
        + (f"**Cc:** {data['cc']}\n" if data["cc"] else "")
        + f"**Subject:** {data['subject']}\n\n"
        f"**Attachments:**\n{atts}\n\n"
        f"---\n\n{data['body']}\n"
    )
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(text)
    return dest


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    out = None
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        args = args[:i] + args[i + 2:]
    target = args[0]
    files = []
    if os.path.isdir(target):
        for f in sorted(os.listdir(target)):
            if f.lower().endswith((".eml", ".msg")):
                files.append(os.path.join(target, f))
    else:
        files = [target]
    if not files:
        print("No .eml or .msg files found.")
        return
    done = 0
    for f in files:
        dest = convert(f, out or os.path.dirname(os.path.abspath(f)))
        print(f"  {os.path.basename(f)} -> {os.path.basename(dest)}")
        done += 1
    print(f"Converted {done} email(s). Originals kept. Run intake to file them.")


if __name__ == "__main__":
    main()
