import os


def rename_file_to_folder_name(root_directory):
    """
    Recursively traverses the specified directory and renames a file if there is only one file in the folder.
    The file is renamed according to the folder name.
    :param root_directory: Path to the root directory.
    """
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Skip folders with more than one file
        if len(filenames) == 1:
            folder_name = os.path.basename(dirpath)  # Get folder name
            file_path = os.path.join(dirpath, filenames[0])  # Path to the only file
            file_extension = os.path.splitext(filenames[0])[1]  # Get file extension

            # New path with folder name
            new_file_name = f"{folder_name}{file_extension}"
            new_file_path = os.path.join(dirpath, new_file_name)

            # Rename the file
            if file_path != new_file_path:
                os.rename(file_path, new_file_path)
                print(f"File renamed: {file_path} -> {new_file_path}")


# Specify path to your directory
root_dir = r""
rename_file_to_folder_name(root_dir)
