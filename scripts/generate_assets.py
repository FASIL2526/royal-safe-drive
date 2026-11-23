import zlib, re, os, base64

pdf_path = r"C:\Users\restart\.gemini\antigravity\brain\f0b19f4c-392d-4781-8c35-06263a70f1c9\.user_uploaded\media_1795375525533_bb560c14.pdf"
assets_dir = r"C:\Users\restart\.gemini\antigravity\scratch\royal-safe-drive\assets"
os.makedirs(assets_dir, exist_ok=True)

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

streams = re.findall(rb"stream\r?\n(.*?)\r?\nendstream", pdf_bytes, re.DOTALL)
print(f"Total streams found: {len(streams)}")

def parse_pdf_ops(content_bytes):
    content = zlib.decompress(content_bytes).decode("latin1")
    tokens = content.split()
    i = 0
    paths = []
    curr_fill = "#000000"
    curr_tx = 0.0
    curr_ty = 0.0
    stack = []
    
    while i < len(tokens):
        t = tokens[i]
        if t == "rg":
            r, g, b = float(tokens[i-3]), float(tokens[i-2]), float(tokens[i-1])
            curr_fill = f"#{int(round(r*255)):02x}{int(round(g*255)):02x}{int(round(b*255)):02x}"
            i += 1
        elif t == "cm":
            curr_tx = float(tokens[i-2])
            curr_ty = float(tokens[i-1])
            i += 1
        elif t == "q":
            stack.append((curr_fill, curr_tx, curr_ty))
            i += 1
        elif t == "Q":
            if stack:
                curr_fill, curr_tx, curr_ty = stack.pop()
            i += 1
        elif t == "m":
            d = []
            curr_x, curr_y = float(tokens[i-2]), float(tokens[i-1])
            d.append(f"M {curr_x:.4f} {curr_y:.4f}")
            i += 1
            while i < len(tokens) and tokens[i] not in ("f", "f*", "s", "S", "B", "B*"):
                op = tokens[i]
                if op == "l":
                    curr_x, curr_y = float(tokens[i-2]), float(tokens[i-1])
                    d.append(f"L {curr_x:.4f} {curr_y:.4f}")
                elif op == "c":
                    x1, y1 = float(tokens[i-6]), float(tokens[i-5])
                    x2, y2 = float(tokens[i-4]), float(tokens[i-3])
                    curr_x, curr_y = float(tokens[i-2]), float(tokens[i-1])
                    d.append(f"C {x1:.4f} {y1:.4f} {x2:.4f} {y2:.4f} {curr_x:.4f} {curr_y:.4f}")
                elif op == "v":
                    x2, y2 = float(tokens[i-4]), float(tokens[i-3])
                    next_x, next_y = float(tokens[i-2]), float(tokens[i-1])
                    d.append(f"C {curr_x:.4f} {curr_y:.4f} {x2:.4f} {y2:.4f} {next_x:.4f} {next_y:.4f}")
                    curr_x, curr_y = next_x, next_y
                elif op == "y":
                    x1, y1 = float(tokens[i-4]), float(tokens[i-3])
                    curr_x, curr_y = float(tokens[i-2]), float(tokens[i-1])
                    d.append(f"C {x1:.4f} {y1:.4f} {curr_x:.4f} {curr_y:.4f} {curr_x:.4f} {curr_y:.4f}")
                elif op == "h":
                    d.append("Z")
                i += 1
            paths.append((curr_fill, curr_tx, curr_ty, " ".join(d)))
            i += 1
        else:
            i += 1
    return paths

# Parse Stream 1 (Page 1)
paths_s1 = parse_pdf_ops(streams[1])
print(f"Paths in Stream 1: {len(paths_s1)}")

# Convert fonts to base64 for embedding in SVG
font_css = []
font_files = {
    "Brother-Bold": os.path.join(assets_dir, "font_9.ttf"),
    "Bizmo-Black": os.path.join(assets_dir, "font_12.ttf"),
    "Urbanist-Regular": os.path.join(assets_dir, "font_8.ttf"),
    "CarlaSans": os.path.join(assets_dir, "font_15.ttf")
}

for font_family, path in font_files.items():
    if os.path.exists(path):
        with open(path, "rb") as font_f:
            b64_font = base64.b64encode(font_f.read()).decode("ascii")
            font_css.append(f"""
@font-face {{
    font-family: '{font_family}';
    src: url(data:font/truetype;charset=utf-8;base64,{b64_font}) format('truetype');
    font-weight: normal;
    font-style: normal;
}}""")

css_block = "\n".join(font_css)

# Generate high quality SVG for Page 1 Logo
# Page 1 text:
# Royal (size ~95, Tm 986.062 557.0166)
# Drive (size ~133, Tm 986.062 452.0166)
# safe (size ~39.4, Tm 1246.2476 554.6704)
# In PDF: y is up, 1080 is top.
# In SVG: y is down.

svg_full = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="480 380 960 320" width="960" height="320">
<defs>
<style>
{css_block}
.txt-royal {{
    font-family: 'CarlaSans', 'Urbanist', 'Cinzel', sans-serif;
    font-size: 95px;
    letter-spacing: 2px;
    fill: #ffffff;
}}
.txt-safe {{
    font-family: 'Brother-Bold', 'Brush Script MT', cursive, sans-serif;
    font-size: 39px;
    fill: #ff1e27;
}}
.txt-drive {{
    font-family: 'Brother-Bold', 'Bizmo-Black', 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 133px;
    letter-spacing: -2px;
    fill: #ffffff;
}}
</style>
</defs>
<rect x="480" y="380" width="960" height="320" fill="transparent"/>
<g transform="matrix(1 0 0 -1 0 1080)">
"""

for fill, tx, ty, d in paths_s1:
    svg_full += f'  <g transform="translate({tx:.4f}, {ty:.4f})">\n'
    svg_full += f'    <path fill="{fill}" d="{d}"/>\n'
    svg_full += f'  </g>\n'

# Add text elements in PDF coordinate space
svg_full += f"""
  <text x="986.062" y="557.0166" class="txt-royal">ROYAL</text>
  <text x="1270" y="565" class="txt-safe">safe</text>
  <text x="986.062" y="452.0166" class="txt-drive">DRIVE</text>
</g>
</svg>
"""

with open(os.path.join(assets_dir, "royal_safe_drive_logo.svg"), "w", encoding="utf-8") as f:
    f.write(svg_full)

# Also generate a standalone Car Emblem SVG (viewBox around the car itself)
# Car bounds: roughly x from 590 to 950 (width 360), y from 450 to 650 (height 200)
car_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="580 430 380 230" width="380" height="230">
<g transform="matrix(1 0 0 -1 0 1080)">
"""
for fill, tx, ty, d in paths_s1:
    car_svg += f'  <g transform="translate({tx:.4f}, {ty:.4f})">\n'
    car_svg += f'    <path fill="{fill}" d="{d}"/>\n'
    car_svg += f'  </g>\n'
car_svg += """
</g>
</svg>
"""

with open(os.path.join(assets_dir, "car_emblem.svg"), "w", encoding="utf-8") as f:
    f.write(car_svg)

print("Successfully generated royal_safe_drive_logo.svg and car_emblem.svg!")
