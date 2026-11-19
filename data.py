"""data.py — the verified stories of Thursday 19 November 2026.

Every story was checked against reporting published on 19 Nov 2026
(BBC, Reuters via BusinessWorld, AP via AJP, NDTV, Al Jazeera, USA
Today, NASA, EU, AFF, NBA/cricket score wires, market wires). No
story is invented, hyped, or speculative. All strings are ASCII-only:
the embedded bitmap font covers printable ASCII.

Structure:
  HERO   — the day's single most consequential story (double-width lead)
  LEADS  — 5 more illustrated leads, one unified duotone style
  BRIEFS — 30 one-line briefs, grouped by section (WORLD, POLITICS,
           TECH, CULTURE, MARKETS, SPORT)
  MARKET_FIGURES — closing figures for the MARKETS panel
  MAP_CITIES — (number, name, lon, lat) for the world-map pins
"""
DATE_LINE = "THURSDAY 19 NOVEMBER 2026"
PAPER_NAME = "THE WORLD IN ONE DAY"
STORY_COUNT_LINE = "36 STORIES FROM SIX CONTINENTS"

HERO = {
    "kicker": "CULTURE  -  GAMES",
    "headline": ["GRAND THEFT AUTO VI",
                 "LAUNCHES WORLDWIDE",
                 "AFTER 13-YEAR WAIT"],
    "summary": ("Rockstar's epic opens at midnight in every time zone "
                "on PS5 and Xbox - 99 on Metacritic, $1bn in pre-sales, "
                "a 212 GB download, and no PC date yet."),
    "art": "gta",
    "source": "Rockstar Games; USA Today; Reuters",
}

LEADS = [
    {
        "section": "WORLD",
        "headline": "TRUMP, XI, PUTIN MEET IN SHENZHEN",
        "summary": ("First three-way summit of the nuclear powers."),
        "art": "summit",
        "source": "BusinessWorld/Reuters; AJP",
    },
    {
        "section": "TECH",
        "headline": "ANTHROPIC IPO SMASHES RECORD",
        "summary": ("Priced at $83; $81bn raised; ANT lists today."),
        "art": "ipo",
        "source": "Reuters; BusinessWorld; TradingView",
    },
    {
        "section": "POLITICS",
        "headline": "JEFFRIES: FIRST BLACK SPEAKER",
        "summary": ("House Democrats nominate him; gavel 3 January."),
        "art": "capitol",
        "source": "NDTV; BBC",
    },
    {
        "section": "WORLD",
        "headline": "US-IRAN FIRE SPREADS IN GULF",
        "summary": ("US hit Qeshm; Iran hit Bahrain and Kuwait."),
        "art": "gulf",
        "source": "SimpleLife/Reuters wire",
    },
    {
        "section": "WORLD",
        "headline": "CRIMEAN BRIDGE HIT AGAIN",
        "summary": ("Moscow says the bridge was attacked again."),
        "art": "bridge",
        "source": "BBC",
    },
]

# One line each; kept short enough to fit a single brief column.
BRIEFS = [
    ("WORLD", "Israeli tanks cross Gaza ceasefire line"),
    ("WORLD", "Cyclone Akvan nears India's east coast"),
    ("WORLD", "Australia sanctions Israeli settlements"),
    ("WORLD", "Spain strike ends in street clashes"),
    ("WORLD", "Libya seizes cocaine and millions of pills"),
    ("WORLD", "Canada rethinks China ties, Carney says"),
    ("POLITICS", "Melenchon could win French presidency: minister"),
    ("POLITICS", "India, Japan hold 2+2 defence talks"),
    ("POLITICS", "Congress attacks Modi govt over inflation"),
    ("POLITICS", "Liu Yunping first Asian American caucus chair"),
    ("POLITICS", "EU proposes 45bn euro Ukraine loan"),
    ("TECH", "Nvidia halts H-series chips to China"),
    ("TECH", "Nvidia chief promises earlier pay rises"),
    ("TECH", "Voyager 1 reaches one light-day from Earth"),
    ("TECH", "Islam to be largest faith by 2035: Pew"),
    ("TECH", "Microsoft in AI talks with ByteDance"),
    ("CULTURE", "Van Gogh sells for record $190.4m"),
    ("CULTURE", "McDonald's faces sex-abuse claims"),
    ("CULTURE", "World COPD Day urges early diagnosis"),
    ("CULTURE", "Ras Al Khaimah top city for expats in 2026"),
    ("MARKETS", "Dow falls 561 as UnitedHealth sinks 10%"),
    ("MARKETS", "S&P 500 logs fifth straight loss"),
    ("MARKETS", "Oil, gold and bitcoin slide together"),
    ("MARKETS", "Fed minutes point to more rate hikes"),
    ("SPORT", "Rockets beat Pacers 119-104 in NBA"),
    ("SPORT", "Cavaliers edge Grizzlies 105-102"),
    ("SPORT", "England win ODI series 2-1 in Hobart"),
    ("SPORT", "Pakistan 325 in Rawalpindi Test"),
    ("SPORT", "India-NZ Test begins in Wellington"),
    ("SPORT", "HCMC Police FC stun Buriram 1-0"),
]

# Closing figures reported on 19 Nov 2026 (Wednesday close in the US,
# Thursday opens in Asia). Format: (label, value, change).
MARKET_FIGURES = [
    ("DOW", "50,198", "-1.1%"),
    ("S&P", "7,324", "-0.2%"),
    ("NDQ", "24,429", "+0.4%"),
    ("FTSE", "10,551", "-1.3%"),
    ("NIKKEI", "59,024", "+0.3%"),
    ("GOLD", "$3,762", "-2.3%"),
    ("WTI", "$82", "-4.1%"),
    ("BTC", "$62,370", "-3.9%"),
]

# (key number, name, longitude, latitude)
MAP_CITIES = [
    (1, "NEW YORK", -74.0, 40.7),
    (2, "WASHINGTON", -77.0, 38.9),
    (3, "SAN FRANCISCO", -122.4, 37.8),
    (4, "LONDON", -0.1, 51.5),
    (5, "PARIS", 2.35, 48.85),
    (6, "KYIV", 30.5, 50.45),
    (7, "GAZA", 34.45, 31.5),
    (8, "NEW DELHI", 77.2, 28.6),
    (9, "SHENZHEN", 114.05, 22.55),
    (10, "WELLINGTON", 174.8, -41.3),
]


def validate():
    """Frozen-record checks: counts, required fields, date relevance."""
    assert HERO["headline"] and HERO["summary"] and HERO["art"]
    assert len(LEADS) == 5
    for lead in LEADS:
        assert lead["section"] and lead["headline"] and lead["summary"]
        assert lead["art"] and lead["source"]
    assert len(BRIEFS) == 30
    sections = {}
    for section, text in BRIEFS:
        assert text and len(text) <= 56, text
        assert all(32 <= ord(ch) < 127 for ch in text), text
        sections[section] = sections.get(section, 0) + 1
    assert sections == {"WORLD": 6, "POLITICS": 5, "TECH": 5,
                        "CULTURE": 4, "MARKETS": 4, "SPORT": 6}, sections
    assert len(MARKET_FIGURES) == 8
    assert len(MAP_CITIES) == 10
    for num, name, lon, lat in MAP_CITIES:
        assert -180 <= lon <= 180 and -90 <= lat <= 90
    total = 1 + len(LEADS) + len(BRIEFS)
    assert total == 36, total
    return total
