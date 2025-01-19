import os
import time
import subprocess
from pathlib import Path

# Configuration
WATCH_FOLDER = "./Images"  # Replace with your folder path
UPLOADED_FOLDER = os.path.join(WATCH_FOLDER, "uploaded")
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Create 'uploaded' folder if it doesn't exist
os.makedirs(UPLOADED_FOLDER, exist_ok=True)

def upload_image(image_path):
    """Uploads an image using the curl command."""
    try:
        result = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{image_path}", UPLOAD_URL],
            capture_output=True,
            text=True
        )
        print(f"Uploaded {image_path}: {result.stdout}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error uploading {image_path}: {e}")
        return False

def monitor_and_upload():
    """Monitors the folder and uploads images."""
    print(f"Monitoring folder: {WATCH_FOLDER}")
    while True:
        for image_file in os.listdir(WATCH_FOLDER):
            image_path = os.path.join(WATCH_FOLDER, image_file)
            # Skip if not a file or already uploaded
            if not os.path.isfile(image_path) or image_file in os.listdir(UPLOADED_FOLDER):
                continue
            # Upload the image
            print(f"Found new image: {image_file}")
            time.sleep(30)  # Wait 30 seconds before uploading
            if upload_image(image_path):
                # Move the image to the uploaded folder
                os.rename(image_path, os.path.join(UPLOADED_FOLDER, image_file))
                print(f"Moved {image_file} to 'uploaded' folder.")
        time.sleep(5)  # Wait a bit before checking again

if __name__ == "__main__":
    monitor_and_upload()
