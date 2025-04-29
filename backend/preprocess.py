import os
import numpy as np
from PIL import Image
import cv2  # OpenCV for denoising
from skimage import exposure  # For histogram equalization
import torchvision.transforms as transforms
# Directory paths
input_directories = ['./dataset/train', './dataset/test', './dataset/valid']  # Paths to train, test, and valid folders
output_directory = '../preprocessed'  # Path where processed images will be saved
# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
# Function to apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
def apply_clahe(image):
    image_np = np.array(image.convert('L'))  # Convert to grayscale
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(image_np)
    return Image.fromarray(clahe_image).convert('RGB')
# Function to apply Gaussian Blur (for noise reduction)
def apply_gaussian_blur(image):
    image_np = np.array(image)
    blurred_image = cv2.GaussianBlur(image_np, (5, 5), 0)  # Kernel size can be adjusted
    return Image.fromarray(blurred_image)
# Function to normalize the image (scale pixel values between 0 and 1)
def normalize_image(image):
    image_np = np.array(image) / 255.0  # Normalize the image to range [0, 1]
    return Image.fromarray((image_np * 255).astype(np.uint8))
# Transformation to convert image to tensor (if needed)
transform = transforms.Compose([
    transforms.Resize((256, 256)),  # Resize to standard input size for the model
    transforms.Grayscale(num_output_channels=3),  # Convert to RGB (3 channels)
    transforms.ToTensor(),  # Convert image to tensor
    transforms.Normalize(mean=[0.5], std=[0.5])  # Normalize if needed (adjust based on model)
])
def preprocess_image(image_path):
    # Open the image
    image = Image.open(image_path).convert('RGB')
    # Apply CLAHE for contrast enhancement
    image = apply_clahe(image)
    # Apply Gaussian Blur for denoising
    image = apply_gaussian_blur(image)
    # Normalize the image
    image = normalize_image(image)
    return image
# Process all images in the dataset (train, test, valid)
for input_directory in input_directories:
    for category_folder in os.listdir(input_directory):
        category_folder_path = os.path.join(input_directory, category_folder)
        # Check if it's a directory (category folder like adenocarcinoma, large.cell.carcinoma)
        if os.path.isdir(category_folder_path):
            # Create corresponding category folder in the output directory
            relative_category_path = os.path.relpath(category_folder_path, 'dataset')
            output_category_folder = os.path.join(output_directory, relative_category_path)
            if not os.path.exists(output_category_folder):
                os.makedirs(output_category_folder)
            # Process each image in the category folder
            for image_filename in os.listdir(category_folder_path):
                image_path = os.path.join(category_folder_path, image_filename)
                # Only process image files (adjust extensions as needed)
                if image_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print(f"Processing {image_filename} in category {category_folder} from {input_directory}...")
                    # Apply preprocessing
                    preprocessed_image = preprocess_image(image_path)
                    # Save the preprocessed image in the corresponding category folder
                    output_image_path = os.path.join(output_category_folder, image_filename)
                    preprocessed_image.save(output_image_path)
print("Preprocessing complete!")
