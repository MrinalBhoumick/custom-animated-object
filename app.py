import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import time
from io import BytesIO
import random

# Function to generate a simple binary grid
def generate_binary_grid(rows, cols):
    return np.random.choice([0, 1], size=(rows, cols))

# Function to convert binary grid to an image
def binary_grid_to_image(grid):
    # Convert binary grid to a black and white image
    img = Image.new('RGB', (grid.shape[1] * 10, grid.shape[0] * 10), color="white")
    draw = ImageDraw.Draw(img)

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            color = "black" if grid[y, x] == 1 else "white"
            draw.rectangle([x * 10, y * 10, (x + 1) * 10, (y + 1) * 10], fill=color)

    return img

# Function to animate binary grids
def animate_binary_grids(rows, cols, num_frames, speed):
    frames = []
    for _ in range(num_frames):
        grid = generate_binary_grid(rows, cols)
        img = binary_grid_to_image(grid)
        frames.append(img)
        time.sleep(speed)

    return frames

# Streamlit UI
st.title("Binary Grid Animation")

# Slider for animation speed control
speed = st.slider("Animation Speed (seconds per frame)", 0.1, 1.0, 0.5)

# User input for object name (for visualization purposes)
object_name = st.text_input("Enter Object Name", "Aeroplane")

# Button to generate animation
if st.button("Generate Animation"):
    # Define the grid size and number of frames
    rows, cols = 10, 10  # Small grid for demonstration (can be scaled)
    num_frames = 30  # Number of frames in the animation

    # Generate and animate the binary grid
    frames = animate_binary_grids(rows, cols, num_frames, speed)

    # Save animation to GIF in memory
    tmpfile = BytesIO()
    frames[0].save(tmpfile, save_all=True, append_images=frames[1:], duration=100, loop=0, format="GIF")
    tmpfile.seek(0)

    # Display the animated GIF
    st.image(tmpfile, caption=f"Animated {object_name} Visualization", use_column_width=True)

    # Optionally, save the GIF
    tmpfile_name = "binary_animation.gif"
    with open(tmpfile_name, "wb") as f:
        f.write(tmpfile.getbuffer())

    # Allow the user to download the GIF
    st.download_button("Download Animation", tmpfile, file_name=tmpfile_name)
