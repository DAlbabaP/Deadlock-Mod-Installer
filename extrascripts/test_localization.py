from localization_handler import replace_localization_with_english, process_all_localizations
import os
import shutil

def process_all_languages():
    # Directory paths
    original_dir = r"C:\Users\pokho\PycharmProjects\DeadlockInstaller\original_localization"
    new_dir = r"C:\Users\pokho\PycharmProjects\DeadlockInstaller\new_localization"
    
    # Create directory for new files if it doesn't exist
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    
    # English file - source
    source_file = os.path.join(original_dir, "citadel_gc_english.txt")
    if not os.path.exists(source_file):
        print(f"Source English file not found: {source_file}")
        return
    
    # Process all localization files
    for filename in os.listdir(original_dir):
        if filename.startswith("citadel_gc_") and filename.endswith(".txt") and filename != "citadel_gc_english.txt":
            # Check file size (skip empty or very small files)
            file_path = os.path.join(original_dir, filename)
            if os.path.getsize(file_path) < 1000:  # skip files smaller than 1KB
                print(f"Skipping {filename} - file too small")
                continue
                
            print(f"\nProcessing {filename}...")
            
            # Copy file to new directory
            target_file = os.path.join(new_dir, filename)
            shutil.copy2(file_path, target_file)
            
            # Apply text replacement
            success = replace_localization_with_english(source_file, target_file)
            
            if success:
                print(f"Successfully processed {filename}")
            else:
                print(f"Failed to process {filename}")

if __name__ == "__main__":
    process_all_languages()
