# -*- coding: utf-8 -*-
"""
Extract system prompts / tool definitions / skill blocks from a PrismCat
instance's captured logs, deduplicate them into groups, and generate
markdown documentation.

Usage:
    set PRISMCAT_BASE=http://<prismcat-host>:8080
    set PRISMCAT_PASSWORD=<your-console-password>
    python extract_prompts.py

Requires a running PrismCat (https://github.com/paopaoandlingyia/PrismCat)
with captured traffic. Output goes to ./extracted/.
"""
import json, hashlib, os, sys, io
from pathlib import Path
from urllib import request as urlreq
from http.cookiejar import CookieJar

BASE = os.environ.get("PRISMCAT_BASE", "http://<prismcat-host>:8080")
PWD = os.environ.get("PRISMCAT_PASSWORD", "<your-console-password>")
OUT = Path("extracted")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

cj = CookieJar()
opener = urlreq.build_opener(urlreq.HTTPCookieProcessor(cj))

def api(path, data=None):
    req = urlreq.Request(BASE + path)
    if data is not None:
        req.data = json.dumps(data).encode()
        req.add_header("content-type", "application/json")
    with opener.open(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))

def walk_list(o):
    if isinstance(o, list) and (not o or isinstance(o[0], dict)):
        return o
    if isinstance(o, dict):
        for v in o.values():
            r = walk_list(v)
            if r is not None:
                return r
    return None

api("/api/auth/login", {"password": PWD})

# ---- 1. Fetch the full log list (offset pagination; the API caps at 50/page) ----
logs, seen = [], set()
for offset in range(0, 5000, 50):
    items = walk_list(api(f"/api/logs?offset={offset}&per_page=50")) or []
    new = [it for it in items if it.get("id") not in seen]
    for it in new:
        seen.add(it.get("id"))
        logs.append(it)
    if len(items) < 50:
        break
print(f"total logs: {len(logs)}")

# ---- 2. Fetch each log's detail; group by hash of (system + tools) ----
groups = {}
for n, it in enumerate(logs, 1):
    lid = it["id"]
    try:
        d = api(f"/api/logs/{lid}")
    except Exception as e:
        print(f"  skip {lid}: {e}")
        continue
    try:
        body = json.loads(d.get("request_body") or "")
    except Exception:
        continue
    if not isinstance(body, dict) or "messages" not in body:
        continue

    sysfield = body.get("system")
    if isinstance(sysfield, list):
        systext = "\n\n".join(b.get("text", "") for b in sysfield if isinstance(b, dict))
    elif isinstance(sysfield, str):
        systext = sysfield
    else:
        systext = ""
    tools = [t for t in (body.get("tools") or []) if isinstance(t, dict)]
    toolnames = [t.get("name", "") for t in tools]

    key = hashlib.sha1((systext + "|" + ",".join(toolnames)).encode()).hexdigest()[:8]
    g = groups.setdefault(key, {
        "system": systext, "tools": tools, "requests": [],
        "sessions": set(), "agents": set(),
        "first": None, "last": None, "skill_blocks": [], "sample": None,
        "max_tokens": set(),
    })
    g["requests"].append(lid)
    if body.get("max_tokens") is not None:
        g["max_tokens"].add(body["max_tokens"])
    ts = d.get("created_at") or it.get("created_at")
    if not g["first"]:
        g["first"] = ts
    g["last"] = ts
    mu = (body.get("metadata") or {}).get("user_id")
    if mu:
        try:
            sid = json.loads(mu).get("session_id")
            if sid:
                g["sessions"].add(sid)
        except Exception:
            pass
    hdrs = d.get("request_headers") or {}
    if isinstance(hdrs, dict):
        for k, v in hdrs.items():
            if k.lower() == "user-agent":
                g["agents"].add(str(v)[:100])

    # Collect text blocks mentioning skills (from system or message reminders)
    if len(g["skill_blocks"]) < 3:
        candidates = []
        if "skill" in systext.lower():
            candidates.append(("system", systext))
        for m in body.get("messages", []):
            c = m.get("content")
            blocks = c if isinstance(c, list) else [{"type": "text", "text": str(c)}]
            for b in blocks:
                if isinstance(b, dict) and b.get("type") == "text":
                    t = b.get("text", "")
                    if "skill" in t.lower() and len(t) > 100:
                        candidates.append((f"message[{m.get('role')}]", t))
        for src, t in candidates:
            if len(g["skill_blocks"]) >= 3:
                break
            if not any(t[:200] == existing[1][:200] for existing in g["skill_blocks"]):
                g["skill_blocks"].append((src, t[:8000]))

    # No-system requests: keep a sample of the first user message
    if not systext and g["sample"] is None:
        m0 = body["messages"][0] if body["messages"] else {}
        c = m0.get("content")
        if isinstance(c, list):
            g["sample"] = "\n".join(x.get("text", "") for x in c
                                    if isinstance(x, dict) and x.get("type") == "text")[:3000]
        else:
            g["sample"] = str(c)[:3000]
    if n % 20 == 0:
        print(f"  processed {n}/{len(logs)}")

