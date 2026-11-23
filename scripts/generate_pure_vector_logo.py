import os, zlib, re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

assets_dir = r"C:\Users\restart\.gemini\antigravity\scratch\royal-safe-drive\assets"
pdf_path = r"C:\Users\restart\.gemini\antigravity\brain\f0b19f4c-392d-4781-8c35-06263a70f1c9\.user_uploaded\media_1795375525533_bb560c14.pdf"

font9 = TTFont(os.path.join(assets_dir, "font_9.ttf"))   # Brother-1816-Bold
font8 = TTFont(os.path.join(assets_dir, "font_8.ttf"))   # Urbanist-Regular
font12 = TTFont(os.path.join(assets_dir, "font_12.ttf")) # Bizmo-Black-Oblique

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

streams = re.findall(rb"stream\r?\n(.*?)\r?\nendstream", pdf_bytes, re.DOTALL)
s10 = zlib.decompress(streams[10]).decode("latin1")

def parse_pdf_ops(content):
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

car_paths = parse_pdf_ops(s10)

def get_text_paths(font, text, font_size, start_x, start_y, fill_color, letter_spacing=0):
    gset = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = font_size / font["head"].unitsPerEm
    curr_x = start_x
    out_svg = []
    
    for ch in text:
        gname = cmap.get(ord(ch))
        if not gname:
            continue
        pen = SVGPathPen(gset)
        gset[gname].draw(pen)
        d = pen.getCommands()
        adv = (font["hmtx"][gname][0] + letter_spacing) * scale
        if d:
            # In PDF coordinates:
            # Base line is at start_y. Font glyph coordinates are: positive Y upwards.
            # In PDF space, glyph with scale(s, s) at (curr_x, start_y) has Y pointing UP.
            # When the whole group is flipped by matrix(1 0 0 -1 0 1080),
            # both the car and the glyphs will flip together correctly!
            out_svg.append(f'    <path fill="{fill_color}" transform="translate({curr_x:.3f}, {start_y:.3f}) scale({scale:.6f}, {scale:.6f})" d="{d}"/>')
        curr_x += adv
    return "\n".join(out_svg), curr_x

# Page 2 coordinates from PDF:
# /TT0 94.9118 -> "Royal" at (962.8779, 560.812)
# /TT1 43.4444 -> "safe" at (1259.8154, 561.4595)
# /TT0 133 -> "Drive" at (962.8779, 455.812)

royal_svg, royal_end_x = get_text_paths(font9, "Royal", 94.91, 962.8779, 560.812, "#ffffff", letter_spacing=-20)
safe_svg, safe_end_x = get_text_paths(font8, "safe", 43.44, 1245.0, 564.0, "#ff1e27", letter_spacing=-10)
drive_svg, drive_end_x = get_text_paths(font12, "Drive", 133.0, 962.8779, 455.812, "#ffffff", letter_spacing=20)

# Build pure vector SVG
# Bounding box in PDF space:
# Car min x ~ 565, max x ~ 925
# Car min y ~ 450, max y ~ 635
# Text min x = 962.88, max x ~ 1380
# Text min y = 455.812 - 20 = 435, max y = 560.812 + 80 = 640
# In PDF: x ranges from 565 to 1390 (width 825)
# In PDF: y ranges from 440 to 640 (height 200)
#
# In SVG, we wrap the whole graphic in <g transform="matrix(1 0 0 -1 0 1080)">
# So y_svg ranges from 1080 - 640 = 440 to 1080 - 440 = 640.
# ViewBox: min-x: 565, min-y: 440, width: 825, height: 200.

full_logo_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="565 440 825 200" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
  <g transform="matrix(1 0 0 -1 0 1080)">
    <!-- Car Silhouette & RD Emblem -->
"""

for fill, tx, ty, d in car_paths:
    full_logo_svg += f'    <g transform="translate({tx:.4f}, {ty:.4f})">\n'
    full_logo_svg += f'      <path fill="{fill}" d="{d}"/>\n'
    full_logo_svg += f'    </g>\n'

full_logo_svg += f"""
    <!-- Pure Vector Typography: Royal safe Drive -->
{royal_svg}
{safe_svg}
{drive_svg}
  </g>
</svg>
"""

out_logo_path = os.path.join(assets_dir, "logo_horizontal.svg")
with open(out_logo_path, "w", encoding="utf-8") as f:
    f.write(full_logo_svg)

print(f"Generated 100% PURE VECTOR logo at {out_logo_path}")

# Also update car_emblem.svg
car_emblem_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="565 440 365 200" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
  <g transform="matrix(1 0 0 -1 0 1080)">
"""
for fill, tx, ty, d in car_paths:
    car_emblem_svg += f'    <g transform="translate({tx:.4f}, {ty:.4f})">\n'
    car_emblem_svg += f'      <path fill="{fill}" d="{d}"/>\n'
    car_emblem_svg += f'    </g>\n'
car_emblem_svg += """  </g>
</svg>"""

with open(os.path.join(assets_dir, "car_emblem.svg"), "w", encoding="utf-8") as f:
    f.write(car_emblem_svg)

# Also update favicon.svg
favicon_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" rx="120" fill="#07080a"/>
  <rect width="512" height="512" rx="120" fill="none" stroke="#ff1e27" stroke-width="8" opacity="0.4"/>
  <!-- Centered Car Icon -->
  <g transform="translate(256, 260) scale(1.05) translate(-747, -540)">
    <g transform="matrix(1 0 0 -1 0 1080)">
"""
for fill, tx, ty, d in car_paths:
    favicon_svg += f'      <g transform="translate({tx:.4f}, {ty:.4f})">\n'
    favicon_svg += f'        <path fill="{fill}" d="{d}"/>\n'
    favicon_svg += f'      </g>\n'
favicon_svg += """    </g>
  </g>
</svg>"""

with open(os.path.join(assets_dir, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(favicon_svg)

print("Generated car_emblem.svg and favicon.svg!")
