"""draw.py — renders Concept A, "Front Page, Refined", onto the canvas.

One unified duotone editorial style: warm paper, navy ink, one red
accent, one teal accent. All illustration is procedural (rects, lines,
polygons, discs) from fixed tables — no external assets, no randomness.
"""
from font import REGULAR, BOLD
from layout import (
    W, H, MARGIN, MASTHEAD, HERO, LEADS, BRIEFS, BOTTOM,
    PAPER, INK, NAVY, RED, TEAL, GREY, LIGHT, WHITE, AMBER,
    SKY_TOP, SKY_BOT, SEA_TOP, SEA_BOT, DUSK_TOP, DUSK_BOT, STONE,
    MAP_SEA, MAP_LAND, MAP_LINE, LEAD_XS, LEAD_COL_W,
    BRIEF_LINE_H, SECTION_H, MARKETS_X, KEY_X, MAP_X, map_xy,
)
import data

# Coarse continent outlines (lon, lat). Stylised, recognisable at small
# size; latitudes clamp to the map window in map_xy.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-60, 52), (-55, 47), (-65, 44), (-75, 39),
     (-80, 32), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-40, 65), (-55, 70), (-65, 70)],
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-40, -5),
     (-35, -9), (-40, -20), (-48, -28), (-55, -35), (-65, -41),
     (-70, -50), (-70, -54), (-75, -40), (-75, -20), (-80, -5), (-80, 5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (48, 11), (51, 12), (44, 0), (40, -10),
     (35, -20), (30, -30), (20, -35), (15, -30), (12, -18), (9, 4),
     (4, 6), (-8, 5), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65),
     (20, 70), (15, 70), (10, 68), (5, 60), (0, 55), (-5, 50), (-10, 44)],
    [(30, 62), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55),
     (150, 59), (140, 50), (135, 43), (127, 40), (122, 38), (120, 32),
     (115, 23), (108, 18), (105, 10), (100, 8), (95, 15), (90, 22),
     (85, 20), (80, 13), (77, 8), (73, 16), (68, 23), (62, 25),
     (57, 26), (52, 28), (48, 30), (44, 29), (40, 31), (36, 36),
     (30, 36), (28, 41), (30, 45), (32, 50), (35, 55), (40, 60)],
    [(114, -22), (114, -30), (120, -34), (130, -32), (140, -38),
     (147, -39), (150, -37), (153, -32), (150, -22), (146, -19),
     (142, -11), (136, -12), (132, -11), (126, -14), (122, -17),
     (118, -20)],
]


