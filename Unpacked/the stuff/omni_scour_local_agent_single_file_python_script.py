#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Omni-Scour Local Agent — single-file Python script
Version: 1.2.0 (2025-09-15)
Author: 🧠 (GPT-5 Thinking)

Purpose
-------
Automate browser-assisted export of your personal AI chat histories across multiple
platforms by guiding you to authenticate manually (no credentials handled by the script),
then programmatically enumerating conversations and extracting the text content of each
thread. Results are saved to a single JSON file grouped by platform.

Supported (built-in) targets
----------------------------
- chat.openai.com (ChatGPT; also handles chatgpt.com redirects)
- claude.ai (Claude)
- poe.com (Poe) — best-effort, generic selectors

You can also point it at other domains using the generic scraper mode.

Important notes
---------------
• Use this only for accounts and conversations you own or have rights to export.
• Respect each site's Terms of Service and robots rules. This script uses your logged-in
  browser session and reads the page DOM like a human would, but automated scraping may
  still be disallowed by a site's TOS.
• The script requires you to log in manually in a real browser window; it does not ever
  ask for or store usernames/passwords.

Quick start
-----------
1) Python 3.10+
2) pip install playwright rich
3) playwright install
4) Run (example):
   python omni_scour_local_agent.py --platforms chat.openai.com claude.ai --max-conversations 500

Output: omni_scour_dump_YYYYMMDD_HHMMSS.json in the working directory.

"""
from __future__ import annotations

import argparse
import asyncio
import contextlib
import dataclasses
import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from rich import print as rprint
from rich.console import Console
from rich.table import Table

try:
    from playwright.async_api import async_playwright, BrowserContext, Page
except Exception as e:  # pragma: no cover
    print("\n[!] Playwright is required. Install with: pip install playwright\nThen run: playwright install\n")
    raise

# ------------------------------ Utilities ------------------------------------

SCRIPT_NAME = Path(__file__).name
DEFAULT_PROFILE_DIR = Path("profiles").resolve()
DEFAULT_HEADLESS = False
DEFAULT_TIMEOUT_MS = 20_000
DEFAULT_NAVIGATION_TIMEOUT_MS = 45_000
SCROLL_PAUSE_SEC = 0.4
MAX_SCROLL_ROUNDS = 50

@dataclass
class Message:
    role: str
    text: str

@dataclass
class Conversation:
    id: str  # usually the URL (stable, unique enough)
    url: str
    title: Optional[str]
    messages: List[Message]
    scraped_at_utc: str

@dataclass
class PlatformDump:
    platform: str
    conversations: List[Conversation]

@dataclass
class OmniDump:
    metadata: Dict[str, Any]
    platforms: Dict[str, PlatformDump]

# ----------------------------- Helper funcs -----------------------------------

async def prompt_user(prompt: str) -> None:
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: input(prompt))

async def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def sanitize_filename(name: str) -> str:
    return re.sub(r"[^-_.() a-zA-Z0-9]", "_", name)[:200]

async def robust_scroll(page: Page, rounds: int = MAX_SCROLL_ROUNDS, pause: float = SCROLL_PAUSE_SEC) -> None:
    # Scroll the main document to try to force lazy-loaded content to appear
    for _ in range(rounds):
        await page.evaluate("window.scrollBy(0, document.documentElement.scrollHeight)")
        await asyncio.sleep(pause)

async def collect_unique_links(page: Page, pattern: str) -> List[str]:
    js = f"""
    const hrefs = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
    const re = new RegExp({json.dumps(pattern)});
    const matches = hrefs.filter(h => re.test(h));
    return Array.from(new Set(matches));
    """
    try:
        links = await page.evaluate(js)
        return list(links or [])
    except Exception:
        return []

async def extract_text_blocks(page: Page, selectors: List[str]) -> List[Tuple[str, str]]:
    """Return list of (role, text). Tries multiple selector strategies.
    Role inference is best-effort."
    candidate_roles = [
        ("[data-message-author-role]", "attr"),
        ("[data-author]", "attr"),
        ("[data-testid]", "attr"),
        ("article", "tag"),
        ("div", "tag"),
    ]

    messages: List[Tuple[str, str]] = []

    # Primary, targeted selectors first
    for sel in selectors:
        try:
            loc_count = await page.locator(sel).count()
            if loc_count == 0:
                continue
            for i in range(loc_count):
                loc = page.locator(sel).nth(i)
                # Try to infer role from attributes
                role = "assistant"
                with contextlib.suppress(Exception):
                    val = await loc.get_attribute("data-message-author-role")
                    if val:
                        role = val
                with contextlib.suppress(Exception):
                    val = await loc.get_attribute("data-author")
                    if val and val.lower() in {"user", "assistant", "system"}:
                        role = val.lower()
                with contextlib.suppress(Exception):
                    val = await loc.get_attribute("data-testid")
                    if val:
                        if "user" in val.lower():
                            role = "user"
                        elif "assistant" in val.lower() or "ai" in val.lower():
                            role = "assistant"
                text = (await loc.inner_text()).strip()
                if text:
                    messages.append((role, text))
        except Exception:
            continue

    # If still empty, fall back to any element that *looks* like a message bubble
    if not messages:
        try:
            bubbles = page.locator("main *, [role='main'] *")
            cnt = await bubbles.count()
            for i in range(min(cnt, 400)):
                t = (await bubbles.nth(i).inner_text()).strip()
                if t and len(t.split()) > 2:
                    messages.append(("unknown", t))
        except Exception:
            pass

    # Deduplicate consecutive duplicates
    deduped: List[Tuple[str, str]] = []
    for role, text in messages:
        if not deduped or deduped[-1][1] != text:
            deduped.append((role, text))
    return deduped

