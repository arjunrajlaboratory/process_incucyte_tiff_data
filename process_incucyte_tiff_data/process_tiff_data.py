import os
import sys
import argparse
import numpy as np
import tifffile as tf

def process_tiff_data(input_directory, output_directory, threshold=65000):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Loop through all folders in the input directory
    for folder in os.listdir(input_directory):
        folder_path = os.path.join(input_directory, folder)
        
        # Check if it's a directory
        if os.path.isdir(folder_path):
            # Remove underscores from the folder name
            folder_name = folder.replace('_', '')

            # Loop through all TIFF files in the folder
            for filename in os.listdir(folder_path):
                if filename.endswith('.tif') or filename.endswith('.tiff'):
                    file_path = os.path.join(folder_path, filename)
                    
                    # Read the image
                    image = tf.imread(file_path)
                    
                    # Check if the image is 16-bit
                    if image.dtype == np.uint16:
                        print(f"Processing 16-bit image: {file_path}")
                        
                        # Replace values above threshold with 0
                        image[image > threshold] = 0
                    elif image.dtype == np.uint8:
                        print(f"Converting 8-bit image to 16-bit: {file_path}")
                        
                        # Convert 8-bit to 16-bit
                        image = np.uint16(image) * 256
                    
                    # Save the processed image to the output directory
                    new_filename = f"{folder_name}_{filename}"
                    destination_path = os.path.join(output_directory, new_filename)
                    tf.imwrite(destination_path, image)
                    print(f"Saved processed image to: {destination_path}")

    print("Processing complete!")

def main():
    parser = argparse.ArgumentParser(description='Process Incucyte TIFF data.')
    parser.add_argument('-i', '--input-directory', default=os.getcwd(), help='Input directory (default: current working directory)')
    parser.add_argument('-o', '--output-directory', default='./fixed_files', help='Output directory (default: ./fixed_files)')
    parser.add_argument('-t', '--threshold', type=int, default=65000, help='Threshold value (default: 65000)')
    
    args = parser.parse_args()
    
    process_tiff_data(args.input_directory, args.output_directory, args.threshold)

if __name__ == "__main__":
    main()
