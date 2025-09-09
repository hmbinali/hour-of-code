"""
 Challenge: File Sorter by Type

Goal:
- Scan the current folder (or a user-provided folder)
- Move files into subfolders based on their type:
    - .pdf → PDFs/
    - .jpg, .jpeg, .png → Images/
    - .txt → TextFiles/
    - Others → Others/
- Create folders if they don't exist
- Ignore folders during the move

Teaches: File system operations, automation, file handling with `os` and `shutil`
"""

import os
import shutil

EXTENTION_MAP = {
    "00_Files_PDFs": [".pdf"],
    "00_Files_Images": [".png", ".jpeg", ".jpg"],
    "00_Files_TextFiles": [".txt"],
}

# --- Files to ignore during sorting ---
# We get the script's own name dynamically to avoid moving it
FILES_TO_SKIP = {".gitignore", "requirements.txt", os.path.basename(__file__)}


def get_destination_folder(filename):
    ext = os.path.splitext(filename)[1].lower()

    for folder, extentions in EXTENTION_MAP.items():
        if ext in extentions:
            return folder

    return "00_Files_Others"


def sort_files(folder_path):
    for file in os.listdir(folder_path):
        # --- ADDED THIS CHECK ---
        # Skip any file in our ignore list or any 'readme' file (e.g., readme.md)
        if file in FILES_TO_SKIP or os.path.splitext(file)[0].lower() == "readme":
            continue  # Skips to the next file in the loop

        full_path = os.path.join(folder_path, file)

        if os.path.isfile(full_path):
            dest_folder = get_destination_folder(file)
            dest_path = os.path.join(folder_path, dest_folder)

            os.makedirs(dest_path, exist_ok=True)

            # Move the file
            shutil.move(full_path, os.path.join(dest_path, file))
            print(f"Moved : {file} -> {dest_folder}/")


if __name__ == "__main__":
    folder = input(
        "Enter the folder path or leave blank to use the current directory: "
    ).strip()
    folder = folder or os.getcwd()

    if not os.path.isdir(folder):
        print("Invalid directory")
    else:
        sort_files(folder)
        print("✅ Sorting completed")
