#!/usr/bin/env python3
"""Build meme.png for the make.fun gta6-meme-x-01 bounty.

Takes the AI-generated Vice City sunset background, centre-crops it to a
1080x1080 square, composites make.fun's press-kit ghost into the scene
(standing on the road beside the pink convertible, not pasted in a corner),
and draws the caption in large bold letters with a heavy outline so it stays
readable when the judge shrinks the picture to 480x480.

Caption:
    WAITED 13 YEARS
    FOR GTA 6
    (ghost)
    CALLED IN SICK.
    WORTH IT.
    make.fun

Run from the repository root:  python3 make_meme.py
Writes meme.png (1080x1080) next to this script.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter

BG = "media-generation-vice-city-sunset-bg-0-ad2a9ba8-a76f-426a-8884-1bc09fda9f8a.png"
GHOST = "assets-ghost.png"
OUT = "meme.png"
SIZE = 1080

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (226, 0, 122)  # make.fun magenta


def fit_font(draw, text, max_width, start_size):
    """Largest bold font size at which `text` fits in max_width."""
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT_BOLD, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(FONT_BOLD, 20)


def outlined_text(draw, xy, text, font, fill, stroke_width):
    draw.text(xy, text, font=font, fill=fill, stroke_width=stroke_width,
              stroke_fill=BLACK, anchor="ma")


def main():
    bg = Image.open(BG).convert("RGB")
    w, h = bg.size
    side = min(w, h)
    # Centre-crop to a square, then scale to the final size.
    bg = bg.crop(((w - side) // 2, (h - side) // 2,
                  (w - side) // 2 + side, (h - side) // 2 + side))
    bg = bg.resize((SIZE, SIZE), Image.LANCZOS)
    draw = ImageDraw.Draw(bg, "RGBA")

    # Soft vertical gradients behind the captions so white letters read
    # anywhere, fading out with no hard edge.
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for yy in range(0, 340):
        a = int(90 * (1 - yy / 340))
        od.line((0, yy, SIZE, yy), fill=(0, 0, 0, a))
    for yy in range(780, SIZE):
        a = int(100 * (yy - 780) / (SIZE - 780))
        od.line((0, yy, SIZE, yy), fill=(0, 0, 0, a))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(bg, "RGBA")

    # Top caption.
    top_lines = ["WAITED 13 YEARS", "FOR GTA 6"]
    y = 48
    for line in top_lines:
        font = fit_font(draw, line, SIZE - 80, 118)
        outlined_text(draw, (SIZE // 2, y), line, font, WHITE, 10)
        y += font.size + 8

    # The ghost, worked into the scene: standing on the left sidewalk in
    # front of the pink art-deco hotel, holding its magenta star coin,
    # watching the convertible cruise past. (The press-kit asset is the
    # make.fun mark itself: white ghost on a magenta disc.)
    ghost = Image.open(GHOST).convert("RGBA")
    ghost_h = 340
    ghost = ghost.resize((int(ghost.width * ghost_h / ghost.height), ghost_h),
                         Image.LANCZOS)
    gx, gy = 45, 400  # top-left corner of the ghost
    # Soft ground shadow under the ghost.
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((gx + 20, gy + ghost_h - 18, gx + ghost.width - 20,
                gy + ghost_h + 14), fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    bg = Image.alpha_composite(bg.convert("RGBA"), shadow).convert("RGB")
    bg.paste(ghost, (gx, gy), ghost)

    # Bottom caption.
    draw = ImageDraw.Draw(bg, "RGBA")
    bottom_lines = ["CALLED IN SICK.", "WORTH IT."]
    y = 812
    for line in bottom_lines:
        font = fit_font(draw, line, SIZE - 80, 98)
        outlined_text(draw, (SIZE // 2, y), line, font, WHITE, 9)
        y += font.size + 6

    # make.fun wordmark, small, in magenta at the very bottom.
    font = fit_font(draw, "make.fun", SIZE - 80, 42)
    draw.text((SIZE // 2, 1024), "make.fun", font=font, fill=MAGENTA,
              stroke_width=3, stroke_fill=WHITE, anchor="ma")

    bg.save(OUT, "PNG")
    print(f"wrote {OUT}: {bg.size[0]}x{bg.size[1]}")


if __name__ == "__main__":
    main()
