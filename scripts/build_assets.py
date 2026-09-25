"""Generate the light/dark SVG assets used by the profile README.

Edit the data below, then run:  python3 scripts/build_assets.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3",
                 muted="#8b949e", faint="#21262d", teal="#2dd4bf", amber="#f5b14c"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", faint="#e6eaef", teal="#0f766e", amber="#b45309"),
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# ---------------------------------------------------------------- content

HERO = dict(
    handle="// mali-anjum",
    name="Muhammad Ali Anjum",
    tagline="Physics graduate building from electrons to agents.",
    pills=["Semiconductor devices", "IC design · SKY130", "Full-stack", "AI agents"],
    footer="Multan, PK  ·  alianjum.vercel.app",
)

CARDS = {
    "asic": dict(
        label="DIGITAL IC · RTL → GDSII", title="Edge-AI ASIC Accelerator",
        desc="4-PE INT8/INT4 MAC array, DRC/LVS-clean GDSII",
        metrics=[("−29.9%", "area"), ("−62.8%", "energy / inference"), ("3.74 ns", "setup slack")],
        stack="SystemVerilog · Yosys · OpenROAD · Magic · Netgen", accent="amber"),
    "vco": dict(
        label="ANALOG / MIXED-SIGNAL", title="CMOS Ring Oscillator & VCO",
        desc="Transistor-level design to custom layout in SKY130",
        metrics=[("109×", "tuning range"), ("2.31 GHz", "max frequency"), ("27-pt", "PVT sweep")],
        stack="NGSpice · Magic · Netgen · Python", accent="amber"),
    "tcad": dict(
        label="SEMICONDUCTOR DEVICES", title="2D MOSFET TCAD Study",
        desc="Poisson + drift-diffusion from first principles",
        metrics=[("3-axis", "L · t_ox · N_A sweep"), ("5", "auto-extracted metrics"), ("1D PN", "analytic validation")],
        stack="DEVSIM · Python · NumPy · Matplotlib", accent="amber"),
    "aios": dict(
        label="AI AGENTS · RAG", title="AI Executive OS",
        desc="Multi-tenant RAG workspace with cited, streamed answers",
        metrics=[("LangGraph", "knowledge agent"), ("pgvector", "retrieval"), ("Celery", "ingest pipeline")],
        stack="Next.js · FastAPI · Supabase · Redis", accent="teal"),
    "workpilot": dict(
        label="AI AGENTS · .NET", title="WorkPilot",
        desc="Personal agent that finds, prepares and tracks work",
        metrics=[("Approval", "gated actions"), ("Multi-LLM", "OpenAI · DeepSeek"), ("Blazor", "web front end")],
        stack=".NET · Aspire · EF Core · Supabase · xUnit", accent="teal"),
    "enginuity": dict(
        label="MOBILE · REACT NATIVE", title="Enginuity",
        desc="Engineering workspace for students & researchers",
        metrics=[("2", "platforms (iOS/Android)"), ("3", "OAuth providers"), ("FTS", "global search")],
        stack="Expo Router · Redux Toolkit · Supabase", accent="teal"),
}

# ---------------------------------------------------------------- helpers


def e(s):
    return escape(s)


def lerp_hex(a, b, t):
    a, b = a.lstrip("#"), b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


def text_w(s, size, mono=False):
    return len(s) * size * (0.61 if mono else 0.5)


def svg(w, h, body, title, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)}">'
            f'<title>{e(title)}</title><style>{style}'
            '@media (prefers-reduced-motion: reduce){*{animation:none!important}}'
            f'</style>{body}</svg>\n')


def pulse_css(c):
    return ('.pulse{fill:none;stroke-linecap:round;stroke-dasharray:28 900;'
            'animation:run 3.2s linear infinite}'
            '@keyframes run{from{stroke-dashoffset:928}to{stroke-dashoffset:0}}'
            '.blink{animation:blink 2.4s ease-in-out infinite}'
            '@keyframes blink{0%,100%{opacity:.25}50%{opacity:1}}')


# ---------------------------------------------------------------- hero


def hero(c):
    W, H = 1200, 340
    b = [f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
         f'<stop offset="0" stop-color="{c["panel"]}"/><stop offset="1" stop-color="{c["bg"]}"/>'
         f'</linearGradient><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
         f'<circle cx="1.5" cy="1.5" r="1.2" fill="{c["faint"]}"/></pattern></defs>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="url(#g)" stroke="{c["border"]}"/>',
         f'<rect x="700" y="1" width="499" height="{H-2}" rx="18" fill="url(#dots)"/>']

    # chip
    cx, cy, s = 950, 170, 170
    x0, y0 = cx - s / 2, cy - s / 2
    traces = []
    n = 7
    for i in range(n):
        o = x0 + 22 + i * (s - 44) / (n - 1)
        # pins
        b.append(f'<rect x="{o-4:.1f}" y="{y0-16}" width="8" height="16" rx="1.5" fill="{c["border"]}"/>')
        b.append(f'<rect x="{o-4:.1f}" y="{y0+s}" width="8" height="16" rx="1.5" fill="{c["border"]}"/>')
        b.append(f'<rect x="{x0-16}" y="{o-x0+y0-4:.1f}" width="16" height="8" rx="1.5" fill="{c["border"]}"/>')
        b.append(f'<rect x="{x0+s}" y="{o-x0+y0-4:.1f}" width="16" height="8" rx="1.5" fill="{c["border"]}"/>')
    # routed traces from pins to the edges
    ys = [y0 + 22 + i * (s - 44) / (n - 1) for i in range(n)]
    for k, i in enumerate((1, 3, 5)):
        y = ys[i]
        traces.append(f'M{x0+s+16},{y:.1f} H{1110+k*18} V{40+k*12 if k != 1 else y:.1f} H1200')
        traces.append(f'M{x0-16},{y:.1f} H{760-k*14} V{H-40-k*12 if k != 1 else y:.1f} H700')
    for k, path in enumerate(traces):
        col = c["teal"] if k % 2 == 0 else c["amber"]
        b.append(f'<path d="{path}" fill="none" stroke="{c["border"]}" stroke-width="2"/>')
        b.append(f'<path class="pulse" d="{path}" stroke="{col}" stroke-width="2.5" '
                 f'style="animation-delay:{k*0.45:.2f}s"/>')
    b.append(f'<rect x="{x0}" y="{y0}" width="{s}" height="{s}" rx="12" fill="{c["panel"]}" stroke="{c["border"]}" stroke-width="2"/>')
    b.append(f'<rect x="{x0+18}" y="{y0+18}" width="{s-36}" height="{s-36}" rx="6" fill="none" stroke="{c["teal"]}" stroke-opacity=".55" stroke-dasharray="4 5"/>')
    b.append(f'<circle class="blink" cx="{x0+30}" cy="{y0+30}" r="4" fill="{c["amber"]}"/>')
    b.append(f'<text x="{cx}" y="{cy-4}" text-anchor="middle" font-family="{MONO}" font-size="22" font-weight="700" fill="{c["text"]}">MA-01</text>')
    b.append(f'<text x="{cx}" y="{cy+22}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{c["muted"]}">SKY130 · 2026</text>')

    # text block
    b.append(f'<text x="64" y="88" font-family="{MONO}" font-size="16" fill="{c["teal"]}">{e(HERO["handle"])}</text>')
    b.append(f'<text x="62" y="148" font-family="{SANS}" font-size="52" font-weight="700" fill="{c["text"]}">{e(HERO["name"])}</text>')
    b.append(f'<text x="64" y="190" font-family="{SANS}" font-size="22" fill="{c["muted"]}">{e(HERO["tagline"])}</text>')
    x = 64
    for i, p in enumerate(HERO["pills"]):
        w = text_w(p, 14) + 30
        col = c["amber"] if i < 2 else c["teal"]
        b.append(f'<rect x="{x}" y="216" width="{w:.0f}" height="32" rx="16" fill="none" stroke="{col}" stroke-opacity=".7"/>')
        b.append(f'<text x="{x + w/2:.0f}" y="237" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{col}">{e(p)}</text>')
        x += w + 10
    b.append(f'<text x="64" y="290" font-family="{MONO}" font-size="14" fill="{c["muted"]}">{e(HERO["footer"])}</text>')
    return svg(W, H, "".join(b), f'{HERO["name"]}: {HERO["tagline"]}', pulse_css(c))


# ---------------------------------------------------------------- cards


def card(c, d):
    W, H = 600, 280
    col = c[d["accent"]]
    b = [f'<clipPath id="r"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16"/></clipPath>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{c["panel"]}" stroke="{c["border"]}"/>',
         f'<rect x="1" y="1" width="{W-2}" height="5" fill="{col}" clip-path="url(#r)"/>',
         f'<text x="32" y="48" font-family="{MONO}" font-size="15" letter-spacing="1" fill="{col}">{e(d["label"])}</text>',
         f'<text x="32" y="90" font-family="{SANS}" font-size="30" font-weight="700" fill="{c["text"]}">{e(d["title"])}</text>',
         f'<text x="32" y="124" font-family="{SANS}" font-size="18" fill="{c["muted"]}">{e(d["desc"])}</text>',
         f'<line x1="32" y1="150" x2="{W-32}" y2="150" stroke="{c["border"]}"/>']
    for i, (v, lbl) in enumerate(d["metrics"]):
        x = 32 + i * 186
        b.append(f'<text x="{x}" y="194" font-family="{SANS}" font-size="28" font-weight="700" fill="{c["text"]}">{e(v)}</text>')
        b.append(f'<text x="{x}" y="218" font-family="{SANS}" font-size="15" fill="{c["muted"]}">{e(lbl)}</text>')
    b.append(f'<text x="32" y="254" font-family="{MONO}" font-size="14" fill="{c["muted"]}">{e(d["stack"])}</text>')
    b.append(f'<text x="{W-32}" y="254" text-anchor="end" font-family="{SANS}" font-size="20" fill="{col}">→</text>')
    return svg(W, H, "".join(b), f'{d["title"]}: {d["desc"]}')


# ---------------------------------------------------------------- typing line

TYPED = [
    "> based in Multan, Pakistan",
    "> designing low-power silicon on SKY130",
    "> modelling MOSFETs from first principles",
    "> shipping full-stack apps & AI agents",
]


def typing(c):
    W, H, size = 900, 50, 26
    cw = size * 0.6
    per_char, hold, erase = 0.055, 1.8, 0.35
    slots = [len(t) * per_char + hold + erase for t in TYPED]
    T = sum(slots)
    b, start = [], 0.0
    for i, line in enumerate(TYPED):
        n = len(line)
        w_full = n * cw
        x = (W - w_full) / 2
        # discrete keyframes: (time_s, visible_chars)
        frames = [(0.0, 0)]
        frames += [(start + k * per_char, k) for k in range(1, n + 1)]
        t_erase = start + n * per_char + hold
        steps = 6
        frames += [(t_erase + j * erase / steps, round(n * (1 - j / steps))) for j in range(1, steps + 1)]
        frames = sorted({round(t / T, 5): v for t, v in frames}.items())
        kt = ";".join(f"{t:g}" for t, _ in frames)
        widths = ";".join(f"{v * cw:.1f}" for _, v in frames)
        cursor = ";".join(f"{x + v * cw:.1f}" for _, v in frames)
        on = ";".join("1" if start <= t * T < start + slots[i] - 1e-6 else "0" for t, _ in frames)
        anim = f'dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}"'
        b.append(f'<clipPath id="c{i}"><rect x="{x:.1f}" y="0" height="{H}" width="0">'
                 f'<animate attributeName="width" values="{widths}" {anim}/></rect></clipPath>')
        b.append(f'<g opacity="0"><animate attributeName="opacity" values="{on}" {anim}/>'
                 f'<text x="{x:.1f}" y="35" textLength="{w_full:.1f}" lengthAdjust="spacing" '
                 f'font-family="{MONO}" font-size="{size}" fill="{c["teal"]}" clip-path="url(#c{i})">{e(line)}</text>'
                 f'<rect x="{x:.1f}" y="12" width="3" height="28" fill="{c["teal"]}">'
                 f'<animate attributeName="x" values="{cursor}" {anim}/></rect></g>')
        start += slots[i]
    return svg(W, H, "".join(b), " / ".join(t.lstrip("> ") for t in TYPED))


# ---------------------------------------------------------------- tech row

ICON_DIR = Path(__file__).resolve().parent / "icons"

# Hand-drawn stroke glyphs (24x24) for tools simple-icons does not cover.
GLYPHS = {
    "hdl": "M8 7 3 12l5 5M16 7l5 5-5 5M14 4l-4 16",
    "chip": "M7 7h10v10H7zM10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4",
    "wave": "M2 12c2.5-8 5.5-8 8 0s5.5 8 8 0 2 0 4 0",
}

# (label, simple-icons slug or glyph name, accent)
TECH = [
    [("SystemVerilog", "hdl"), ("Verilog", "hdl"), ("VHDL", "hdl"), ("Yosys", "chip"), ("OpenROAD", "chip"),
     ("OpenLane", "chip"), ("Magic", "chip"), ("Netgen", "chip"), ("SKY130", "chip")],
    [("NGSpice", "wave"), ("LTspice", "wave"), ("DEVSIM", "wave"), ("MATLAB", "mathworks"), ("Cadence", "chip"),
     ("Arduino", "arduino"), ("ESP32", "espressif"), ("KiCad", "kicad"), ("C++", "cplusplus")],
    [("Python", "python"), ("TypeScript", "typescript"), ("C#", "csharp"), (".NET", "dotnet"), ("React", "react"),
     ("Next.js", "nextdotjs"), ("Expo", "expo"), ("FastAPI", "fastapi"), ("Node.js", "nodedotjs")],
    [("LangChain", "langchain"), ("Supabase", "supabase"), ("PostgreSQL", "postgresql"), ("Redis", "redis"),
     ("Firebase", "firebase"), ("Docker", "docker"), ("Git", "git"), ("Linux", "linux"), ("NumPy", "numpy")],
]
TECH_ACCENT = ["amber", "amber", "teal", "teal"]


def icon(slug, x, y, size, col):
    s = size / 24
    if slug in GLYPHS:
        return (f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.3f})" d="{GLYPHS[slug]}" fill="none" '
                f'stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    raw = (ICON_DIR / f"{slug}.svg").read_text()
    d = raw.split(' d="', 1)[1].split('"', 1)[0]
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.3f})" d="{d}" fill="{col}"/>'


def tech(c):
    W, row_h, isz, gap, fs = 1100, 42, 20, 26, 16
    H = len(TECH) * row_h + 12
    b = []
    for r, row in enumerate(TECH):
        col = c[TECH_ACCENT[r]]
        widths = [isz + 7 + len(lbl) * fs * 0.58 for lbl, _ in row]
        x = (W - sum(widths) - gap * (len(row) - 1)) / 2
        y = 10 + r * row_h
        for (lbl, slug), w in zip(row, widths):
            b.append(icon(slug, x, y, isz, col))
            b.append(f'<text x="{x + isz + 7:.1f}" y="{y + 16}" font-family="{SANS}" font-size="{fs}" '
                     f'fill="{c["text"]}">{e(lbl)}</text>')
            x += w + gap
    labels = ", ".join(lbl for row in TECH for lbl, _ in row)
    return svg(W, H, "".join(b), f"Tech: {labels}")


# ---------------------------------------------------------------- link icons

LINK_COLOR = "#14b8a6"  # mid teal, readable on both GitHub themes
LINK_ICONS = {
    "globe": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM2 12h20M12 2c2.8 3 4 6.5 4 10s-1.2 7-4 10c-2.8-3-4-6.5-4-10s1.2-7 4-10z",
    "mail": "M3 6h18v12H3zM3 7l9 6 9-6",
    "pen": "M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4",
}

# ---------------------------------------------------------------- main


def main():
    OUT.mkdir(exist_ok=True)
    for theme, c in THEMES.items():
        (OUT / f"hero-{theme}.svg").write_text(hero(c), encoding="utf-8")
        (OUT / f"typing-{theme}.svg").write_text(typing(c), encoding="utf-8")
        (OUT / f"tech-{theme}.svg").write_text(tech(c), encoding="utf-8")
        for key, d in CARDS.items():
            (OUT / f"card-{key}-{theme}.svg").write_text(card(c, d), encoding="utf-8")
    (OUT / "icons").mkdir(exist_ok=True)
    for name, d in LINK_ICONS.items():
        (OUT / "icons" / f"{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
            f'fill="none" stroke="{LINK_COLOR}" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round"><path d="{d}"/></svg>\n', encoding="utf-8")
    print("wrote", len(list(OUT.glob("*.svg"))), "SVGs to", OUT)


if __name__ == "__main__":
    main()
