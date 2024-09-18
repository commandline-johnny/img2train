
# img2train - Automates cropping and reszing photos of people for use in AI model training

This script processes images in one or more directories, detects faces, and resizes the images to 1024x1024. It also generates augmented versions of the images, including flipped and rotated variations. The script is designed to handle multiple directories and works seamlessly with Windows paths.

## Features:
- Detects faces in images using OpenCV.
- Crops and centers the image based on the detected face.
- Resizes the images to 1024x1024 while preserving aspect ratio.
- Generates augmented versions (flipped and rotated) of the processed images.
- Handles multiple directories and Windows paths.
- Offers a user prompt for directory input or accepts directories as command-line arguments.

## Known Issues:
- It thinks vaginas are faces. Ordinarily this is a problem but not for my use case. This will be fixed at a later date, I'm sure.

## Usage

### Command-Line Arguments

You can pass multiple directories to the script as arguments. For example:

```bash
python script_name.py "C:\path_to_photos1" "D:\another_path_to_photos2"
```

### User Prompt

If no arguments are passed, the script will prompt you to enter a comma-separated list of directories:

```bash
python script_name.py
```

Example input when prompted:

```
C:\path\to\photos1, D:\another_path\to\photos2
```

### Help Option

To see usage instructions, use the `--help` flag:

```bash
python script_name.py --help
```

## Requirements

Before running the script, ensure you have the following Python libraries installed:

- `opencv-python`
- `Pillow`

You can install the required libraries with:

```bash
pip install opencv-python Pillow
```

## Example Output

For each image in the input directories:
- The image is cropped and resized to 1024x1024.
- Augmented images are generated, including:
  - A horizontally flipped version.
  - A 90-degree rotated version.
  - A 270-degree rotated version.
- All processed images are saved in the `training_photos` folder within each input directory.

## Send a Tip

If you found this script useful and would like to support its continued development, feel free to send a tip! 💖

**[Click here to send a tip](https://buymeacoffee.com/commandline_johnny)**
![](./bmc_qr.png)
Your support is greatly appreciated!

## License

This project is open-source and available under the MIT License.
