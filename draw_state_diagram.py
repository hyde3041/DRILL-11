from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 1400, 760
ORANGE = "#e65c2f"
BLUE = "#109ac2"
BLACK = "#202020"
FONT = "C:/Windows/Fonts/malgun.ttf"
BOLD = "C:/Windows/Fonts/malgunbd.ttf"

STATES = {
    "idle": (230, 380, ["IDLE 상태"]),
    "run_left": (650, 610, ["왼쪽 Run", "상태"]),
    "run_right": (650, 150, ["오른쪽 Run", "상태"]),
    "auto_run": (1050, 380, ["AutoRun 상태"]),
    "sleep": (230, 650, ["Sleep 상태"]),
}

EDGES = [
    ("idle", "run_left", "왼쪽 방향키 누름"),
    ("idle", "run_right", "오른쪽 방향키 누름"),
    ("run_left", "idle", "왼쪽 방향키 뗌"),
    ("run_right", "idle", "오른쪽 방향키 뗌"),
    ("idle", "auto_run", "a 키 누름"),
    ("auto_run", "run_left", "왼쪽 방향키 누름"),
    ("auto_run", "run_right", "오른쪽 방향키 누름"),
    ("auto_run", "idle", "5초 경과"),
    ("idle", "sleep", "5초 무입력"),
    ("sleep", "idle", "키 입력"),
]


POSITION = {name: (x, y) for name, (x, y, _) in STATES.items()}


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def create_diagram():
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    draw.text((40, 25), "Boy 상태 다이어그램 — DRILL 11", font=font(38, True), fill=BLACK)
    draw.line((40, 85, 1360, 85), fill=BLUE, width=4)

    radius = 95
    for name, (x, y, lines) in STATES.items():
        if name == "idle":
            draw.ellipse((x - radius - 7, y - radius - 7, x + radius + 7, y + radius + 7), fill="white", outline=BLACK, width=3)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="white", outline=BLACK, width=3)
        block = "\n".join(lines)
        draw.multiline_text((x, y), block, font=font(26, True), fill=BLACK, anchor="mm", align="center")

    def arrow(points, label, label_position):
        draw.line(points, fill=ORANGE, width=5, joint="curve")
        x1, y1 = points[-2]
        x2, y2 = points[-1]
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        size = 18
        points_arrow = [
            (x2, y2),
            (x2 - size * math.cos(angle - 0.45), y2 - size * math.sin(angle - 0.45)),
            (x2 - size * math.cos(angle + 0.45), y2 - size * math.sin(angle + 0.45)),
        ]
        draw.polygon(points_arrow, fill=ORANGE)
        lx, ly = label_position
        bbox = draw.textbbox((lx, ly), label, font=font(20), anchor="mm")
        pad = 5
        draw.rectangle((bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad), fill="white")
        draw.text((lx, ly), label, font=font(20), fill=BLACK, anchor="mm")

    arrow([(330, 380), (555, 380)], "좌우 방향키", (440, 350))
    arrow([(555, 610), (330, 450)], "방향키 뗌", (420, 565))
    arrow([(555, 150), (330, 310)], "방향키 뗌", (420, 205))
    arrow([(330, 380), (555, 610)], "왼쪽 방향키 누름", (430, 500))
    arrow([(330, 380), (555, 150)], "오른쪽 방향키 누름", (430, 250))
    arrow([(325, 380), (955, 380)], "a 키 누름", (680, 345))
    arrow([(1050, 475), (745, 610)], "왼쪽 방향키 누름", (880, 550))
    arrow([(1050, 285), (745, 150)], "오른쪽 방향키 누름", (880, 220))
    arrow([(1145, 380), (325, 380)], "5초 경과", (1040, 445))
    arrow([(230, 475), (230, 555)], "5초 무입력", (320, 520))
    arrow([(230, 555), (230, 475)], "키 입력", (145, 520))

    caption = "Idle 5초 무입력 → Sleep / 방향키 입력 → Run 또는 Idle / AutoRun 5초 → Idle"
    draw.text((40, 710), caption, font=font(22, True), fill=BLACK)

    png_path = OUT / "boy-state-diagram.png"
    svg_path = OUT / "boy-state-diagram.svg"
    image.save(png_path)

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="760" viewBox="0 0 1400 760">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="40" y="65" font-family="Malgun Gothic, sans-serif" font-size="38" font-weight="700" fill="#202020">Boy 상태 다이어그램 — DRILL 11</text>',
        '<line x1="40" y1="85" x2="1360" y2="85" stroke="#109ac2" stroke-width="4"/>',
    ]
    for name, (x, y, lines) in STATES.items():
        svg.append(f'<circle cx="{x}" cy="{y}" r="95" fill="white" stroke="#202020" stroke-width="3"/>')
        for index, line in enumerate(lines):
            offset = (index - (len(lines) - 1) / 2) * 34
            svg.append(f'<text x="{x}" y="{y + offset}" text-anchor="middle" dominant-baseline="central" font-family="Malgun Gothic, sans-serif" font-size="26" font-weight="700" fill="#202020">{line}</text>')
    svg.append('</svg>')
    svg_path.write_text("\n".join(svg), encoding="utf-8")
    print(png_path)
    print(svg_path)


if __name__ == "__main__":
    create_diagram()
