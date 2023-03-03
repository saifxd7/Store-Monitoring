import os
import time
import subprocess

WATCH_DIR = "/app/incoming_files"


def watch_directory():
    """
    Monitors the WATCH_DIR for new files, and executes the import command if a file named "store.csv" is detected.
    """
    print("Starting file watcher...")
    while True:
        time.sleep(1)
        for filename in os.listdir(WATCH_DIR):
            if filename == "store.csv":
                filepath = os.path.join(WATCH_DIR, filename)
                print(f"New file detected: {filepath}")

                # Process the file using subprocess
                subprocess.run(
                    ["python", "manage.py", "import_data", filepath, "Store"])

                # Delete the file from the incoming folder
                os.remove(filepath)

            elif filename == "store_status.csv":
                filepath = os.path.join(WATCH_DIR, filename)
                print(f"New file detected: {filepath}")

                # Process the file using subprocess
                subprocess.run(
                    ["python", "manage.py", "import_data", filepath, "StoreStatus"])

                # Delete the file from the incoming folder
                # os.remove(filepath)

            elif filename == "store_hours.csv":
                filepath = os.path.join(WATCH_DIR, filename)
                print(f"New file detected: {filepath}")

                # Process the file using subprocess
                subprocess.run(
                    ["python", "manage.py", "import_data", filepath, "StoreHours"])

                # Delete the file from the incoming folder
                # os.remove(filepath)


if __name__ == "__main__":
    watch_directory()
