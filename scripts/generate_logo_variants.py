import os, base64

assets_dir = r"C:\Users\restart\.gemini\antigravity\scratch\royal-safe-drive\assets"

# Read the paths generated previously
with open(os.path.join(assets_dir, "royal_safe_drive_logo.svg"), "r", encoding="utf-8") as f:
    orig = f.read()

# Extract defs style
defs_match = orig[orig.find("<defs>"):orig.find("</defs>")+7]

# Extract car paths
paths_start = orig.find("<g transform=\"translate(")
paths_end = orig.find("<text x=\"986.062\"")
paths_block = orig[paths_start:paths_end]

# 1. Main Horizontal Brand Logo (Car on Left + Royal safe Drive on Right)
# x: 580 to 1380 (width: 800), y: 430 to 650 (height: 220)
horizontal_logo = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="580 430 800 220" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
{defs_match}
<g transform="matrix(1 0 0 -1 0 1080)">
{paths_block}
  <text x="980" y="557" class="txt-royal">ROYAL</text>
  <text x="1275" y="563" class="txt-safe">safe</text>
  <text x="980" y="452" class="txt-drive">DRIVE</text>
</g>
</svg>"""

with open(os.path.join(assets_dir, "logo_horizontal.svg"), "w", encoding="utf-8") as f:
    f.write(horizontal_logo)

# 2. Car Emblem Only (for Favicon, Navbar icon, Floating badge)
# Car bounds: x: 590 to 955, y: 440 to 640
car_icon = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="595 440 365 200" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
<g transform="matrix(1 0 0 -1 0 1080)">
{paths_block}
</g>
</svg>"""

with open(os.path.join(assets_dir, "car_emblem.svg"), "w", encoding="utf-8") as f:
    f.write(car_icon)

# 3. Favicon SVG (square format with dark rounded background)
favicon_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
<rect width="512" height="512" rx="128" fill="#0d0e12"/>
<rect width="512" height="512" rx="128" fill="none" stroke="#ff1e27" stroke-width="8" opacity="0.6"/>
<g transform="translate(256, 230) scale(0.9) translate(-777, -540)">
  <g transform="matrix(1 0 0 -1 0 1080)">
{paths_block}
  </g>
</g>
<text x="256" y="440" text-anchor="middle" font-family="'Brother-Bold', 'Montserrat', sans-serif" font-weight="900" font-size="52" fill="#ffffff" letter-spacing="3">ROYAL DRIVE</text>
</svg>"""

with open(os.path.join(assets_dir, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(favicon_svg)

print("Generated logo_horizontal.svg, car_emblem.svg, and favicon.svg successfully!")
