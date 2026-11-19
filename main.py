#!/usr/bin/env python3
"""The World in One Day — Thursday 19 November 2026.
A 1024x1024 newspaper front page drawn with PIL, no network.
Reads nothing, writes out/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).
Deterministic: same bytes on every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 231)
INK = (26, 32, 54)
NAVY = (31, 58, 95)
RED = (178, 44, 36)
GOLD = (198, 142, 38)
TEAL = (42, 122, 120)
SAGE = (112, 141, 110)
ROSE = (214, 138, 128)
SKY = (141, 178, 204)
SAND = (226, 201, 152)
LILAC = (150, 138, 190)
GREY = (110, 112, 118)
RULE = (26, 32, 54)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def centre(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.2)


# ---------------------------------------------------------------- stories
# (num, kicker, headline, deck, place) — all events of Thu 19 Nov 2026.
HEROES = [
    (1, "CULTURE  ·  LEONIDA",
     "GTA VI IS HERE",
     "After 13 years and $1bn, Rockstar's Vice City epic launches to a Metacritic 99. Take-Two shares jump 6.5% as downloads shatter network records.",
     "MIAMI"),
    (2, "DIPLOMACY  ·  SHENZHEN",
     "THREE LEADERS, ONE TABLE",
     "Trump, Xi and Putin hold a first three-way summit at APEC, pledging talks on nuclear risks as Ukraine and Iran top the agenda.",
     "SHENZHEN"),
    (3, "JUSTICE  ·  THE HAGUE",
     "MYANMAR GUILTY OF GENOCIDE",
     "The world court rules 9-6 that the 2017 crackdown on the Rohingya was genocide. Reparations to follow.",
     "THE HAGUE"),
]

FEATURES = [
    (4, "BUSINESS", "ANTHROPIC'S $81BN DEBUT",
     "AI lab prices at $83 a share in the largest IPO on record; shares open as ANT on the Nasdaq."),
    (5, "WAR IN UKRAINE", "BRIDGE HIT A THIRD TIME",
     "Ukraine strikes the Crimean Bridge for the third time in a week as the war grinds on."),
    (6, "MIDDLE EAST", "IRAN HITS GULF AFTER US STRIKE",
     "Tehran attacks Gulf states and fires on Kuwait after a US strike on Qeshm island."),
    (7, "WEATHER", "CYCLONE AKVAN BEARS DOWN",
     "Storm to hit India's Andhra-Odisha coast on Friday with winds of 100 km/h."),
    (8, "MARKETS", "WALL ST SPLIT AS FED SPLIT SHOWS",
     "Dow falls 1.1% in a fifth S&P slide; minutes show October's rate hold was a close call."),
    (9, "CLIMATE", "CLIMATE TALKS IN FINAL STRETCH",
     "Negotiators split over 'transition away' from fossil fuels and a 2035 electrification goal."),
    (10, "GAZA", "GAZA PLAN SCORES 4 OF 26",
     "Five aid groups rate the peace plan's delivery; Israel pushes past the Yellow Line."),
    (11, "SPACE", "VOYAGER 1, ONE LIGHT-DAY OUT",
     "NASA's probe becomes the first human-made object a light-day from Earth, 49 years on."),
    (12, "SPACE", "NASA RESHAPES MOON LANDINGS",
     "Starship to dock with Orion in Earth orbit; Blue Moon to meet it around the Moon."),
    (13, "SPORT", "BUURMAN SENDS CHELSEA TOP",
     "Late 87th-minute winner beats PSG 1-0 in the Women's Champions League."),
]

BRIEFS = [
    (14, "North Korea enriches more uranium, IAEA warns", "Enrichment expands at Yongbyon, the agency says."),
    (15, "Tanker Gas Husky sinks off Bulgaria", "LPG carrier struck by projectiles; 3,400 tonnes aboard."),
    (16, "Bangladesh shutdown turns violent", "Opposition calls a nationwide stoppage; Yunus home attacked."),
    (17, "Indonesia passes asset-forfeiture bill", "Parliament approves law to seize graft-linked assets."),
    (18, "Fiji declares disaster over El Nino drought", "National state of disaster as drought grips the islands."),
    (19, "589m children lived in war zones in 2025", "Save the Children: 23.4% of the world's children."),
    (20, "Denmark backs Greenland defence deal 109-0", "Folketing approves the September agreement."),
    (21, "Serbia elects Cupic as speaker", "Student List candidate wins 140 votes in parliament."),
    (22, "US-Philippines pursue $2bn loan package", "White House announces a financing push via FMF."),
    (23, "Taiwan stocks plunge 4%", "Regulators curb short-selling as the Taiex tumbles."),
    (24, "Walmart lifts outlook; Palo Alto jumps 9.3%", "Williams-Sonoma slides 6.2% after earnings."),
    (25, "Bitcoin slips to $63,479", "Gold sheds 3.6%, oil drops 4.6% in a commodity rout."),
    (26, "Sandisk sets 8-for-1 stock split", "Split-adjusted trading starts on Friday."),
    (27, "Pulsar hunt speeds up a million-fold", "New code finds dead stars in 30 seconds, not a year."),
    (28, "Webb sees rare star merger", "A supergiant swallows a sun-like star, a first."),
    (29, "NASA test-fires RS-25 engine", "A 200-second burn at Stennis for Artemis missions."),
    (30, "ESA picks seven-spacecraft Plasma Observatory", "Next medium mission eyes the late 2030s."),
    (31, "NASA offers $1m for Moon base ideas", "Student challenge to design a lunar outpost."),
    (32, "Space-station science to fight cancer", "ISS lab tests muscle-loss drugs and bioprinted liver."),
    (33, "Prince Harry 'ready to re-enlist'", "Duke says he would fight Russia in Ukraine."),
    (34, "Trump asks top court to block migrant shield", "Emergency bid over Venezuelan TPS protections."),
    (35, "43 soldiers re-enlist for GTA launch", "Four days off to play, in a Fort Stewart deal."),
    (36, "APEC adopts Shenzhen Outlook", "Leaders agree a voluntary agenda on trade, data, AI."),
    (37, "Saudi storms warning to Tuesday", "Heavy rain, hail and floods forecast in Mecca region."),
    (38, "Missile threat reported towards Riyadh", "Yemen coalition flags the threat."),
    (39, "Israel delays E1 settlement plan", "Settler kills a woman near Jericho, West Bank."),
    (40, "Seoul urges new talks with Pyongyang", "President Lee renews his dialogue appeal."),
    (41, "Flamengo edge Athletico-PR 2-1", "Cruzeiro beat Palmeiras 2-1 in Brazil's Serie A."),
    (42, "Svay Rieng rout Port FC 4-1", "Cambodians revive their ASEAN Club Championship bid."),
    (43, "Juventus Women beat Leuven 2-0", "Man Utd Women edge Everton 2-1 in the League Cup."),
    (44, "48 pepper genomes map chilli's heat", "Study traces domestication and where spice comes from."),
    (45, "NASA sets CRS-25 launch for 29 Nov", "Cargo mission to carry science to the space station."),
]


# ------------------------------------------------------------ illustrations
def pin(draw, x, y, n, color=RED):
    """Numbered map pin: filled circle + white number."""
    r = 9
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=(255, 255, 255), width=1)
    t = str(n)
    f = font(SANS_B, 10)
    w = draw.textlength(t, font=f)
    draw.text((x - w / 2, y - 7), t, font=f, fill=(255, 255, 255))


def draw_gta_panel(draw, x, y, w, h):
    """Original neon-sunset poster art: skyline, palms, two figures.
    No Rockstar logo, no official artwork, no trademarked fonts."""
    # sunset sky: horizontal bands
    bands = [(255, 158, 112), (255, 122, 140), (214, 92, 158), (122, 72, 150)]
    bh = h // 4
    for i, c in enumerate(bands):
        draw.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=c)
    # sun
    cx, cy, r = x + w // 2, y + int(h * 0.42), 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 130))
    # skyline blocks
    base = y + h
    for bx, bw, bh2 in [(0, 52, 58), (58, 38, 84), (102, 46, 66), (154, 40, 92),
                        (200, 50, 60), (256, 44, 78)]:
        draw.rectangle([x + bx, base - bh2, x + bx + bw, base], fill=(52, 32, 78))
        for wy in range(base - bh2 + 8, base - 6, 12):
            for wx in range(x + bx + 6, x + bx + bw - 6, 11):
                if (wx + wy) % 23 < 11:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 130))
    # palm silhouettes
    for px, ph in [(x + 18, 34), (x + w - 26, 28)]:
        draw.line([px, base, px, base - ph], fill=(30, 20, 52), width=3)
        for a in range(-3, 4):
            draw.arc([px - 14 + a * 4, base - ph - 8, px + 14 + a * 4, base - ph + 8],
                     200, 340, fill=(30, 20, 52), width=2)
    # two figures, back to back, centre foreground
    fx = x + w // 2
    for dx, col in [(-16, (30, 20, 52)), (14, (245, 240, 228))]:
        draw.ellipse([fx + dx - 6, base - 46, fx + dx + 6, base - 34], fill=col)
        draw.polygon([(fx + dx - 9, base - 34), (fx + dx + 9, base - 34),
                      (fx + dx + 6, base), (fx + dx - 6, base)], fill=col)
    # poster title bar
    draw.rectangle([x, y, x + w, y + 22], fill=(30, 20, 52))
    f = font(SANS_B, 13)
    t = "VICE CITY  ·  LEONIDA"
    tw = draw.textlength(t, font=f)
    draw.text((x + (w - tw) / 2, y + 4), t, font=f, fill=(255, 214, 130))


def draw_summit_panel(draw, x, y, w, h):
    """Three flags over a table: flat pastel diplomacy art."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 222, 196))
    # sky
    draw.rectangle([x, y, x + w, y + int(h * 0.55)], fill=SKY)
    draw.ellipse([x + w - 34, y + 8, x + w - 10, y + 32], fill=(255, 226, 150))
    # table
    draw.rectangle([x + 14, y + int(h * 0.62), x + w - 14, y + h - 10], fill=(120, 84, 58))
    draw.rectangle([x + 14, y + int(h * 0.62), x + w - 14, y + int(h * 0.62) + 6], fill=(150, 110, 76))
    # three flags (rectangular, larger)
    cols = [(178, 44, 36), (198, 142, 38), (42, 122, 120)]
    for i, c in enumerate(cols):
        fx = x + 24 + i * (w - 72) // 2
        draw.line([fx, y + 14, fx, y + int(h * 0.62)], fill=INK, width=2)
        draw.rectangle([fx, y + 14, fx + 34, y + 30], fill=c, outline=INK, width=1)
        # seated figure
        draw.ellipse([fx + 8, y + int(h * 0.66), fx + 20, y + int(h * 0.66) + 12], fill=INK)
        draw.polygon([(fx + 4, y + int(h * 0.66) + 12), (fx + 24, y + int(h * 0.66) + 12),
                      (fx + 22, y + h - 10), (fx + 6, y + h - 10)], fill=NAVY)


