Of course! Below is a revised introduction for the README with the representation of the input file structure and the expected output:


# process_incucyte_tiff_data

This is a Python package for processing TIFF images generated by the Incucyte imaging system. The script processes TIFF files nested in folders within the input directory and saves the processed images with modified filenames in the output directory.

## Input Directory Structure Example:

```
OriginalData/
│
├── phase/
│   ├── VID1630_C4_1_01d23h34m.tif
│   ├── VID1630_C4_1_00d23h56m.tif
│   ├── VID1630_C4_1_00d00h00m.tif
│   ├── ...
│
├── red/
│   ├── VID1630_C4_1_01d23h34m.tif
│   ├── VID1630_C4_1_00d23h56m.tif
│   ├── VID1630_C4_1_00d00h00m.tif
│   ├── ...
│
└── gfp/
    ├── VID1630_C4_1_01d23h34m.tif
    ├── VID1630_C4_1_00d23h56m.tif
    ├── VID1630_C4_1_00d00h00m.tif
    └── ...
```

## Expected Output Directory Structure:

```
fixed_files/
│
├── phase_VID1630_C4_1_01d23h34m.tif
├── phase_VID1630_C4_1_00d23h56m.tif
├── phase_VID1630_C4_1_00d00h00m.tif
├── ...
├── red_VID1630_C4_1_01d23h34m.tif
├── red_VID1630_C4_1_00d23h56m.tif
├── red_VID1630_C4_1_00d00h00m.tif
├── ...
├── gfp_VID1630_C4_1_01d23h34m.tif
├── gfp_VID1630_C4_1_00d23h56m.tif
└── gfp_VID1630_C4_1_00d00h00m.tif
...
```

For each TIFF file in the input directory, the script takes the folder name, removes any underscores, appends it to the filename with an underscore, and then saves it to the output directory.


## Installation
Navigate to the repository directory and run the following command:
```bash
pip install process_incucyte_tiff_data
```

## Usage
After installation, you can use the command-line interface to process your TIFF images. Here are the available options:

```
usage: process-incucyte-tiff-data [-h] [-i INPUT_DIRECTORY] [-o OUTPUT_DIRECTORY] [-t THRESHOLD]

Process Incucyte TIFF data.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIRECTORY, --input-directory INPUT_DIRECTORY
                        Input directory (default: current working directory)
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Output directory (default: ./fixed_files)
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold value (default: 65000)
```
The `input-directory` parameter is used to specify the directory where your folders with TIFF files are located. The `output-directory` parameter is used to specify the directory where you want to save the processed TIFF files. The `threshold` parameter is used to specify the value above which pixel values in the 16-bit images will be set to 0.

For example, to process TIFF files in the folder `/path/to/tiff/files`, and save the processed files to `/path/to/fixed/files` with a threshold value of 40000, you would run:

```bash
process-incucyte-tiff-data -i /path/to/tiff/files -o /path/to/fixed/files -t 40000
```
If you don't specify any parameters, the script will use the current working directory as the input directory, `./fixed_files` as the output directory, and 65000 as the threshold value.