"""
output/thumbnail.png を 1200×1200px の正方形にリサイズする。
元画像をキャンバス中央に配置し、余白は元画像の四隅の平均色で埋める。
"""

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "output" / "thumbnail.png"
DST = ROOT / "output" / "thumbnail_square.png"
SIZE = 1200


def dominant_edge_color(img: Image.Image) -> tuple[int, int, int]:
    """画像四隅 10px 領域の平均色を背景色として返す"""
    w, h = img.size
    sample = 10
    corners = [
        img.crop((0, 0, sample, sample)),
        img.crop((w - sample, 0, w, sample)),
        img.crop((0, h - sample, sample, h)),
        img.crop((w - sample, h - sample, w, h)),
    ]
    pixels: list[tuple[int, int, int]] = []
    for c in corners:
        rgb = c.convert("RGB")
        pixels.extend(list(rgb.get_flattened_data() if hasattr(rgb, "get_flattened_data") else rgb.getdata()))
    n = len(pixels)
    r = sum(p[0] for p in pixels) // n
    g = sum(p[1] for p in pixels) // n
    b = sum(p[2] for p in pixels) // n
    return (r, g, b)


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(f"元画像が見つかりません: {SRC}")

    src_img = Image.open(SRC).convert("RGB")
    orig_w, orig_h = src_img.size
    print(f"元画像サイズ: {orig_w}×{orig_h}px")

    bg_color = dominant_edge_color(src_img)
    print(f"背景色 (RGB): {bg_color}")

    canvas = Image.new("RGB", (SIZE, SIZE), bg_color)

    # アスペクト比を保ったまま SIZE に収まるようスケーリング
    scale = min(SIZE / orig_w, SIZE / orig_h)
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    resized = src_img.resize((new_w, new_h), Image.LANCZOS)

    paste_x = (SIZE - new_w) // 2
    paste_y = (SIZE - new_h) // 2
    canvas.paste(resized, (paste_x, paste_y))

    DST.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(DST, "PNG")
    print(f"保存完了: {DST}  ({SIZE}×{SIZE}px)")


if __name__ == "__main__":
    main()
