"""layout.py — fixed 1024x1024 composition on a strict pixel grid.

Concept A, "Front Page, Refined": one dominant hero, five illustrated
leads in one unified duotone style, ~30 briefs with larger type and
monochrome bullets, a decluttered world map with numbered pins only.

All coordinates are fixed integers. plan() computes every text wrap
and asserts that nothing overflows its box; a layout failure is a
loud error at build time, never a silent overlap in the image.
"""
from font import REGULAR, BOLD
import data

W = 1024
H = 1024
MARGIN = 24
CONTENT_W = W - 2 * MARGIN  # 976

# Vertical bands (fixed).
MASTHEAD = (8, 84)
HERO = (92, 304)
LEADS = (312, 540)
BRIEFS = (548, 896)
BOTTOM = (904, 1016)

# Palette (limited, high contrast, duotone editorial).
PAPER = (246, 242, 233)
INK = (24, 28, 36)
NAVY = (27, 42, 74)
RED = (198, 32, 32)
TEAL = (16, 90, 96)
GREY = (96, 100, 112)
LIGHT = (214, 212, 204)
WHITE = (255, 255, 255)
AMBER = (255, 178, 71)
SKY_TOP = (191, 211, 230)
SKY_BOT = (143, 179, 217)
SEA_TOP = (46, 111, 163)
SEA_BOT = (28, 74, 116)
DUSK_TOP = (233, 196, 150)
DUSK_BOT = (196, 148, 116)
STONE = (222, 216, 200)
MAP_SEA = (176, 204, 226)
MAP_LAND = (226, 220, 196)
MAP_LINE = (120, 118, 106)

# Lead columns: 5 across, 10px gaps.
LEAD_COL_W = 187
LEAD_XS = [MARGIN + i * (LEAD_COL_W + 10) for i in range(5)]

# Brief columns.
BRIEF_COL_A = (MARGIN, MARGIN + 476)          # x 24..500
BRIEF_COL_B = (MARGIN + 488, W - MARGIN)      # x 512..1000
BRIEF_LINE_H = 18
SECTION_H = 18

# Bottom strip.
MARKETS_X = (MARGIN, 396)
KEY_X = (408, 696)
MAP_X = (708, 999)
MAP_LAT_TOP = 70.0    # north edge shown
MAP_LAT_BOT = -55.0   # south edge shown


def map_xy(lon, lat):
    """Equirectangular projection into the map box."""
    x0, x1 = MAP_X
    y0, y1 = BOTTOM
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (MAP_LAT_TOP - lat) / (MAP_LAT_TOP - MAP_LAT_BOT) * (y1 - y0)
    return int(round(x)), int(round(y))


def plan(canvas):
    """Compute every wrap; assert everything fits. Returns a dict of
    regions the renderer consumes."""
    p = {}

    # --- masthead ---
    title_w = canvas.text_w(data.PAPER_NAME, BOLD, 2)
    assert title_w <= CONTENT_W, title_w
    p["title_x"] = (W - title_w) // 2
    date_w = canvas.text_w(data.DATE_LINE, BOLD, 1)
    assert date_w <= CONTENT_W
    p["date_x"] = (W - date_w) // 2
    count_w = canvas.text_w(data.STORY_COUNT_LINE, REGULAR, 1)
    p["count_x"] = (W - count_w) // 2

    # --- hero ---
    hero_text_x = 500
    hero_text_w = 1000 - hero_text_x
    hero_lines = []
    for line in data.HERO["headline"]:
        assert canvas.text_w(line, BOLD, 2) <= hero_text_w, line
        hero_lines.append(line)
    assert len(hero_lines) == 3
    p["hero_lines"] = hero_lines
    summary = canvas.wrap(data.HERO["summary"], REGULAR, 1, hero_text_w)
    assert len(summary) <= 3, summary
    p["hero_summary"] = summary

    # --- leads ---
    p["leads"] = []
    for i, lead in enumerate(data.LEADS):
        x = LEAD_XS[i]
        head = canvas.wrap(lead["headline"], BOLD, 1, LEAD_COL_W)
        assert len(head) <= 2, (lead["headline"], head)
        summ = canvas.wrap(lead["summary"], REGULAR, 1, LEAD_COL_W)
        assert len(summ) <= 3, (lead["summary"], summ)
        p["leads"].append({"x": x, "head": head, "summ": summ,
                           "lead": lead})

    # --- briefs: two columns, three sections each ---
    # Column A: WORLD, POLITICS, TECH. Column B: CULTURE, MARKETS, SPORT.
    groups = [("WORLD", "POLITICS", "TECH"), ("CULTURE", "MARKETS", "SPORT")]
    by_section = {}
    for section, text in data.BRIEFS:
        by_section.setdefault(section, []).append(text)
    p["brief_cols"] = []
    for ci, (x0, x1) in enumerate((BRIEF_COL_A, BRIEF_COL_B)):
        col_w = x1 - x0
        col = {"x0": x0, "x1": x1, "sections": []}
        y = BRIEFS[0]
        for section in groups[ci]:
            items = by_section[section]
            col["sections"].append({"name": section, "y": y,
                                    "items": items})
            y += SECTION_H
            for text in items:
                assert canvas.text_w(text, REGULAR, 1) <= col_w - 18, text
                y += BRIEF_LINE_H
        assert y <= BRIEFS[1], ("briefs overflow col", ci, y)
        col["bottom"] = y
        p["brief_cols"].append(col)

    # --- markets figures: 4 rows x 2 cols ---
    p["market_cells"] = []
    for i, (label, value, change) in enumerate(data.MARKET_FIGURES):
        row, col = divmod(i, 2)
        x = MARKETS_X[0] + col * 186
        y = BOTTOM[0] + 24 + row * 22
        # True rendered width: bold label + 4 + value + 4 + bold change.
        true_w = (canvas.text_w(label, BOLD, 1) + 4
                  + canvas.text_w(value, REGULAR, 1) + 4
                  + canvas.text_w(change, BOLD, 1))
        assert true_w <= 182, (label, true_w)
        p["market_cells"].append({"x": x, "y": y, "label": label,
                                  "value": value, "change": change})

    # --- map key: 2 cols x 5 rows ---
    p["key_cells"] = []
    for i, (num, name, lon, lat) in enumerate(data.MAP_CITIES):
        col, row = divmod(i, 5)
        x = KEY_X[0] + col * 152
        y = BOTTOM[0] + 22 + row * 17
        cell = "%d %s" % (num, name)
        assert canvas.text_w(cell, REGULAR, 1) <= 148, cell
        p["key_cells"].append({"x": x, "y": y, "num": num, "name": name})

    # --- map pins (number-label offsets tuned so Europe does not collide) ---
    offsets = {
        1: (-16, -12),   # NEW YORK: label up-left
        2: (8, 8),       # WASHINGTON: label down-right
        3: (-16, -12),   # SAN FRANCISCO
        4: (-14, -14),   # LONDON: label up-left
        5: (10, 6),      # PARIS: label down-right
        6: (8, -12),     # KYIV
        7: (8, 6),       # GAZA
        8: (8, -12),     # NEW DELHI
        9: (8, 6),       # SHENZHEN
        10: (-24, -6),   # WELLINGTON: label to the left (map edge)
    }
    p["pins"] = []
    for num, name, lon, lat in data.MAP_CITIES:
        px, py = map_xy(lon, lat)
        dx, dy = offsets[num]
        p["pins"].append({"num": num, "x": px, "y": py,
                          "lx": px + dx, "ly": py + dy})
    return p