print(f"unique (system+tools) groups: {len(groups)}")

# ---- 3. Label and write documentation ----
def label(g):
    tn = ",".join(t.get("name", "") for t in g["tools"])
    s = g["system"]
    if g["max_tokens"] == {1}:
        return "token-probe"          # max_tokens=1: token-counting probes
    if "ccd" in tn or "Claude Agent SDK" in s:
        return "ccd-desktop"
    if "Claude Code" in s:
        return "claude-code"
    if not s:
        return "no-system"
    return "other"

OUT.mkdir(exist_ok=True)
index_rows = []
for idx, (key, g) in enumerate(sorted(groups.items(), key=lambda kv: -(len(kv[1]["system"]))), 1):
    lab = label(g)
    folder = OUT / f"{idx:02d}-{lab}-{key}"
    folder.mkdir(exist_ok=True)

    if g["system"]:
        (folder / "system-prompt.md").write_text(
            f"# System prompt ({lab} / {key})\n\n"
            f"> Extracted from PrismCat logs; {len(g['requests'])} requests used this prompt.\n\n---\n\n"
            + g["system"], encoding="utf-8")

    if g["tools"]:
        parts = [f"# Tool definitions ({lab} / {key}) — {len(g['tools'])} tools\n"]
        for t in g["tools"]:
            parts.append(f"\n## `{t.get('name','?')}`\n")
            parts.append((t.get("description") or "") + "\n")
            schema = t.get("input_schema") or t.get("parameters")
            if schema:
                parts.append("\n**input_schema:**\n\n```json\n"
                             + json.dumps(schema, ensure_ascii=False, indent=2) + "\n```\n")
        (folder / "tools.md").write_text("".join(parts), encoding="utf-8")

    if g["skill_blocks"]:
        parts = [f"# Skill-related content ({lab} / {key})\n"]
        for src, t in g["skill_blocks"]:
            parts.append(f"\n## Source: {src}\n\n```\n{t}\n```\n")
        (folder / "skills.md").write_text("".join(parts), encoding="utf-8")

    if g["sample"]:
        (folder / "sample-message.md").write_text(
            f"# Request message sample ({lab} / {key})\n\n"
            "These requests carry no system field; the prompt lives in the message body:\n\n---\n\n"
            + g["sample"], encoding="utf-8")

    meta = {
        "hash": key, "label": lab,
        "request_count": len(g["requests"]),
        "max_tokens": sorted(g["max_tokens"]),
        "session_ids": sorted(g["sessions"]),
        "user_agents": sorted(g["agents"]),
        "first_seen": g["first"], "last_seen": g["last"],
        "system_chars": len(g["system"]), "tool_count": len(g["tools"]),
        "request_ids": g["requests"],
    }
    (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    index_rows.append(meta)
    print(f"  [{idx:02d}] {lab:<12} {key}  system={len(g['system']):>7} chars  tools={len(g['tools']):>3}  requests={len(g['requests'])}")

# ---- 4. Index ----
lines = ["# PrismCat extraction index\n",
         f"> {len(logs)} logs deduplicated into {len(groups)} (system+tools) groups.\n\n",
         "| # | Label | Hash | System size | Tools | Requests | Folder |\n",
         "|---|-------|------|-------------|-------|----------|--------|\n"]
for i, m in enumerate(index_rows, 1):
    lines.append(f"| {i} | {m['label']} | {m['hash']} | {m['system_chars']} | "
                 f"{m['tool_count']} | {m['request_count']} | "
                 f"{i:02d}-{m['label']}-{m['hash']} |\n")
(OUT / "README.md").write_text("".join(lines), encoding="utf-8")
print("done ->", OUT)
