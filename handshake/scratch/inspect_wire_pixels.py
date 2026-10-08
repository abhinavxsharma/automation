import numpy as np
from PIL import Image, ImageDraw

# Load image
im = Image.open("handshake/scratch/new_circuit_image.png").convert("RGB")
w, h = im.size
print(f"Loaded image {w}x{h}")

# Let's inspect the vertical line at x=163 between y=455 and y=745
# We can erase it by painting it white!
# Let's see what color the background is:
bg_color = (255, 255, 255)
# Check pixels around (163, 600)
arr = np.array(im)
print("Background sample at (100, 100):", arr[100, 100])
print("Wire sample at (164, 600):", arr[600, 164])
