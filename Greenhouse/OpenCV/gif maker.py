import os


from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True


# Directory containing your images
image_folder = r'c:\Users\MakerSpaceAdmin\Documents\GitHub\InfoEng\Greenhouse\Photos'

# Output GIF file path
gif_path = r'c:\Users\MakerSpaceAdmin\Documents\GitHub\InfoEng\Greenhouse\output.gif'

# List of image file names
jpg_images = [img for img in os.listdir(image_folder) if img.lower().endswith(".jpg")]
jpeg_images = [img for img in os.listdir(image_folder) if img.lower().endswith(".jpeg")]

# Combine both lists of image names
images = sorted(jpg_images + jpeg_images)

# Create a list to store the frames
frames = []

# Loop through each image and append it to the frames list
for image_name in images:
    image_path = os.path.join(image_folder, image_name)
    try:
        img = Image.open(image_path)
        if img.size != (0, 0):  # Check if image is not empty
            frames.append(img)
            print(f"Added image: {image_name}")
        else:
            print(f"Skipped empty image: {image_name}")
    except Exception as e:
        print(f"Error processing image {image_name}: {e}")

# Save frames as a GIF if there are valid frames
if frames:
    try:
        frames[0].save(gif_path, format='GIF', append_images=frames[1:], save_all=True, duration=1, loop=0)
        print("GIF created successfully!")
    except Exception as e:
        print(f"Error saving GIF: {e}")
else:
    print("No valid images found in the specified directory.")
