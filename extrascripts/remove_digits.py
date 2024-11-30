import os
import shutil
import re

def move_vpk_files_and_cleanup(directory):
    """
    Moves all .vpk files to the specified directory and removes all other files and folders.
    :param directory: Path to the root directory.
    """
    # Get path to Deadlock Skins folder
    root_dir = directory
    # Iterate through all folders and files inside root_dir
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for filename in filenames:
            # Rename file if it contains digits or spaces
            new_filename = re.sub(r'\d', '', filename)  # Remove all digits
            new_filename = new_filename.lstrip()  # Remove leading spaces

            # If filename changed, rename it
            if filename != new_filename:
                old_file_path = os.path.join(dirpath, filename)
                new_file_path = os.path.join(dirpath, new_filename)
                os.rename(old_file_path, new_file_path)
                print(f"File renamed: {old_file_path} -> {new_file_path}")
                filename = new_filename  # update filename for further processing

            # If file has .vpk extension, move it to main folder
            if filename.endswith('.vpk'):
                old_file_path = os.path.join(dirpath, filename)
                new_file_path = os.path.join(root_dir, filename)

                # Check if file with same name exists in main folder, if yes, add unique suffix
                if os.path.exists(new_file_path):
                    base, extension = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(new_file_path):
                        new_file_path = os.path.join(root_dir, f"{base}_{counter}{extension}")
                        counter += 1

                shutil.move(old_file_path, new_file_path)  # Move file
                print(f"File moved: {old_file_path} -> {new_file_path}")

        # Remove all folders (keep only .vpk files)
        for dirname in dirnames:
            dir_path = os.path.join(dirpath, dirname)
            shutil.rmtree(dir_path)  # Remove folder and all its contents
            print(f"Folder removed: {dir_path}")

# Specify path to your root directory
root_dir = r""
move_vpk_files_and_cleanup(root_dir)