def sky_bands(cv, x, y, w, h, top, bot):
    """Two-tone sky: top half lighter, bottom half deeper."""
    cv.fill_rect(x, y, w, h // 2, top)
    cv.fill_rect(x, y + h // 2, w, h - h // 2, bot)


def skyline(cv, x, y, w, base_y, heights, color, win_color):
    """Row of buildings with lit windows. heights: fixed list."""
    n = len(heights)
    bw = w // n
    for i, hh in enumerate(heights):
        bx = x + i * bw
        bh = hh
        cv.fill_rect(bx + 1, base_y - bh, bw - 2, bh, color)
        # windows: fixed grid, every third cell lit
        for wy in range(base_y - bh + 6, base_y - 6, 12):
            for wx in range(bx + 4, bx + bw - 4, 10):
                if (wx // 10 + wy // 12) % 3 == 0:
                    cv.fill_rect(wx, wy, 3, 4, win_color)


def art_gta(cv, x, y, w, h):
    """Hero art: Vice City dusk skyline, sun, road."""
    sky_bands(cv, x, y, w, h, DUSK_TOP, DUSK_BOT)
    cv.disc(x + w - 70, y + 42, 26, AMBER)
    cv.disc(x + w - 70, y + 42, 18, (255, 210, 63))
    skyline(cv, x, y + 40, w, y + h - 26,
            [52, 78, 64, 96, 70, 110, 84, 60, 92, 74, 100, 66],
            NAVY, AMBER)
    # road
    cv.fill_rect(x, y + h - 26, w, 26, INK)
    cv.fill_rect(x, y + h - 14, w, 2, (255, 210, 63))
    # giant VI numerals in the sky
    cv.text(x + 28, y + 8, "VI", BOLD, 3, (255, 255, 255))


def art_summit(cv, x, y, w, h):
    """Three flags over a summit skyline."""
    sky_bands(cv, x, y, w, h, SKY_TOP, SKY_BOT)
    skyline(cv, x, y + 30, w, y + h - 14,
            [26, 34, 22, 40, 30, 24], (90, 96, 110), WHITE)
    # flag poles
    for i, fx in enumerate((x + 30, x + w // 2, x + w - 34)):
        cv.vline(fx, y + 10, y + 58, NAVY)
        if i == 0:  # US: stripes + blue canton
            for s in range(4):
                cv.fill_rect(fx + 2, y + 12 + s * 7, 26, 3,
                             RED if s % 2 == 0 else WHITE)
            cv.fill_rect(fx + 2, y + 12, 12, 12, NAVY)
        elif i == 1:  # China: red field, gold dots
            cv.fill_rect(fx + 2, y + 12, 26, 24, RED)
            cv.disc(fx + 8, y + 20, 2, AMBER)
            cv.disc(fx + 16, y + 16, 1, AMBER)
            cv.disc(fx + 20, y + 22, 1, AMBER)
        else:  # Russia: white-blue-red bands
            cv.fill_rect(fx - 24, y + 12, 26, 8, WHITE)
            cv.fill_rect(fx - 24, y + 20, 26, 8, (46, 111, 163))
            cv.fill_rect(fx - 24, y + 28, 26, 8, RED)
    cv.fill_rect(x, y + h - 14, w, 14, NAVY)


def art_ipo(cv, x, y, w, h):
    """Rising chart with arrow, ANT ticker."""
    cv.fill_rect(x, y, w, h, PAPER)
    cv.rect(x, y, w, h, LIGHT, 1)
    # grid
    for gy in range(y + 16, y + h - 8, 14):
        cv.hline(x + 8, x + w - 8, gy, LIGHT)
    # rising line (thick, two passes)
    pts = [(x + 10, y + h - 18), (x + 40, y + h - 30), (x + 70, y + h - 26),
           (x + 100, y + h - 44), (x + 130, y + h - 40), (x + 160, y + 16)]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], TEAL)
        cv.line(pts[i][0], pts[i][1] + 1, pts[i + 1][0], pts[i + 1][1] + 1, TEAL)
    # arrow head
    ax, ay = pts[-1]
    cv.poly([(ax, ay - 2), (ax - 12, ay + 2), (ax - 2, ay + 10)], TEAL)
    cv.text(x + 10, y + 6, "ANT", BOLD, 1, NAVY)


def art_capitol(cv, x, y, w, h):
    """Capitol dome as a navy silhouette on a pale sky."""
    sky_bands(cv, x, y, w, h, SKY_TOP, SKY_BOT)
    cx = x + w // 2
    base = y + h - 12
    # dome silhouette
    cv.disc(cx, base - 26, 22, NAVY)
    cv.fill_rect(cx - 22, base - 26, 44, 26, NAVY)
    # flagpole + red finial
    cv.vline(cx, base - 58, base - 46, NAVY)
    cv.disc(cx, base - 58, 3, RED)
    # body with sky-coloured slits for columns
    cv.fill_rect(cx - 44, base - 26, 88, 26, NAVY)
    for i in range(4):
        gapx = cx - 32 + i * 20
        cv.fill_rect(gapx, base - 24, 5, 24, SKY_BOT)
    # steps
    cv.fill_rect(x, base, w, 12, NAVY)


def art_gulf(cv, x, y, w, h):
    """Sea, ship, sun."""
    sky_bands(cv, x, y, w, h, SKY_TOP, SKY_BOT)
    cv.disc(x + w - 30, y + 18, 12, AMBER)
    cv.fill_rect(x, y + h // 2, w, h - h // 2, SEA_TOP)
    cv.fill_rect(x, y + h // 2 + 12, w, h - h // 2 - 12, SEA_BOT)
    # ship hull + containers + mast
    hx, hy = x + 30, y + h - 34
    cv.poly([(hx, hy), (hx + 110, hy), (hx + 98, hy + 14),
             (hx + 12, hy + 14)], NAVY)
    cv.fill_rect(hx + 18, hy - 14, 16, 14, RED)
    cv.fill_rect(hx + 38, hy - 14, 16, 14, AMBER)
    cv.fill_rect(hx + 58, hy - 14, 16, 14, WHITE)
    cv.vline(hx + 88, hy - 26, hy, NAVY)
    cv.hline(hx + 88, hx + 108, hy - 26, NAVY)


def art_bridge(cv, x, y, w, h):
    """Suspension bridge over water, burst above."""
    sky_bands(cv, x, y, w, h, SKY_TOP, SKY_BOT)
    cv.fill_rect(x, y + h - 22, w, 22, SEA_TOP)
    # towers + deck + cables
    for tx in (x + 40, x + w - 44):
        cv.fill_rect(tx, y + 18, 6, h - 40, NAVY)
    cv.fill_rect(x + 8, y + h - 34, w - 16, 6, NAVY)
    cv.line(x + 40, y + 18, x + w // 2, y + h - 34, NAVY)
    cv.line(x + w - 40, y + 18, x + w // 2, y + h - 34, NAVY)
    # burst star
    bx, by = x + w // 2, y + 16
    for dx, dy in ((-10, 0), (10, 0), (0, -8), (0, 8),
                   (-7, -7), (7, -7), (-7, 7), (7, 7)):
        cv.line(bx, by, bx + dx, by + dy, RED)
    cv.disc(bx, by, 3, RED)


ART = {
    "gta": art_gta,
    "summit": art_summit,
    "ipo": art_ipo,
    "capitol": art_capitol,
    "gulf": art_gulf,
    "bridge": art_bridge,
}


def draw_map(cv, plan):
    x0, x1 = MAP_X
    y0, y1 = BOTTOM
    cv.fill_rect(x0, y0, x1 - x0, y1 - y0, MAP_SEA)
    for poly in CONTINENTS:
        pts = [map_xy(lon, max(-55.0, min(70.0, lat))) for lon, lat in poly]
        cv.poly(pts, MAP_LAND)
        for i in range(len(pts)):
            ax, ay = pts[i]
            bx, by = pts[(i + 1) % len(pts)]
            cv.line(ax, ay, bx, by, MAP_LINE)
    cv.rect(x0, y0, x1 - x0, y1 - y0, MAP_LINE, 1)
    for pin in plan["pins"]:
        cv.disc(pin["x"], pin["y"], 4, NAVY)
        num = str(pin["num"])
        tw = cv.text_w(num, BOLD, 1)
        lx, ly = pin["lx"], pin["ly"]
        cv.fill_rect(lx - 2, ly, tw + 4, 16, WHITE)
        cv.text(lx, ly, num, BOLD, 1, RED)


def render(cv, plan):
    # --- masthead ---
    cv.text(plan["title_x"], MASTHEAD[0], data.PAPER_NAME, BOLD, 2, NAVY)
    cv.text(plan["date_x"], 50, data.DATE_LINE, BOLD, 1, RED)
    cv.text(plan["count_x"], 68, data.STORY_COUNT_LINE, REGULAR, 1, GREY)
    cv.hline(MARGIN, W - MARGIN, 84, NAVY)
    cv.hline(MARGIN, W - MARGIN, 86, NAVY)

    # --- hero ---
    cv.rect(MARGIN, HERO[0], W - 2 * MARGIN, HERO[1] - HERO[0],
            NAVY, 2)
    ART[data.HERO["art"]](cv, MARGIN, HERO[0], 460, HERO[1] - HERO[0])
    tx = 500
    cv.text(tx, 100, data.HERO["kicker"], BOLD, 1, RED)
    for i, line in enumerate(plan["hero_lines"]):
        cv.text(tx, 124 + i * 36, line, BOLD, 2, INK)
    for i, line in enumerate(plan["hero_summary"]):
        cv.text(tx, 244 + i * 20, line, REGULAR, 1, INK)

    # --- leads ---
    for item in plan["leads"]:
        x = item["x"]
        lead = item["lead"]
        ART[lead["art"]](cv, x, LEADS[0], LEAD_COL_W, 80)
        cv.text(x, 398, lead["section"], BOLD, 1, RED)
        for i, line in enumerate(item["head"]):
            cv.text(x, 420 + i * 20, line, BOLD, 1, INK)
        for i, line in enumerate(item["summ"]):
            cv.text(x, 462 + i * 20, line, REGULAR, 1, GREY)

    # --- briefs ---
    for col in plan["brief_cols"]:
        y = BRIEFS[0]
        for section in col["sections"]:
            cv.text(col["x0"], y, section["name"], BOLD, 1, RED)
            cv.hline(col["x0"], col["x1"], y + 17, LIGHT)
            y += SECTION_H
            for text in section["items"]:
                cv.fill_rect(col["x0"], y + 7, 6, 6, NAVY)
                cv.text(col["x0"] + 14, y, text, REGULAR, 1, INK)
                y += BRIEF_LINE_H

    # --- bottom: markets ---
    cv.text(MARKETS_X[0], BOTTOM[0] + 2, "MARKETS", BOLD, 1, RED)
    cv.hline(MARKETS_X[0], MARKETS_X[1], BOTTOM[0] + 20, LIGHT)
    for cell in plan["market_cells"]:
        x, y = cell["x"], cell["y"]
        lx = cv.text(x, y, cell["label"], BOLD, 1, INK)
        vx = cv.text(x + lx + 4, y, cell["value"], REGULAR, 1, INK)
        col = RED if cell["change"].startswith("-") else TEAL
        cv.text(x + lx + 4 + vx + 4, y, cell["change"], BOLD, 1, col)

    # --- bottom: map key ---
    cv.text(KEY_X[0], BOTTOM[0] + 2, "ON THE MAP", BOLD, 1, RED)
    cv.hline(KEY_X[0], KEY_X[1], BOTTOM[0] + 20, LIGHT)
    for cell in plan["key_cells"]:
        cv.text(cell["x"], cell["y"], str(cell["num"]), BOLD, 1, RED)
        nx = cell["x"] + cv.text_w(str(cell["num"]), BOLD, 1) + 5
        cv.text(nx, cell["y"], cell["name"], REGULAR, 1, INK)

    # --- bottom: world map ---
    draw_map(cv, plan)
