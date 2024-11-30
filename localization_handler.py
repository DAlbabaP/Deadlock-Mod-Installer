import os
import shutil

def replace_localization_with_english(source_file, target_file):
    """
    Replace hero names and item descriptions with English versions starting from 'Steam_RP_hero_vampire'
    
    Args:
        source_file (str): Path to the English localization file
        target_file (str): Path to the target language file to be modified
    """
    try:
        # Read the English content first
        with open(source_file, 'r', encoding='utf-8') as f:
            english_content = f.read()
            
        # Find the start of the section in English file
        start_marker = 'Steam_RP_hero_vampire'
        end_marker = '}'
        
        # Extract the English section
        start_idx = english_content.find(start_marker)
        if start_idx == -1:
            raise ValueError("Could not find starting marker in English file")
            
        # Find the last closing brace
        end_idx = english_content.rfind(end_marker)
        if end_idx == -1:
            raise ValueError("Could not find end marker in English file")
            
        english_section = english_content[start_idx:end_idx+1]
        
        # Now read and modify the target file
        with open(target_file, 'r', encoding='utf-8') as f:
            target_content = f.read()
            
        # Find the same section in target file
        target_start_idx = target_content.find(start_marker)
        if target_start_idx == -1:
            raise ValueError(f"Could not find starting marker in target file: {target_file}")
            
        target_end_idx = target_content.rfind(end_marker)
        if target_end_idx == -1:
            raise ValueError(f"Could not find end marker in target file: {target_file}")
            
        # Create new content with English section
        new_content = (
            target_content[:target_start_idx] + 
            english_section + 
            target_content[target_end_idx+1:]
        )
        
        # Write the modified content
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return True
        
    except Exception as e:
        print(f"Error processing file {target_file}: {str(e)}")
        return False

def process_all_localizations(localization_dir):
    """
    Process all localization files in the directory.
    
    Args:
        localization_dir (str): Directory containing localization files
    """
    english_file = os.path.join(localization_dir, 'english.txt')
    if not os.path.exists(english_file):
        raise FileNotFoundError("English localization file not found")
        
    results = []
    
    # Process each .txt file in the directory except english.txt
    for filename in os.listdir(localization_dir):
        if filename.endswith('.txt') and filename != 'english.txt':
            target_file = os.path.join(localization_dir, filename)
            success = replace_localization_with_english(english_file, target_file)
            results.append((filename, success))
            
    return results
