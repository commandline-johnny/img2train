import os
import cv2
import sys
from PIL import Image, ImageOps


def detect_face(image_path):
    # Load the Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Read the image using OpenCV
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    return faces


def crop_face_center(image, faces, target_size=(1024, 1024)):
    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        left = max(0, face_center_x - target_size[0] // 2)
        top = max(0, face_center_y - target_size[1] // 2)
        right = min(image.width, face_center_x + target_size[0] // 2)
        bottom = min(image.height, face_center_y + target_size[1] // 2)

        cropped_image = image.crop((left, top, right, bottom))
        cropped_image = ImageOps.pad(cropped_image, target_size, color=(0, 0, 0))
        return cropped_image
    else:
        return None  # Return None if no face is detected


def augment_and_save(image, filename, output_dir):
    image.save(os.path.join(output_dir, filename))

    flipped_img = image.transpose(Image.FLIP_LEFT_RIGHT)
    flipped_img.save(os.path.join(output_dir, f"flipped_{filename}"))

    rotated_90_img = image.rotate(90, expand=True)
    rotated_90_img.save(os.path.join(output_dir, f"rotated_90_{filename}"))

    rotated_270_img = image.rotate(270, expand=True)
    rotated_270_img.save(os.path.join(output_dir, f"rotated_270_{filename}"))

    print(f"Augmented versions saved for: {filename}")


def resize_images(input_dir, output_dir, size=(1024, 1024)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            image_path = os.path.join(input_dir, filename)
            faces = detect_face(image_path)
            if len(faces) > 0:
                try:
                    img = Image.open(image_path)
                    img_cropped = crop_face_center(img, faces, size)
                    if img_cropped:
                        augment_and_save(img_cropped, filename, output_dir)
                except Exception as e:
                    print(f"Failed to process {filename}: {e}")
            else:
                print(f"No face detected in: {filename}, skipping.")
        else:
            print(f"Skipped non-image file: {filename}")


def get_input_directories():
    # Check if directories were provided as arguments
    if len(sys.argv) > 1:
        if "--help" in sys.argv:
            print_help()
            sys.exit(0)
        input_dirs = sys.argv[1:]  # Take all arguments after the script name as directories
        for directory in input_dirs:
            if not os.path.isdir(directory):
                print(f"The provided directory does not exist: {directory}")
                sys.exit(1)
    else:
        # If no arguments provided, prompt the user for directories
        input_dirs = input("Please enter the paths to your photo directories (comma separated): ").split(',')
        input_dirs = [d.strip() for d in input_dirs]
        for directory in input_dirs:
            if not os.path.isdir(directory):
                print(f"The provided directory does not exist: {directory}")
                sys.exit(1)
    return input_dirs


def print_help():
    print("""
    Usage: python script_name.py [photo_directory1] [photo_directory2] ...

    This script processes images in the given directories, detects faces, and resizes the images to 1024x1024.
    If no arguments are passed, it will prompt you for the photo directories.

    Options:
    --help      Show this help message and exit.

    Example:
    python script_name.py <path_to_photo_directory> <path_to_another_photo_directory> ...
    """)


if __name__ == "__main__":
    # Get input directories from arguments or prompt the user
    input_dirs = get_input_directories()

    for input_dir in input_dirs:
        output_dir = os.path.join(input_dir, "training_photos")
        resize_images(input_dir, output_dir)
