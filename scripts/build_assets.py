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

# Bottom (L0) to top (L6).
LAYERS = [
    ("Physics", "BS Physics, Bahauddin Zakariya University", "CGPA 3.61"),
    ("Devices", "2D MOSFET TCAD: Poisson + drift-diffusion", "V_TH · I_ON/I_OFF · SS"),
    ("Circuits", "CMOS ring oscillator & current-starved VCO", "109× tuning range"),
    ("Chips", "Edge-AI MAC accelerator, RTL → GDSII on SKY130", "−62.8% energy"),
    ("Systems", "Solar-powered smart irrigation on ATmega328P", "−80% water use"),
    ("Software", "Next.js, React Native, FastAPI, .NET, Supabase", "web + mobile, shipped"),
    ("Agents", "LangGraph RAG, autonomous scheduling, work agents", "LangChain · LangGraph"),
]

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

TOOLKIT = [
    ("Silicon", "amber", ["SystemVerilog", "Verilog", "VHDL", "Yosys", "OpenROAD", "OpenLane",
                          "Magic", "Netgen", "NGSpice", "SKY130", "Cadence"]),
    ("Devices", "amber", ["DEVSIM", "TCAD", "LTspice", "PSPICE", "MATLAB", "NumPy", "Pandas"]),
    ("Embedded", "amber", ["C / C++", "Arduino", "ESP32", "ESP8266", "KiCad", "Oscilloscope"]),
    ("Software", "teal", ["TypeScript", "Python", "C#", "Next.js", "React Native", ".NET",
                          "FastAPI", "Supabase", "Firebase", "Docker", "Git"]),
    ("AI", "teal", ["LangChain", "LangGraph", "RAG", "pgvector", "scikit-learn"]),
]

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


# ---------------------------------------------------------------- stack


def stack(c):
    W, rowh, gap, top = 1200, 62, 12, 104
    H = top + len(LAYERS) * (rowh + gap) + 20
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{c["panel"]}" stroke="{c["border"]}"/>',
         f'<text x="48" y="58" font-family="{SANS}" font-size="28" font-weight="700" fill="{c["text"]}">One stack, electrons to agents</text>',
         f'<text x="48" y="84" font-family="{SANS}" font-size="16" fill="{c["muted"]}">Each layer is something I have built on, and each builds on the one below.</text>']
    rail_x = 80
    y_first = top + rowh / 2
    y_last = top + (len(LAYERS) - 1) * (rowh + gap) + rowh / 2
    b.append(f'<line x1="{rail_x}" y1="{y_first}" x2="{rail_x}" y2="{y_last}" stroke="{c["border"]}" stroke-width="2"/>')
    b.append(f'<path class="pulse" d="M{rail_x},{y_last} V{y_first}" stroke="{c["teal"]}" stroke-width="3"/>')
    for idx, (name, detail, metric) in enumerate(reversed(LAYERS)):
        level = len(LAYERS) - 1 - idx
        col = lerp_hex(c["amber"], c["teal"], level / (len(LAYERS) - 1))
        y = top + idx * (rowh + gap)
        mid = y + rowh / 2
        b.append(f'<rect x="112" y="{y}" width="{W-160}" height="{rowh}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>')
        b.append(f'<rect x="112" y="{y}" width="6" height="{rowh}" rx="3" fill="{col}"/>')
        b.append(f'<circle cx="{rail_x}" cy="{mid}" r="9" fill="{c["panel"]}" stroke="{col}" stroke-width="2.5"/>')
        b.append(f'<text x="140" y="{mid+6}" font-family="{MONO}" font-size="15" fill="{c["muted"]}">L{level}</text>')
        b.append(f'<text x="184" y="{mid+7}" font-family="{SANS}" font-size="20" font-weight="700" fill="{c["text"]}">{e(name)}</text>')
        b.append(f'<text x="320" y="{mid+6}" font-family="{SANS}" font-size="16" fill="{c["muted"]}">{e(detail)}</text>')
        b.append(f'<text x="{W-72}" y="{mid+6}" text-anchor="end" font-family="{MONO}" font-size="15" font-weight="700" fill="{col}">{e(metric)}</text>')
    return svg(W, H, "".join(b), "Stack from physics to AI agents", pulse_css(c))


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


# ---------------------------------------------------------------- toolkit


def toolkit(c):
    W, pad_l, chip_h, row_gap = 1200, 190, 36, 14
    rows, y = [], 96
    for name, accent, items in TOOLKIT:
        x, first_y, placed = pad_l, y, []
        for it in items:
            w = text_w(it, 15) + 26
            if x + w > W - 40:
                x, y = pad_l, y + chip_h + 10
            placed.append((x, y, w, it))
            x += w + 10
        rows.append((name, accent, first_y, placed))
        y += chip_h + row_gap + 10
    H = y + 14
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{c["panel"]}" stroke="{c["border"]}"/>',
         f'<text x="48" y="58" font-family="{SANS}" font-size="28" font-weight="700" fill="{c["text"]}">Toolkit</text>']
    for name, accent, ry, placed in rows:
        col = c[accent]
        b.append(f'<text x="48" y="{ry+24}" font-family="{MONO}" font-size="15" font-weight="700" fill="{col}">{e(name)}</text>')
        for x, cy, w, it in placed:
            b.append(f'<rect x="{x:.0f}" y="{cy}" width="{w:.0f}" height="{chip_h}" rx="8" fill="{c["bg"]}" stroke="{c["border"]}"/>')
            b.append(f'<text x="{x + w/2:.0f}" y="{cy+23}" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{c["text"]}">{e(it)}</text>')
    return svg(W, H, "".join(b), "Toolkit: silicon, devices, embedded, software and AI tools")


# ---------------------------------------------------------------- main


def main():
    OUT.mkdir(exist_ok=True)
    for theme, c in THEMES.items():
        (OUT / f"hero-{theme}.svg").write_text(hero(c), encoding="utf-8")
        (OUT / f"stack-{theme}.svg").write_text(stack(c), encoding="utf-8")
        (OUT / f"toolkit-{theme}.svg").write_text(toolkit(c), encoding="utf-8")
        for key, d in CARDS.items():
            (OUT / f"card-{key}-{theme}.svg").write_text(card(c, d), encoding="utf-8")
    print("wrote", len(list(OUT.glob("*.svg"))), "SVGs to", OUT)


if __name__ == "__main__":
    main()
