#!/usr/bin/env python3
"""
Omni‑Scour Local Agent (Single‑File)
------------------------------------

Purpose
  • Launches a real browser via Playwright.
  • You log in *manually* to each platform (no credential handling by this script).
  • After you confirm login, the agent extracts your full chat history (text) using in‑context
    authenticated requests and/or robust DOM fallbacks.
  • Saves everything to one structured JSON file.

Supported (first‑class) platforms
  • chatgpt / chat.openai.com / chatgpt.com (ChatGPT)
  • claude.ai (Claude)

Design Principles
  • You retain control: manual login + explicit confirmation before any extraction.
  • Read‑only: never posts, deletes, or modifies.
  • Conservative rate‑limits + error handling to reduce flakiness.
  • Outputs a single, portable JSON codex you can hand back to Scour 🧠.

🚨 Important
  • Review each website’s Terms of Service and legal restrictions where you live before using.
  • Prefer built‑in export tools when available; this agent is for your own data in your own accounts.

Quickstart
  python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\\Scripts\\activate)
  pip install --upgrade playwright
  python -m playwright install
  python omni_scour_local_agent.py --platforms chatgpt,claude --output codex.json

Then:
  • A browser opens per platform.
  • Log in normally. When the site shows you as signed in, return to the terminal and hit ENTER.
  • The agent fetches all conversations and writes them to your output JSON.

JSON Shape (example)
{
  "exported_at": "2025-09-16T20:15:00Z",
  "host": "omni-scour-local-agent",
  "platforms": {
    "chatgpt": {
      "account_hint": "email@domain.tld",
      "conversations": [
        {"id": "abc", "title": "Trip plan", "created": 1710200000, "updated": 1710210000,
         "messages": [{"role": "user", "text": "Hi"}, {"role": "assistant", "text": "Hello"}]}
      ]
    },
    "claude": { ... }
  }
}

"""

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from playwright.async_api import async_playwright, Page, BrowserContext

# --------- Utilities ---------

def now_iso() -> str:
    import datetime as _dt
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

async def press_enter_to_continue(prompt: str = "\nWhen you're fully logged in on this platform, press ENTER to continue..."):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: input(prompt))

async def goto_any(page: Page, urls: List[str]) -> str:
    for u in urls:
        try:
            resp = await page.goto(u, wait_until="domcontentloaded", timeout=60_000)
            if resp is not None and (200 <= resp.status < 400):
                return u
        except Exception:
            pass
    # last try without status check
    await page.goto(urls[0], wait_until="domcontentloaded")
    return urls[0]

async def safe_eval(page: Page, script: str, arg: Any = None, timeout: int = 120_000):
    return await page.evaluate(script, arg, timeout=timeout)

async def ensure_network_idle(page: Page, quiet_ms: int = 1200, max_wait_ms: int = 15_000):
    start = time.time()
    last = time.time()
    while True:
        await asyncio.sleep(0.3)
        try:
            # a light heuristic: wait for networkidle if available, else time windows
            await page.wait_for_load_state("networkidle", timeout=quiet_ms)
            return
        except Exception:
            pass
        if (time.time() - start) * 1000 > max_wait_ms:
            return

# --------- ChatGPT Extractor ---------

