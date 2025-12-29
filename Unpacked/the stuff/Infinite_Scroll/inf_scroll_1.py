#!/usr/bin/env python3
# infinite_scroll_ui.py
# Termux-friendly curses UI: Infinite Scroll viewer with color, mood, search, bookmarks.

import curses
import os
import textwrap
import json
from pathlib import Path

# Config
HOME = Path(os.environ.get("HOME", "."))
DEFAULT_SCROLL_PATH = HOME / "zaai" / "scroll.md"
BOOKMARKS_PATH = HOME / ".infinite_scroll_bookmarks.json"
PADDING = 2
WRAP_WIDTH = 80

SAMPLE_SCROLL = """\
♾️  INFINITE SCROLL — ZAAI
────────────────────────

This is a sample of the Infinite Scroll. Replace $HOME/zaai/scroll.md
with your own scroll text to view it here.

Controls:
  ↑/↓  k/j    scroll
  PgUp/PgDn   page jump
  g / G       top / bottom
  /           search
  n           next match
  b           toggle bookmark at current line
  B           bookmarks menu
  q           quit

Mood: twilight — slow, deep, reverent. Color theme: indigo / magenta / gold.
"""

# Utilities for bookmarks
def load_bookmarks():
    try:
        with open(BOOKMARKS_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_bookmarks(bm):
    try:
        with open(BOOKMARKS_PATH, "w") as f:
            json.dump(bm, f, indent=2)
    except Exception:
        pass

# Load scroll text
def load_scroll_text(path=None):
    path = path or DEFAULT_SCROLL_PATH
    if path.exists():
        raw = path.read_text(encoding="utf-8", errors="ignore")
    else:
        raw = SAMPLE_SCROLL
    # split into paragraphs and wrap
    paragraphs = [p.strip() for p in raw.splitlines()]
    # produce display lines - wrap long lines
    lines = []
    for p in paragraphs:
        if p == "":
            lines.append("")
        else:
            wrapped = textwrap.wrap(p, width=WRAP_WIDTH)
            if not wrapped:
                lines.append("")
            else:
                lines.extend(wrapped)
    return lines

# Curses UI
def ui(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()
    # Initialize color pairs (limited but expressive)
    curses.init_pair(1, curses.COLOR_MAGENTA, -1)  # header
    curses.init_pair(2, curses.COLOR_CYAN, -1)     # subheader
    curses.init_pair(3, curses.COLOR_WHITE, -1)    # body
    curses.init_pair(4, curses.COLOR_YELLOW, -1)   # gold accents
    curses.init_pair(5, curses.COLOR_BLUE, -1)     # sidebar
    curses.init_pair(6, curses.COLOR_GREEN, -1)    # bookmarks
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)  # status

    height, width = stdscr.getmaxyx()
    left_w = max(24, int(width * 0.18))
    right_w = max(22, int(width * 0.18))
    center_w = width - left_w - right_w - (PADDING * 2)

    # load content
    lines = load_scroll_text()
    n_lines = len(lines)

    top = 0           # index of top visible line
    cursor = 0        # highlighted line index
    bookmarks = load_bookmarks()  # list of line numbers
    search_query = ""
    matches = []
    match_index = -1

    def draw():
        nonlocal height, width, left_w, right_w, center_w
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        left_w = max(24, int(width * 0.18))
        right_w = max(22, int(width * 0.18))
        center_w = width - left_w - right_w - (PADDING * 2)

        # Header
        header = " ♾️  INFINITE SCROLL — ZAAI ".center(width)
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(0, 0, header[:width])
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # Left sidebar (mood + meta)
        meta_win_h = height - 3
        for i in range(2, meta_win_h):
            stdscr.addch(i, left_w - 1, curses.ACS_VLINE)
        # Mood block
        mood_y = 2
        stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
        stdscr.addstr(mood_y, 1, "MOOD".center(left_w - 2))
        stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
        stdscr.attron(curses.color_pair(2))
        mood_lines = ["twilight", "indigo wash", "magenta pulse", "slow reverence"]
        for i, m in enumerate(mood_lines):
            stdscr.addstr(mood_y + 2 + i, 2, ("• " + m)[:left_w - 4])
        stdscr.attroff(curses.color_pair(2))

        # Left metadata footer
        stdscr.attron(curses.color_pair(4))
        meta_footer = f"Lines: {n_lines}  Width:{center_w}"
        stdscr.addstr(height - 2, 1, meta_footer[:left_w - 2])
        stdscr.attroff(curses.color_pair(4))

        # Right sidebar (bookmarks)
        stdscr.attron(curses.color_pair(6) | curses.A_BOLD)
        stdscr.addstr(2, width - right_w + 1, "BOOKMARKS".center(right_w - 2))
        stdscr.attroff(curses.color_pair(6) | curses.A_BOLD)
        for idx, lm in enumerate(sorted(bookmarks)[:meta_win_h - 4]):
            label = f"{idx+1}. L{lm+1}"
            display = (" " + label + " " + (lines[lm][:right_w - len(label) - 6]))[:right_w - 4]
            stdscr.addstr(4 + idx, width - right_w + 2, display)

        # Center window - content pane
        view_h = height - 6
        for i in range(view_h):
            li = top + i
            if li >= n_lines:
                break
            text = lines[li]
            # choose color gradient by position
            if li == cursor:
                attr = curses.A_REVERSE | curses.color_pair(3)
            else:
                if li % 7 == 0:
                    attr = curses.color_pair(2)
                elif li % 5 == 0:
                    attr = curses.color_pair(4)
                elif li % 3 == 0:
                    attr = curses.color_pair(1)
                else:
                    attr = curses.color_pair(3)
            # mark matches
            mark = " "
            if li in matches:
                mark = "*"
            # bookmarked marker
            bmark = "◈" if li in bookmarks else " "
            line_text = f"{bmark}{mark} {text}".ljust(center_w)[:center_w]
            stdscr.addstr(2 + i, left_w + PADDING, line_text, attr)

        # Footer / status
        status = f" {cursor+1}/{n_lines}  top={top+1}  q:quit  /:search  b:bookmark  B:bookmarks  n:next "
        if search_query:
            status = f"[search='{search_query}'] " + status
        stdscr.attron(curses.color_pair(7))
        stdscr.addstr(height - 1, 0, status.ljust(width)[:width])
        stdscr.attroff(curses.color_pair(7))

        stdscr.refresh()

    def find_matches(q):
        res = []
        if not q:
            return res
        lowq = q.lower()
        for i, ln in enumerate(lines):
            if lowq in ln.lower():
                res.append(i)
        return res

    draw()
    while True:
        draw()
        ch = stdscr.getch()
        if ch in (curses.KEY_DOWN, ord('j')):
            if cursor < n_lines - 1:
                cursor += 1
            if cursor >= top + (height - 6):
                top += 1
        elif ch in (curses.KEY_UP, ord('k')):
            if cursor > 0:
                cursor -= 1
            if cursor < top:
                top = max(0, top - 1)
        elif ch == curses.KEY_NPAGE:  # Page Down
            page = height - 6
            cursor = min(n_lines - 1, cursor + page)
            top = min(max(0, n_lines - page), top + page)
        elif ch == curses.KEY_PPAGE:  # Page Up
            page = height - 6
            cursor = max(0, cursor - page)
            top = max(0, top - page)
        elif ch == ord('g'):
            cursor = 0
            top = 0
        elif ch == ord('G'):
            cursor = n_lines - 1
            top = max(0, n_lines - (height - 6))
        elif ch == ord('q'):
            save_bookmarks(bookmarks)
            break
        elif ch == ord('b'):
            # toggle bookmark at cursor
            if cursor in bookmarks:
                bookmarks.remove(cursor)
            else:
                bookmarks.append(cursor)
            bookmarks = sorted(set(bookmarks))
        elif ch == ord('B'):
            # show bookmarks quick-jump: simple modal
            if not bookmarks:
                # flash status
                stdscr.addstr(height - 2, 1, "No bookmarks".ljust(left_w - 2)[:left_w - 2], curses.color_pair(4))
                stdscr.refresh()
                curses.napms(600)
            else:
                sel = 0
                while True:
                    # draw modal
                    mw = min(60, width - 6)
                    mh = min(10, height - 6)
                    sx = (width - mw) // 2
                    sy = (height - mh) // 2
                    for r in range(mh):
                        stdscr.addstr(sy + r, sx, " " * mw, curses.color_pair(7))
                    stdscr.addstr(sy, sx + 2, "Bookmarks (Enter to jump, q to close)", curses.color_pair(1))
                    for i, bm in enumerate(bookmarks[:mh - 4]):
                        prefix = "→ " if i == sel else "  "
                        text = f"{prefix}{i+1}. L{bm+1} {lines[bm][:mw-12]}"
                        stdscr.addstr(sy + 2 + i, sx + 2, text[:mw-4], curses.color_pair(3))
                    stdscr.refresh()
                    k = stdscr.getch()
                    if k in (curses.KEY_DOWN, ord('j')):
                        if sel < len(bookmarks) - 1:
                            sel += 1
                    elif k in (curses.KEY_UP, ord('k')):
                        if sel > 0:
                            sel -= 1
                    elif k in (10, 13):  # enter
                        cursor = bookmarks[sel]
                        top = max(0, cursor - (height - 6) // 2)
                        break
                    elif k == ord('q'):
                        break
        elif ch == ord('/'):
            # search prompt - simple inline
            curses.echo()
            stdscr.addstr(height - 2, 0, "Search: ".ljust(width))
            stdscr.refresh()
            q = stdscr.getstr(height - 2, 8, 60).decode("utf-8")
            curses.noecho()
            search_query = q.strip()
            matches = find_matches(search_query)
            if matches:
                match_index = 0
                cursor = matches[match_index]
                top = max(0, cursor - (height - 6)//2)
            else:
                match_index = -1
        elif ch == ord('n'):
            # next match
            if matches:
                match_index = (match_index + 1) % len(matches) if match_index >= 0 else 0
                cursor = matches[match_index]
                top = max(0, cursor - (height - 6)//2)
        elif ch == curses.KEY_RESIZE:
            pass
        else:
            # ignore other keys
            pass

def main():
    try:
        curses.wrapper(ui)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