def draw_court_panel(draw, x, y, w, h):
    """Scales of justice before a courthouse: flat pastel art."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 222, 208))
    # courthouse
    draw.rectangle([x + 18, y + 16, x + w - 18, y + int(h * 0.6)], fill=(232, 222, 196),
                   outline=NAVY, width=2)
    draw.polygon([(x + 10, y + 16), (x + w // 2, y + 2), (x + w - 10, y + 16)], fill=NAVY)
    for i in range(4):
        cx = x + 34 + i * (w - 68) // 3
        draw.rectangle([cx - 5, y + 24, cx + 5, y + int(h * 0.6) - 4], fill=NAVY)
    # scales
    cx, top = x + w // 2, y + int(h * 0.62)
    draw.line([cx, top, cx, top + 34], fill=INK, width=3)
    draw.line([cx - 34, top + 4, cx + 34, top + 4], fill=INK, width=3)
    for dx in (-34, 34):
        draw.line([cx + dx, top + 4, cx + dx, top + 18], fill=INK, width=2)
        draw.polygon([(cx + dx - 12, top + 18), (cx + dx + 12, top + 18),
                      (cx + dx, top + 30)], fill=GOLD)
    draw.rectangle([cx - 16, top + 34, cx + 16, top + 40], fill=INK)


def draw_feature_icon(draw, x, y, w, h, kind):
    """Small flat icon per feature kind, pastel background."""
    bg = {"ipo": (214, 232, 214), "war": (238, 214, 204), "gulf": (214, 226, 238),
          "storm": (214, 222, 238), "market": (232, 226, 196), "climate": (204, 230, 214),
          "gaza": (238, 220, 214), "space": (214, 214, 238), "sport": (238, 226, 196)}
    draw.rectangle([x, y, x + w, y + h], fill=bg.get(kind, (232, 226, 196)))
    cx, cy = x + w // 2, y + h // 2
    if kind == "ipo":  # rising bars
        for i, bh in enumerate([10, 18, 26, 34]):
            draw.rectangle([x + 12 + i * 14, cy + 16 - bh, x + 22 + i * 14, cy + 16], fill=TEAL)
        draw.line([x + 10, cy - 20, x + w - 10, cy - 26], fill=RED, width=2)
    elif kind == "war":  # bridge: deck, arc, supports
        draw.line([x + 8, cy + 8, x + w - 8, cy + 8], fill=INK, width=3)
        draw.arc([x + 12, cy - 14, x + w - 12, cy + 22], 180, 360, fill=INK, width=3)
        for sx in (x + 20, x + w // 2, x + w - 20):
            draw.line([sx, cy - 6, sx, cy + 8], fill=INK, width=2)
    elif kind == "gulf":  # flame / tanker
        draw.rectangle([x + 10, cy + 2, x + w - 10, cy + 14], fill=NAVY)
        draw.polygon([(cx - 8, cy + 2), (cx, cy - 16), (cx + 8, cy + 2)], fill=RED)
    elif kind == "storm":  # spiral cloud
        draw.ellipse([x + 12, cy - 12, x + 38, cy + 6], fill=(120, 140, 170))
        draw.ellipse([x + 26, cy - 18, x + 52, cy + 4], fill=(150, 168, 196))
        draw.line([x + 18, cy + 10, x + 16, cy + 20], fill=TEAL, width=2)
        draw.line([x + 30, cy + 10, x + 28, cy + 20], fill=TEAL, width=2)
    elif kind == "market":  # candlesticks
        for i, (o, c) in enumerate([(0, 1), (1, 0), (0, 1)]):
            bx = x + 14 + i * 16
            draw.line([bx + 4, cy - 16, bx + 4, cy + 16], fill=INK, width=1)
            col = RED if c else TEAL
            draw.rectangle([bx, cy - 8 + o * 8, bx + 8, cy + 8 - o * 8], fill=col)
    elif kind == "climate":  # leaf + sun
        draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 214, 130))
        draw.polygon([(cx - 14, cy + 2), (cx, cy - 12), (cx + 14, cy + 2), (cx, cy + 14)], fill=SAGE)
    elif kind == "gaza":  # dove, grey on cream
        draw.ellipse([x + 14, cy - 6, x + w - 14, cy + 8], fill=(190, 196, 200), outline=INK, width=1)
        draw.polygon([(x + w - 16, cy - 4), (x + w - 2, cy - 12), (x + w - 6, cy + 2)],
                     fill=(190, 196, 200), outline=INK)
    elif kind == "space":  # planet + ring
        draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=LILAC)
        draw.arc([cx - 24, cy - 8, cx + 24, cy + 8], 200, 340, fill=GOLD, width=3)
        draw.ellipse([cx + 18, cy - 20, cx + 22, cy - 16], fill=GOLD)
    else:  # sport: ball
        draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(255, 255, 255), outline=INK, width=2)
        draw.polygon([(cx, cy - 6), (cx + 6, cy), (cx, cy + 6), (cx - 6, cy)], fill=INK)


FEATURE_KIND = {4: "ipo", 5: "war", 6: "gulf", 7: "storm", 8: "market",
                9: "climate", 10: "gaza", 11: "space", 12: "space", 13: "sport"}


def draw_map(draw, x, y, w, h):
    """Stylised world map: pastel continents, numbered pins, legend."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 236, 240))
    # continents as soft rounded blobs (stylised, not to scale)
    conts = [
        ("N AMERICA", (150, 190, 168), [(x + 30, y + 14, 150, 60), (x + 52, y + 74, 96, 36)]),
        ("S AMERICA", (168, 200, 150), [(x + 118, y + 112, 58, 34)]),
        ("EUROPE", (214, 196, 150), [(x + 430, y + 18, 92, 40)]),
        ("AFRICA", (232, 196, 140), [(x + 440, y + 62, 84, 72)]),
        ("ASIA", (232, 178, 150), [(x + 540, y + 12, 210, 60), (x + 560, y + 72, 120, 40)]),
        ("OCEANIA", (178, 196, 214), [(x + 790, y + 116, 66, 26)]),
    ]
    for name, col, rects in conts:
        for (rx, ry, rw, rh) in rects:
            draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=14, fill=col)
    # title + legend
    f_t = font(SANS_B, 13)
    draw.text((x + 10, y + 4), "WHERE IT HAPPENED", font=f_t, fill=NAVY)
    legend = [("N AMERICA", (150, 190, 168)), ("S AMERICA", (168, 200, 150)),
              ("EUROPE", (214, 196, 150)), ("AFRICA", (232, 196, 140)),
              ("ASIA", (232, 178, 150)), ("OCEANIA", (178, 196, 214))]
    lx = x + 10
    f_l = font(SANS, 9)
    for name, col in legend:
        draw.rectangle([lx, y + h - 14, lx + 9, y + h - 5], fill=col, outline=INK, width=1)
        draw.text((lx + 12, y + h - 15), name, font=f_l, fill=INK)
        lx += 12 + int(draw.textlength(name, font=f_l)) + 14
    # pins: (num, px, py) in panel coords — spaced so none overlap
    pins = [(1, 172, 78), (2, 700, 78), (3, 462, 48), (4, 187, 60),
            (5, 530, 55), (6, 570, 110), (7, 640, 120), (8, 205, 74),
            (9, 300, 118), (10, 505, 100), (13, 432, 30)]
    for n, px, py in pins:
        pin(draw, x + px, y + py, n)
    # space badge top-right: pins 11 (Voyager) and 12 (Artemis)
    bx, by = x + w - 118, y + 6
    draw.rounded_rectangle([bx, by, bx + 108, by + 30], radius=8, fill=NAVY)
    draw.text((bx + 8, by + 8), "SPACE", font=font(SANS_B, 11), fill=(255, 214, 130))
    pin(draw, bx + 66, by + 15, 11, color=NAVY)
    pin(draw, bx + 94, by + 15, 12, color=NAVY)


