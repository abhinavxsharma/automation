import math
from PIL import Image, ImageDraw, ImageFont

def render_dag(filename="handshake/scratch/dag_10nodes_hard.png"):
    width, height = 2400, 1400
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # 10 Nodes layout across 5 distinct columns:
    # Col 0: S (x=220, y=700)
    # Col 1: A (x=680, y=380), B (x=680, y=1020)
    # Col 2: C (x=1150, y=260), D (x=1150, y=700), E (x=1150, y=1140)
    # Col 3: F (x=1620, y=320), G (x=1620, y=700), H (x=1620, y=1080)
    # Col 4: T (x=2150, y=700)

    node_pos = {
        'S': (220, 700),
        'A': (680, 380),
        'B': (680, 1020),
        'C': (1150, 260),
        'D': (1150, 700),
        'E': (1150, 1140),
        'F': (1620, 320),
        'G': (1620, 700),
        'H': (1620, 1080),
        'T': (2150, 700)
    }

    # 20 Directed edges with tuned badge positions (t_pos along line) and offsets (perpendicular or shift)
    edges = [
        # (u, v, weight, t_pos, (off_x, off_y))
        ('S', 'A', 16, 0.45, (0, -22)),
        ('S', 'B', 19, 0.45, (0, 22)),
        ('S', 'D', 15, 0.32, (0, -20)),
        ('A', 'C', 11, 0.45, (-15, -18)),
        ('A', 'D', 24, 0.42, (18, 12)),
        ('A', 'F', 31, 0.26, (0, -22)),
        ('B', 'D', 17, 0.42, (18, -12)),
        ('B', 'E', 28, 0.45, (-15, 18)),
        ('C', 'F', 23, 0.45, (0, -22)),
        ('D', 'F', 20, 0.42, (-16, -16)),
        ('D', 'G', 26, 0.45, (0, -20)),
        ('D', 'H', 22, 0.42, (-16, 16)),
        ('E', 'G', 18, 0.45, (16, -16)),
        ('E', 'H', 25, 0.45, (0, 22)),
        ('E', 'T', 34, 0.30, (18, 22)),
        ('F', 'G', 13, 0.50, (26, 0)),
        ('F', 'T', 27, 0.45, (16, -18)),
        ('G', 'H', 15, 0.50, (26, 0)),
        ('G', 'T', 29, 0.45, (0, -20)),
        ('H', 'T', 21, 0.45, (16, 18))
    ]

    radius = 50
    node_border_width = 3
    arrow_color = "#1E293B"  # slate 800
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