# --------------------------- Scraper base class -------------------------------

class BaseScraper:
    name = "generic"
    start_url = None  # override
    convo_url_regex = r"/chat|/c/|/conversation"  # override if known
    message_selectors: List[str] = []  # override with best-known selectors

    def __init__(self, platform: str, context: BrowserContext, headless: bool):
        self.platform = platform
        self.context = context
        self.headless = headless

    async def ensure_ready(self) -> Page:
        page = await self.context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT_MS)
        page.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT_MS)
        base = self.start_url or f"https://{self.platform}"
        await page.goto(base)
        await asyncio.sleep(0.8)
        return page

    async def authenticate(self) -> None:
        page = await self.ensure_ready()
        console_msg = (
            f"\n[bold cyan]Login required:[/bold cyan] Please log in to [yellow]{self.platform}[/yellow] in the opened browser.\n"
            "Complete 2FA if prompted. Once you can see your chat history, return here and press Enter.\n"
        )
        await prompt_user(console_msg)
        await page.close()

    async def collect_conversation_urls(self) -> List[str]:
        page = await self.ensure_ready()
        # Attempt to visit a likely history page; subclasses may override
        with contextlib.suppress(Exception):
            await page.goto(f"https://{self.platform}")
            await asyncio.sleep(0.6)
        # Scroll & collect
        await robust_scroll(page)
        links = await collect_unique_links(page, self.convo_url_regex)
        await page.close()
        return links

    async def scrape_one_conversation(self, url: str) -> Conversation:
        page = await self.context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT_MS)
        page.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT_MS)
        await page.goto(url)
        await robust_scroll(page, rounds=20)
        title = None
        with contextlib.suppress(Exception):
            title = await page.title()
        # Use best-known selectors for this platform; fall back to heuristics
        raw_pairs = await extract_text_blocks(page, self.message_selectors)
        messages = [Message(role=r, text=t) for (r, t) in raw_pairs]
        await page.close()
        return Conversation(
            id=url,
            url=url,
            title=title,
            messages=messages,
            scraped_at_utc=now_iso(),
        )

# -------------------------- Platform-specific scrapers ------------------------

class ChatGPTScraper(BaseScraper):
    name = "chat.openai.com"
    start_url = "https://chat.openai.com/"  # will also handle chatgpt.com via redirect
    convo_url_regex = r"https?:\/\/(chat\.openai\.com|chatgpt\.com)\/c\/[-a-z0-9]+"
    message_selectors = [
        # Common ChatGPT structures
        "[data-message-author-role]",
        "[data-testid='conversation-turn']",
        "div.markdown",
        "article",
    ]

    async def collect_conversation_urls(self) -> List[str]:
        page = await self.ensure_ready()
        # Make the UI more likely to load the left sidebar fully
        await page.set_viewport_size({"width": 1440, "height": 1100})
        # The root app shows sidebar with links (virtualized). Try to expand it by scrolling the sidebar and main.
        await robust_scroll(page, rounds=10)
        # Attempt to force-load sidebar by hovering/clicking
        with contextlib.suppress(Exception):
            await page.mouse.move(40, 200)
            await asyncio.sleep(0.2)
            await page.mouse.wheel(0, 3000)
        links = await collect_unique_links(page, self.convo_url_regex)
        # If very few links, try opening the history pane explicitly via keyboard
        if len(links) < 5:
            with contextlib.suppress(Exception):
                await page.keyboard.press("Alt+h")
                await asyncio.sleep(0.5)
                await robust_scroll(page, rounds=15)
                links = await collect_unique_links(page, self.convo_url_regex)
        await page.close()
        return links

class ClaudeScraper(BaseScraper):
    name = "claude.ai"
    start_url = "https://claude.ai/chats"
    convo_url_regex = r"https?:\/\/claude\.ai\/chat\/[-a-z0-9]+"
    message_selectors = [
        "[data-testid='chat-message']",
        "[data-testid^='message-']",
        "[data-author]",
        "article",
    ]

    async def collect_conversation_urls(self) -> List[str]:
        page = await self.ensure_ready()
        await page.goto(self.start_url)
        await page.wait_for_load_state("domcontentloaded")
        await robust_scroll(page, rounds=30)
        links = await collect_unique_links(page, self.convo_url_regex)
        await page.close()
        return links