async def extract_chatgpt(page: Page) -> Dict[str, Any]:
    """Extract conversations from ChatGPT (chatgpt.com/chat.openai.com)."""
    base = await goto_any(page, ["https://chatgpt.com/", "https://chat.openai.com/"])
    print(f"Opened: {base}")
    print("\n➡️  Please log in to ChatGPT in the opened browser window.")
    await press_enter_to_continue()
    await ensure_network_idle(page)

    # Attempt to read account hint (email) from UI if present
    account_hint = None
    try:
        # Some builds show user email in account menu aria-label; keep best-effort only
        account_hint = await page.evaluate("""
            () => {
              const el = document.querySelector('[data-testid="user-menu-button"]') || document.querySelector('[aria-label*="Account"]');
              return el?.textContent?.trim() || null;
            }
        """)
    except Exception:
        pass

    # Fetch conversation list via authenticated internal API
    print("Gathering conversation index…")
    try:
        convos = await safe_eval(page, """
            async () => {
              const all = [];
              let offset = 0;
              const limit = 100;
              for (let i=0;i<1000;i++) { // hard cap safety
                const r = await fetch(`/backend-api/conversations?offset=${offset}&limit=${limit}`, {credentials:'include'});
                if (!r.ok) throw new Error('index status '+r.status);
                const j = await r.json();
                const items = j.items || j.conversations || [];
                all.push(...items);
                const hasNext = (typeof j.has_next_page !== 'undefined') ? j.has_next_page : (items.length === limit);
                if (!hasNext) break;
                offset += limit;
              }
              return all.map(x => ({
                id: x.id || x.conversation_id || x.uuid || null,
                title: x.title || null,
                create_time: x.create_time || x.created_at || null,
                update_time: x.update_time || x.updated_at || null,
              }));
            }
        """)
    except Exception as e:
        print("⚠️  Failed to list conversations via API:", e)
        convos = []

    # If API path fails (UI/layout changes), fallback: scrape sidebar
    if not convos:
        print("Falling back to sidebar scraping (may be partial)…")
        try:
            await page.wait_for_timeout(1500)
            # Try to open sidebar if collapsed
            try:
                btn = page.locator('button:has-text("Show sidebar")')
                if await btn.count() > 0:
                    await btn.first.click()
                    await page.wait_for_timeout(500)
            except Exception:
                pass
            # Aggregate visible conversation links
            links = await page.locator('nav a, [data-testid="conversations"] a').all()
            convos = []
            seen = set()
            for a in links:
                href = await a.get_attribute('href')
                title = (await a.text_content() or '').strip() or None
                if href and '/c/' in href and href not in seen:
                    seen.add(href)
                    convos.append({"id": href.split('/c/')[-1], "title": title, "create_time": None, "update_time": None})
        except Exception:
            pass

    # Fetch each conversation detail
    results = []
    print(f"Found {len(convos)} ChatGPT conversations. Fetching details…")
    for i, c in enumerate(convos, 1):
        cid = c.get("id")
        if not cid:
            continue
        print(f"  [{i}/{len(convos)}] {cid} …")
        try:
            detail = await safe_eval(page, """
                async (cid) => {
                  const r = await fetch(`/backend-api/conversation/${cid}`, {credentials:'include'});
                  if (!r.ok) return {__error: 'status '+r.status};
                  const d = await r.json();
                  const mapping = d.mapping || {};
                  const nodes = Object.values(mapping).filter(n => n && n.message);
                  const msgs = nodes.map(n => {
                    const m = n.message || {};
                    const role = (m.author && m.author.role) || null;
                    let text = '';
                    const c = m.content;
                    if (!c) text='';
                    else if (Array.isArray(c.parts)) text = c.parts.filter(Boolean).join('\n');
                    else if (Array.isArray(c)) text = c.map(p => (p?.text) ? p.text : (typeof p==='string'?p:'')).join('\n');
                    else if (typeof c.text === 'string') text = c.text;
                    const ts = m.create_time || m.end_turn || m.update_time || null;
                    return { role, text, ts };
                  }).filter(x => x.text && (x.role==='user' || x.role==='assistant'));

                  // Sort by timestamp if present, else keep original
                  msgs.sort((a,b) => ((a.ts||0) - (b.ts||0)));

                  return {
                    id: d.conversation_id || d.id || cid,
                    title: d.title || null,
                    create_time: d.create_time || null,
                    update_time: d.update_time || null,
                    messages: msgs
                  };
                }
            """, cid)
            if isinstance(detail := detail, dict) and not detail.get("__error"):
                # overlay sidebar title/times if API missing
                if not detail.get("title") and c.get("title"):
                    detail["title"] = c.get("title")
                results.append(detail)
            else:
                results.append({"id": cid, "title": c.get("title"), "error": detail.get("__error") if isinstance(detail, dict) else "unknown"})
        except Exception as e:
            results.append({"id": cid, "title": c.get("title"), "error": str(e)})
        await asyncio.sleep(0.15)

    return {
        "account_hint": account_hint,
        "conversations": results,
    }

# --------- Claude Extractor ---------

