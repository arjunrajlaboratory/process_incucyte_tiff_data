import os
import sys
import argparse
import numpy as np
import tifffile as tf
from pystackreg import StackReg

def crop_center(img, fraction=0.1):
    """Crop the center of the image based on the given fraction."""
    if not 0 < fraction <= 1:
        raise ValueError("Fraction must be between 0 and 1 (exclusive of 0 and inclusive of 1).")
    center_x, center_y = img.shape[1] // 2, img.shape[0] // 2
    width_x = int(img.shape[1] * fraction)
    width_y = int(img.shape[0] * fraction)
    crop_x1 = center_x - width_x // 2
    crop_x2 = center_x + width_x // 2
    crop_y1 = center_y - width_y // 2
    crop_y2 = center_y + width_y // 2
    return img[crop_y1:crop_y2, crop_x1:crop_x2]

def register_images(input_directory, registration_directory="phase"):
    """Calculate transformation matrices using images from the specified directory."""
    directory_path = os.path.join(input_directory, registration_directory)
    files = [f for f in os.listdir(directory_path) if f.endswith(('.tif', '.tiff'))]
    files.sort()

    sr = StackReg(StackReg.TRANSLATION)
    transformation_matrices = []
    previous_cropped_image = None

    for idx, filename in enumerate(files):
        img_path = os.path.join(directory_path, filename)
        img = tf.imread(img_path)
        print(f"Loaded {filename} with data type {img.dtype}")  # Print the data type of the image
        cropped_img = crop_center(img, 0.3)

        if previous_cropped_image is not None:
            print(f"Calculating transformation for {filename} ({idx + 1}/{len(files)})")
            matrix = sr.register(previous_cropped_image, cropped_img)
            transformation_matrices.append(matrix)
        else:
            transformation_matrices.append(np.eye(3))  # Identity matrix for the first image
            print(f"Setting identity transformation for the first image {filename} ({idx + 1}/{len(files)})")

        previous_cropped_image = cropped_img
    
    return files, transformation_matrices

def process_tiff_data(input_directory, output_directory, threshold=65000, register=False, registration_directory="phase"):
    """Process TIFF data with optional registration."""
    if register:
        files, matrices = register_images(input_directory, registration_directory)
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for folder in os.listdir(input_directory):
        folder_path = os.path.join(input_directory, folder)
        if os.path.isdir(folder_path):
            folder_name = folder.replace('_', '')
            for filename in os.listdir(folder_path):
                if filename.endswith(('.tif', '.tiff')):
                    file_path = os.path.join(folder_path, filename)
                    image = tf.imread(file_path)
                    
                    if register and filename in files:
                        print(f"Applying registration transformation to {filename}")
                        idx = files.index(filename)
                        # Check if the image is uint8 and convert to uint16
                        if image.dtype == np.uint8:
                            image = np.uint16(image) * 256  # Scale appropriately to preserve the image contrast
                        image = StackReg(StackReg.TRANSLATION).transform(image, tmat=matrices[idx])
                        # Normalize to the original range and cast to uint16
                        image = np.clip(image, 0, 65535).astype(np.uint16)

                    if image.dtype == np.uint16 and np.max(image) > threshold:
                        image[image > threshold] = 0
                    elif image.dtype == np.uint8:
                        image = np.uint16(image) * 256

                    new_filename = f"{folder_name}_{filename}"
                    destination_path = os.path.join(output_directory, new_filename)
                    tf.imwrite(destination_path, image, dtype=image.dtype)
                    print(f"Saved processed image to: {destination_path}")

    print("Processing complete!")

def main():
    parser = argparse.ArgumentParser(description='Process and register TIFF data.')
    parser.add_argument('-i', '--input-directory', default=os.getcwd(), help='Input directory (default: current working directory)')
    parser.add_argument('-o', '--output-directory', default='./fixed_files', help='Output directory (default: ./fixed_files)')
    parser.add_argument('-t', '--threshold', type=int, default=65000, help='Threshold value (default: 65000)')
    parser.add_argument('-r', '--register', action='store_true', help='Enable image registration')
    parser.add_argument('-rd', '--registration-directory', default='phase', help='Directory to use for registration (default: "phase")')
    
    args = parser.parse_args()
    
    process_tiff_data(args.input_directory, args.output_directory, args.threshold, args.register, args.registration_directory)

if __name__ == "__main__":
    main()