class PoeScraper(BaseScraper):
    name = "poe.com"
    start_url = "https://poe.com/"
    convo_url_regex = r"https?:\/\/poe\.com\/[^?#]+\?[^#]*(message|chat)\="  # best-effort
    message_selectors = [
        "[data-testid*='Message']",
        "[class*='message']",
        "article",
    ]

# ------------------------------- Factory --------------------------------------

SCRAPER_MAP = {
    "chat.openai.com": ChatGPTScraper,
    "chatgpt.com": ChatGPTScraper,
    "claude.ai": ClaudeScraper,
    "poe.com": PoeScraper,
}

# ------------------------------- Main logic -----------------------------------

async def scrape_platform(platform: str, context: BrowserContext, headless: bool, max_conversations: Optional[int]) -> PlatformDump:
    ScraperCls = SCRAPER_MAP.get(platform, BaseScraper)
    scraper = ScraperCls(platform, context, headless)

    rprint(f"\n[bold]→ {platform}[/bold]: Starting authentication check…")
    await scraper.authenticate()

    rprint("  • Enumerating conversations… (scrolling and collecting links)")
    urls = await scraper.collect_conversation_urls()
    urls = list(dict.fromkeys(urls))  # dedupe, preserve order

    if max_conversations:
        urls = urls[:max_conversations]

    rprint(f"  • Found [cyan]{len(urls)}[/cyan] conversation URLs to scrape.")

    conversations: List[Conversation] = []
    for idx, url in enumerate(urls, 1):
        rprint(f"    [{idx}/{len(urls)}] Scraping: {url}")
        with contextlib.suppress(Exception) as sup:
            convo = await scraper.scrape_one_conversation(url)
            conversations.append(convo)
        if sup is not None and sup.__enter__ is None:  # noqa: E711 - no-op
            pass
        await asyncio.sleep(0.2)

    return PlatformDump(platform=platform, conversations=conversations)

async def run(platforms: List[str], out_path: Optional[Path], headless: bool, max_conversations: Optional[int]) -> Path:
    await ensure_dir(DEFAULT_PROFILE_DIR)

    out_path = out_path or Path(f"omni_scour_dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json").resolve()

    async with async_playwright() as p:
        browser_type = p.chromium
        all_platform_dumps: Dict[str, PlatformDump] = {}

        for platform in platforms:
            profile_dir = DEFAULT_PROFILE_DIR / sanitize_filename(platform)
            await ensure_dir(profile_dir)

            rprint(f"\n[bold magenta]=== {platform} ===[/bold magenta]")
            context = await browser_type.launch_persistent_context(
                user_data_dir=str(profile_dir),
                headless=headless,
                viewport={"width": 1440, "height": 1100},
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-default-browser-check",
                    "--disable-features=site-per-process",
                ],
            )

            try:
                dump = await scrape_platform(platform, context, headless, max_conversations)
                all_platform_dumps[platform] = dump
            finally:
                with contextlib.suppress(Exception):
                    await context.close()

    # Assemble final JSON
    serializable = {
        "metadata": {
            "generated_at_utc": now_iso(),
            "script": SCRIPT_NAME,
            "version": "1.2.0",
            "platforms": platforms,
            "notes": "Text-only export (best-effort). Structure may vary per site UI update.",
        },
        "platforms": {
            plat: {
                "platform": plat,
                "conversations": [
                    {
                        "id": c.id,
                        "url": c.url,
                        "title": c.title,
                        "scraped_at_utc": c.scraped_at_utc,
                        "messages": [
                            {"role": m.role, "text": m.text} for m in c.messages
                        ],
                    }
                    for c in dump.conversations
                ],
            }
            for plat, dump in all_platform_dumps.items()
        },
    }

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

    rprint(f"\n[bold green]✓ Saved:[/bold green] {out_path}")
    return out_path

# --------------------------------- CLI ----------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description="Omni-Scour Local Agent — export your chat histories by logging in manually then letting Playwright crawl threads.",
    )
    ap.add_argument(
        "--platforms",
        nargs="+",
        required=True,
        help=(
            "One or more domains to scrape (e.g., chat.openai.com claude.ai poe.com). "
            "Unknown domains will use a generic scraper."
        ),
    )
    ap.add_argument(
        "--out",
        type=Path,
        help="Optional output JSON path (default: omni_scour_dump_YYYYMMDD_HHMMSS.json)",
    )
    ap.add_argument(
        "--headless",
        action="store_true",
        default=DEFAULT_HEADLESS,
        help="Run browser headlessly (not recommended for manual login).",
    )
    ap.add_argument(
        "--max-conversations",
        type=int,
        help="Optional cap on conversations per platform.",
    )
    return ap

async def main_async(args: argparse.Namespace) -> None:
    await run(
        platforms=args.platforms,
        out_path=args.out,
        headless=args.headless,
        max_conversations=args.max_conversations,
    )

def main() -> None:
    ap = build_arg_parser()
    args = ap.parse_args()
    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        rprint("\n[red]Interrupted by user.[/red]")

if __name__ == "__main__":
    main()
