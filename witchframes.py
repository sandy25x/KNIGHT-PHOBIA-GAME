from PIL import Image
import os

def extract_frames(gif_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    with Image.open(gif_path) as img:
        for frame in range(img.n_frames):
            img.seek(frame)
            img.save(os.path.join(output_folder, f"witch{frame}.png"))

# Provide the correct path to the GIF file
gif_path = r'C:\Users\yourpc\Downloads\knight phobia\witch.gif'
output_folder = r'C:\Users\yourpc\Downloads\knight phobia\witch_frames'

# Extract frames from witch.gif and save them to the "witch_frames" folder
extract_frames(gif_path, output_folder)
