import math
from PIL import Image, ImageDraw, ImageFont

def render_dag(filename="scratch/dag_10nodes_hard.png"):
    width, height = 2400, 1400
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # 10 Nodes layout across 5 distinct columns:
    # Col 0: S (x=200, y=700)
    # Col 1: A (x=600, y=450), B (x=600, y=950)
    # Col 2: C (x=1050, y=300), D (x=1050, y=700), E (x=1050, y=1100)
    # Col 3: F (x=1550, y=350), G (x=1550, y=750), H (x=1550, y=1150)
    # Col 4: T (x=2150, y=700)

    node_pos = {
        'S': (200, 700),
        'A': (620, 420),
        'B': (620, 980),
        'C': (1080, 260),
        'D': (1080, 700),
        'E': (1080, 1140),
        'F': (1580, 320),
        'G': (1580, 720),
        'H': (1580, 1120),
        'T': (2150, 700)
    }

    # 22 Directed edges with weights:
    edges = [
        ('S', 'A', 16, 0.45, (0, -18)),
        ('S', 'B', 19, 0.45, (0, 18)),
        ('S', 'C', 12, 0.35, (-15, -15)),
        ('S', 'D', 15, 0.40, (0, -15)),
        ('A', 'C', 11, 0.45, (-15, -10)),
        ('A', 'D', 24, 0.45, (12, 10)),
        ('A', 'F', 31, 0.32, (0, -18)), # long bypass
        ('B', 'D', 17, 0.45, (12, -10)),
        ('B', 'E', 28, 0.45, (-15, 12)),
        ('C', 'E', 14, 0.50, (20, 0)),   # vertical in col 2
        ('C', 'F', 23, 0.45, (0, -16)),
        ('D', 'F', 20, 0.40, (-10, -12)),
        ('D', 'G', 26, 0.45, (0, -16)),
        ('D', 'H', 22, 0.40, (-10, 12)),
        ('E', 'G', 18, 0.45, (10, -12)),
        ('E', 'H', 25, 0.45, (0, 16)),
        ('E', 'T', 34, 0.35, (10, 18)), # long bypass
        ('F', 'G', 13, 0.50, (22, 0)),   # vertical in col 3
        ('F', 'T', 27, 0.40, (15, -15)),
        ('G', 'H', 15, 0.50, (22, 0)),   # vertical in col 3
        ('G', 'T', 29, 0.45, (0, -16)),
        ('H', 'T', 21, 0.45, (10, 16))
    ]

    radius = 52
    node_border_width = 3
    arrow_color = "#1E293B" # slate 800
    arrow_width = 3

    # Load fonts
    try:
        font_node = ImageFont.truetype("arialbd.ttf", 36)
        font_badge = ImageFont.truetype("arialbd.ttf", 26)
    except:
        font_node = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # Draw edges first
    for u, v, w, t_pos, offset in edges:
        x1, y1 = node_pos[u]
        x2, y2 = node_pos[v]

        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        ux = dx / dist
        uy = dy / dist

        # Start and end outside node circles
        start_x = x1 + ux * radius
        start_y = y1 + uy * radius
        end_x = x2 - ux * radius
        end_y = y2 - uy * radius

        # Draw line
        draw.line([(start_x, start_y), (end_x, end_y)], fill=arrow_color, width=arrow_width)

        # Draw arrowhead
        arrow_len = 18
        arrow_angle = math.pi / 7
        angle = math.atan2(dy, dx)
        p1 = (end_x - arrow_len * math.cos(angle - arrow_angle), end_y - arrow_len * math.sin(angle - arrow_angle))
        p2 = (end_x - arrow_len * math.cos(angle + arrow_angle), end_y - arrow_len * math.sin(angle + arrow_angle))
        draw.polygon([(end_x, end_y), p1, p2], fill=arrow_color)

    # Draw badges
    badge_boxes = []
    for u, v, w, t_pos, (off_x, off_y) in edges:
        x1, y1 = node_pos[u]
        x2, y2 = node_pos[v]
        bx = x1 + (x2 - x1) * t_pos + off_x
        by = y1 + (y2 - y1) * t_pos + off_y

        text = str(w)
        bbox = draw.textbbox((0, 0), text, font=font_badge)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        pad_x = 10
        pad_y = 6
        rect = [bx - tw/2 - pad_x, by - th/2 - pad_y, bx + tw/2 + pad_x, by + th/2 + pad_y]
        badge_boxes.append((w, rect))

        # Draw badge background
        draw.rounded_rectangle(rect, radius=6, fill="#FFFFFF", outline="#64748B", width=2)
        # Draw badge text in dark red / crimson
        draw.text((bx - tw/2, by - th/2 - 2), text, fill="#B91C1C", font=font_badge)

    # Draw nodes
    for name, (x, y) in node_pos.items():
        # Circle fill
        circle_bbox = [x - radius, y - radius, x + radius, y + radius]
        draw.ellipse(circle_bbox, fill="#FFFBEB", outline="#000000", width=node_border_width)

        # Node letter
        bbox = draw.textbbox((0, 0), name, font=font_node)
        nw = bbox[2] - bbox[0]
        nh = bbox[3] - bbox[1]
        draw.text((x - nw/2, y - nh/2 - 3), name, fill="#0F172A", font=font_node)

    img.save(filename, "PNG")
    print(f"Saved DAG image to {filename}")

if __name__ == "__main__":
    render_dag()