async def extract_claude(page: Page) -> Dict[str, Any]:
    base = await goto_any(page, ["https://claude.ai/"])
    print(f"Opened: {base}")
    print("\n➡️  Please log in to Claude in the opened browser window.")
    await press_enter_to_continue()
    await ensure_network_idle(page)

    # Discover orgs
    print("Discovering organizations…")
    orgs = []
    try:
        orgs = await safe_eval(page, """
            async () => {
              const r = await fetch('/api/organizations', {credentials:'include'});
              if (!r.ok) throw new Error('orgs status '+r.status);
              const j = await r.json();
              return (Array.isArray(j) ? j : (j?.organizations || [])).map(x => ({uuid: x.uuid || x.id, name: x.name || null}));
            }
        """)
    except Exception as e:
        print("⚠️  Could not load organizations:", e)

    if not orgs:
        print("Trying to proceed without explicit org (single‑org assumption)…")
        orgs = [{"uuid": "default", "name": None}]

    all_convos: List[Dict[str, Any]] = []

    for org in orgs:
        org_uuid = org.get("uuid")
        print(f"Listing conversations for org {org_uuid}…")
        try:
            convos = await safe_eval(page, """
                async (orgUuid) => {
                  const limit = 100; let offset = 0; const out = [];
                  for (let i=0;i<1000;i++) {
                    const path = orgUuid && orgUuid!=='default'
                      ? `/api/organizations/${orgUuid}/chat_conversations?offset=${offset}&limit=${limit}`
                      : `/api/organizations/chat_conversations?offset=${offset}&limit=${limit}`; // fallback
                    const r = await fetch(path, {credentials:'include'});
                    if (!r.ok) throw new Error('index status '+r.status);
                    const j = await r.json();
                    const arr = Array.isArray(j) ? j : (j?.items || j?.conversations || []);
                    out.push(...arr.map(x => ({ uuid: x.uuid || x.id || x.conversation_id, name: x.name || x.title || null }))); 
                    if (arr.length < limit) break; offset += limit;
                  }
                  return out;
                }
            """, org_uuid)
        except Exception as e:
            print("⚠️  Conversation index error:", e)
            convos = []

        print(f"Found {len(convos)} Claude conversations in org {org_uuid}. Fetching details…")
        for i, co in enumerate(convos, 1):
            cuid = co.get("uuid")
            if not cuid:
                continue
            print(f"  [{i}/{len(convos)}] {cuid} …")
            try:
                detail = await safe_eval(page, """
                    async ({orgUuid, cuid}) => {
                      const path = orgUuid && orgUuid!=='default'
                        ? `/api/organizations/${orgUuid}/chat_conversations/${cuid}`
                        : `/api/organizations/chat_conversations/${cuid}`; // fallback
                      const r = await fetch(path, {credentials:'include'});
                      if (!r.ok) return {__error: 'status '+r.status};
                      const d = await r.json();
                      const name = d.name || d.title || null;
                      const messages = (d.chat_messages || d.messages || d || []).map(m => {
                        const role = m.sender || m.role || m.from || null;
                        let text = '';
                        const c = m.content || m.text || m.parts || null;
                        if (typeof c === 'string') text = c;
                        else if (Array.isArray(c)) text = c.map(p => p?.text || (typeof p==='string'?p:'')).join('\n');
                        else if (c && typeof c === 'object' && typeof c.text === 'string') text = c.text;
                        const ts = m.created_at || m.create_time || m.updated_at || m.ts || null;
                        return { role, text, ts };
                      }).filter(x => x.text && (x.role==='user' or x.role=='assistant' or x.role=='system'));
                      return { id: d.uuid || d.id || cuid, title: name, messages };
                    }
                """, {"orgUuid": org_uuid, "cuid": cuid})
                if isinstance(detail, dict) and not detail.get("__error"):
                    all_convos.append(detail)
                else:
                    all_convos.append({"id": cuid, "title": co.get("name"), "error": detail.get("__error") if isinstance(detail, dict) else "unknown"})
            except Exception as e:
                all_convos.append({"id": cuid, "title": co.get("name"), "error": str(e)})
            await asyncio.sleep(0.15)

    return {
        "account_hint": None,
        "conversations": all_convos,
    }

# --------- Orchestration ---------

SUPPORTED = {
    "chatgpt": extract_chatgpt,
    "chat.openai.com": extract_chatgpt,
    "chatgpt.com": extract_chatgpt,
    "claude": extract_claude,
    "claude.ai": extract_claude,
}

async def run_for_platform(ctx: BrowserContext, platform: str) -> Dict[str, Any]:
    plat = platform.strip().lower()
    if plat not in SUPPORTED:
        raise ValueError(f"Unsupported platform: {platform}")
    page = await ctx.new_page()
    try:
        return await SUPPORTED[plat](page)
    finally:
        await page.close()

async def main_async(args):
    platforms = [p.strip() for p in args.platforms.split(',') if p.strip()]
    user_data_dir = Path(args.user_data_dir).expanduser().resolve()
    user_data_dir.mkdir(parents=True, exist_ok=True)

    print("Launching browser…")
    async with async_playwright() as pw:
        browser = await pw.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=args.headless,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        try:
            bundle: Dict[str, Any] = {
                "exported_at": now_iso(),
                "host": "omni-scour-local-agent",
                "platforms": {},
            }

            for plat in platforms:
                print(f"\n==============================\n>>> {plat} <<<\n==============================")
                try:
                    data = await run_for_platform(browser, plat)
                    bundle["platforms"][plat.split('.')[-1]] = data
                except Exception as e:
                    print(f"❌ {plat} failed: {e}")
                    bundle["platforms"][plat.split('.')[-1]] = {"error": str(e)}

            out_path = Path(args.output).expanduser().resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with out_path.open('w', encoding='utf-8') as f:
                json.dump(bundle, f, ensure_ascii=False, indent=2)
            print(f"\n✅ Done. Wrote {out_path}")
        finally:
            await browser.close()

def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="Omni‑Scour Local Agent")
    ap.add_argument("--platforms", default="chatgpt,claude",
                    help="Comma‑separated list, e.g., 'chatgpt,claude' or hostnames like 'chat.openai.com' ")
    ap.add_argument("--output", default="omni_scour_codex.json", help="Output JSON file path")
    ap.add_argument("--user-data-dir", default=".omni_scour_profile", help="Persistent browser profile dir")
    ap.add_argument("--headless", action="store_true", help="Run browser headless (not recommended for manual login)")
    return ap.parse_args(argv)

def main():
    args = parse_args()
    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(2)

if __name__ == "__main__":
    main()
