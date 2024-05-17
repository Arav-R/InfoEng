# MAKES A grid on an image and computes the amount of green in each. When closed, also displays a green mask to show what it sees.

import cv2
import numpy as np



# Load the image
image = cv2.imread(r'c:\Users\MakerSpaceAdmin\Downloads\Greenhouse Photos\PXL_20240404_141008371.jpg')  # Replace 'your_image.jpg' with the path to your image
if image is None:
    print("Image not found")
    exit()

# Define the dimensions of the ROI
roi_x = 700  # X coordinate of the top-left corner of the ROI
roi_y = 300  # Y coordinate of the top-left corner of the ROI
roi_width = 1600  # Width of the ROI
roi_height = 3100  # Height of the ROI

# Define the dimensions of the grid within the ROI
rows = 10
cols = 5

# Define the dimensions of each grid cell
cell_height = roi_height // rows
cell_width = roi_width // cols

# Create a resizable window
cv2.namedWindow('Grid with Green Boxes', cv2.WINDOW_NORMAL)

# Loop through each cell in the grid
for i in range(rows):
    for j in range(cols):
        # Define the coordinates of the current cell within the ROI
        x1 = roi_x + j * cell_width
        y1 = roi_y + i * cell_height
        x2 = roi_x + (j + 1) * cell_width
        y2 = roi_y + (i + 1) * cell_height
        
        # Extract the current cell from the image
        cell = image[y1:y2, x1:x2]
        
        # Convert cell to HSV color space
        cell_hsv = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)
        
        # Define lower and upper bounds for green color in HSV
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([90, 255, 255])
        
        # Create a mask of green areas within the cell
        mask = cv2.inRange(cell_hsv, lower_green, upper_green)
        
        # Calculate the number of green pixels in the mask
        green_pixels = np.count_nonzero(mask)
        
        # Calculate the total number of pixels in the cell
        total_pixels = cell_height * cell_width
        
        # Calculate the percentage of green pixels
        percentage_green = (green_pixels / total_pixels) * 100
        
        # Print the percentage of green in the cell
        print(f"Percentage of green in cell ({i+1},{j+1}): {percentage_green:.2f}%")
        
        # Draw a rectangle around the current cell for visualization
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Show the image with grid
cv2.imshow('Grid with Green Boxes', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

def mask_green(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for green color in HSV
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([90, 255, 255])

    # Create a mask of green areas within the image
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Apply the mask to the original image
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    return masked_image

# Load the image
image_path = r'c:\Users\MakerSpaceAdmin\Downloads\Greenhouse Photos\PXL_20240404_141008371.jpg'  # Replace 'your_image.jpg' with the path to your image
image = cv2.imread(image_path)
if image is None:
    print("Image not found")
else:
    # Apply the mask to detect green areas
    masked_green_image = mask_green(image)

    # Display the original image and the masked green areas
    cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Masked Green Areas', cv2.WINDOW_NORMAL)

    # cv2.imshow('Original Image', image)
    cv2.imshow('Masked Green Areas', masked_green_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