# ------------------------------------------------------------ page layout
M = 28  # margin


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    y = 16
    d.line([M, y + 6, W - M, y + 6], fill=RULE, width=2)
    centre(d, W // 2, y + 10, "THE DAY IN WORLD NEWS", font(SERIF_B, 46), NAVY)
    y = 74
    d.line([M, y, W - M, y], fill=RULE, width=1)
    f_sub = font(SANS_B, 12)
    centre(d, W // 2, y + 4, "THURSDAY, 19 NOVEMBER 2026  ·  45 STORIES  ·  6 CONTINENTS  ·  ONE DAY",
           f_sub, INK)
    y = 96
    d.line([M, y, W - M, y], fill=RULE, width=2)
    d.line([M, y + 3, W - M, y + 3], fill=RULE, width=1)

    # ---- heroes (3 columns) ----
    hy, hh = 108, 208
    col_w = (W - 2 * M - 2 * 12) // 3
    panels = [draw_gta_panel, draw_summit_panel, draw_court_panel]
    for i, (num, kick, head, deck, place) in enumerate(HEROES):
        x = M + i * (col_w + 12)
        panels[i](d, x, hy, col_w, 108)
        f_k = font(SANS_B, 10)
        d.text((x, hy + 114), kick, font=f_k, fill=RED)
        f_h = font(SERIF_B, 21 if len(head) < 22 else 18)
        yy = draw_wrapped(d, x, hy + 128, head, f_h, col_w, INK, leading=22)
        draw_wrapped(d, x, yy + 2, deck, font(SERIF, 12), col_w, (58, 62, 74), leading=15)
        # number badge
        d.ellipse([x + col_w - 18, hy + 112, x + col_w, hy + 130], fill=RED)
        f_n = font(SANS_B, 11)
        t = str(num)
        d.text((x + col_w - 9 - d.textlength(t, font=f_n) / 2, hy + 114), t, font=f_n,
               fill=(255, 255, 255))

    # ---- features, two rows of five ----
    def feature_row(fy, items):
        fw = (W - 2 * M - 4 * 10) // 5
        fh = 126
        for j, (num, kick, head, deck) in enumerate(items):
            x = M + j * (fw + 10)
            draw_feature_icon(d, x, fy, fw, 46, FEATURE_KIND[num])
            d.text((x, fy + 50), f"{num:02d}  ·  {kick}", font=font(SANS_B, 9), fill=RED)
            yy = draw_wrapped(d, x, fy + 62, head, font(SERIF_B, 12), fw, INK, leading=14)
            draw_wrapped(d, x, yy + 1, deck, font(SERIF, 10), fw, (58, 62, 74), leading=12)
        return fy + fh

    fy = 330
    d.line([M, 324, W - M, 324], fill=RULE, width=1)
    fy = feature_row(330, FEATURES[:5])
    d.line([M, fy + 4, W - M, fy + 4], fill=(180, 178, 168), width=1)
    fy = feature_row(fy + 12, FEATURES[5:])

    # ---- map ----
    my = fy + 12
    d.line([M, my - 4, W - M, my - 4], fill=RULE, width=1)
    draw_map(d, M, my, W - 2 * M, 150)

    # ---- briefs, two columns ----
    by = my + 158
    d.line([M, by - 4, W - M, by - 4], fill=RULE, width=1)
    d.text((M, by), "THE DAY IN BRIEF", font=font(SANS_B, 12), fill=NAVY)
    by += 18
    col_w2 = (W - 2 * M - 20) // 2
    f_bh = font(SERIF_B, 11)
    f_bb = font(SERIF, 10)
    for ci in range(2):
        x = M + ci * (col_w2 + 20)
        yy = by
        for (num, head, deck) in BRIEFS[ci * 16:(ci + 1) * 16]:
            d.text((x, yy), f"{num:02d}", font=font(SANS_B, 10), fill=RED)
            tx = x + 24
            yy2 = draw_wrapped(d, tx, yy, head, f_bh, col_w2 - 24, INK, leading=12)
            yy = yy2 + 1
        # separator between columns
        if ci == 0:
            d.line([M + col_w2 + 10, by, M + col_w2 + 10, by + 16 * 13], fill=(200, 198, 188), width=1)

    # ---- footer ----
    fy2 = by + 16 * 13 + 8
    d.line([M, fy2, W - M, fy2], fill=RULE, width=2)
    centre(d, W // 2, fy2 + 5,
           "Sources: Reuters  ·  AP  ·  AFP  ·  BBC  ·  Al Jazeera  ·  The Day in World News, Thursday 19 November 2026",
           font(SANS, 10), GREY)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
