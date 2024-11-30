import os
import shutil
from tkinter import messagebox

class Installer:
    def __init__(self, game_path, translations):
        self.game_path = game_path
        self.t = translations
        
    def update_gameinfo(self):
        """Updates the gameinfo.gi file in the game directory"""
        if not self.game_path:
            messagebox.showerror(self.t['path_error'], self.t['path_error_msg'])
            return False
            
        if not os.path.isdir(self.game_path) or not self.game_path.endswith("Deadlock"):
            messagebox.showerror(self.t['error'], self.t['invalid_path_error'])
            return False
            
        try:
            # Path to our gameinfo.gi in the program folder
            source_gameinfo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gameinfo.gi")
            if not os.path.exists(source_gameinfo):
                source_gameinfo = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gameinfo.gi")
            
            print(f"Debug: Source gameinfo path = {source_gameinfo}")
            print(f"Debug: Source gameinfo exists = {os.path.exists(source_gameinfo)}")
            
            if not os.path.exists(source_gameinfo):
                messagebox.showerror(self.t['error'], self.t['gameinfo_not_found'])
                return False
                
            # Path to copy gameinfo.gi
            target_dir = os.path.join(self.game_path, "game", "citadel")
            target_gameinfo = os.path.join(target_dir, "gameinfo.gi")
            
            print(f"Debug: Target directory = {target_dir}")
            print(f"Debug: Target gameinfo path = {target_gameinfo}")
            
            # Create directory if it doesn't exist
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            # Copy our gameinfo.gi
            print(f"Debug: Copying gameinfo.gi")
            shutil.copy2(source_gameinfo, target_gameinfo)
            print(f"Debug: File copied successfully")
            
            return True
            
        except Exception as e:
            print(f"Debug: Error during gameinfo update: {str(e)}")
            messagebox.showerror(self.t['error'], f"{self.t['gameinfo_error']}:\n{str(e)}")
            return False
            
    def install_mods(self, selected_mods, progress_callback=None):
        """Installs selected mods with progress tracking"""
        print("\nDebug: Starting mod installation")
        print(f"Debug: Game path = {self.game_path}")
        print("Debug: Selected mods structure:", selected_mods)
        
        if not self.game_path:
            messagebox.showerror(self.t['path_error'], self.t['path_error_msg'])
            return False
            
        if not os.path.isdir(self.game_path) or not self.game_path.endswith("Deadlock"):
            messagebox.showerror(self.t['error'], self.t['invalid_path_error'])
            return False
            
        try:
            # Count the number of selected mods
            total_mods = 0
            for category, mods in selected_mods.items():
                if category != 'Skins':
                    total_mods += sum(1 for mod, var in mods.items() if var.get())
                else:
                    total_mods += sum(1 for char, var in mods.items() if var.get() != "Default")
            
            total_steps = total_mods + 2  # +2 for cleaning and gameinfo
            current_step = 0
            
            # Update progress
            if progress_callback:
                progress_callback(0, self.t['cleaning'])
            
            print("Debug: Cleaning old mods...")
            # Clean old mods
            self.clean_old_mods()
            current_step += 1
            
            if progress_callback:
                progress_callback(current_step / total_steps * 100, self.t['installing_mods'])
            
            # Install mods
            for category, mods in selected_mods.items():
                print(f"\nDebug: Processing category {category}")
                if category != 'Skins':
                    # For regular categories
                    for mod, var in mods.items():
                        if var.get():
                            print(f"Debug: Installing mod {mod}")
                            self.install_mod(mod)
                            current_step += 1
                            if progress_callback:
                                progress_callback(current_step / total_steps * 100)
                else:
                    # For skins
                    for character, var in mods.items():
                        skin = var.get()
                        if skin != "Default":
                            print(f"Debug: Installing skin {skin} for {character}")
                            self.install_mod(skin)
                            current_step += 1
                            if progress_callback:
                                progress_callback(current_step / total_steps * 100)
            
            # Update gameinfo.gi
            if progress_callback:
                progress_callback((total_steps - 1) / total_steps * 100, self.t['update_gameinfo'])
            self.update_gameinfo()
            
            if progress_callback:
                progress_callback(100, self.t['installation_complete'])
            
            messagebox.showinfo(self.t['success'], self.t['installation_complete'])
            return True
            
        except Exception as e:
            print(f"Debug: Error during installation: {str(e)}")
            messagebox.showerror(self.t['error'], str(e))
            return False
            
    def clean_old_mods(self):
        """Cleans old mods before installing new ones"""
        addons_dir = os.path.join(self.game_path, "game", "citadel", "addons")
        print(f"Debug: Cleaning directory {addons_dir}")
        if os.path.exists(addons_dir):
            for file in os.listdir(addons_dir):
                if file.endswith('.vpk'):
                    print(f"Debug: Removing file {file}")
                    os.remove(os.path.join(addons_dir, file))
        else:
            print(f"Debug: Creating directory {addons_dir}")
            os.makedirs(addons_dir)
            
    def get_next_pak_number(self, addons_dir):
        """Finds the next available number for pak file"""
        max_num = 0
        if os.path.exists(addons_dir):
            for file in os.listdir(addons_dir):
                if file.startswith('pak') and file.endswith('_dir.vpk'):
                    try:
                        num = int(file[3:5])  # Extract number from pakXX_dir.vpk
                        max_num = max(max_num, num)
                    except ValueError:
                        continue
        return max_num + 1
        
    def install_mod(self, mod_name):
        """Installs a specific mod"""
        source_file = f"{mod_name}.vpk"
        print(f"Debug: Looking for mod file {source_file}")
        
        source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mods", source_file)
        if not os.path.exists(source_path):
            source_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mods", source_file)
            
        print(f"Debug: Source file path = {source_path}")
        print(f"Debug: Source file exists = {os.path.exists(source_path)}")
            
        if os.path.exists(source_path):
            addons_dir = os.path.join(self.game_path, "game", "citadel", "addons")
            pak_num = self.get_next_pak_number(addons_dir)
            target_file = f"pak{pak_num:02d}_dir.vpk"
            target_path = os.path.join(addons_dir, target_file)
            
            print(f"Debug: Copying to {target_path}")
            shutil.copy2(source_path, target_path)
            print(f"Debug: File copied successfully")

    def install_localization(self, localization_files):
        """Installs localization files"""
        if not self.game_path:
            messagebox.showerror(self.t['path_error'], self.t['path_error_msg'])
            return False

        try:
            # Correct path for localization
            localization_dir = os.path.join(self.game_path, "game", "citadel", "resource", "localization", "citadel_gc")
            
            # Create directory if it doesn't exist
            if not os.path.exists(localization_dir):
                os.makedirs(localization_dir)
                
            # Copy localization files
            for file in localization_files:
                source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "new_localization", file)
                if not os.path.exists(source_path):
                    source_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "new_localization", file)
                
                if os.path.exists(source_path):
                    shutil.copy2(source_path, os.path.join(localization_dir, file))
                    
            return True
            
        except Exception as e:
            messagebox.showerror(self.t['error'], f"{self.t['localization_error']}:\n{str(e)}")
            return False
            
    def remove_localization(self):
        """Removes localization files"""
        if not self.game_path:
            messagebox.showerror(self.t['path_error'], self.t['path_error_msg'])
            return False
            
        try:
            # Correct path for localization
            localization_dir = os.path.join(self.game_path, "game", "citadel", "resource", "localization", "citadel_gc")
            
            # Remove localization files if directory exists
            if os.path.exists(localization_dir):
                for file in os.listdir(localization_dir):
                    if file.endswith('.txt'):
                        os.remove(os.path.join(localization_dir, file))
                        
            return True
            
        except Exception as e:
            messagebox.showerror(self.t['error'], f"{self.t['localization_error']}:\n{str(e)}")
            return False
            
    def restore_original_localization(self):
        """Restores original localization"""
        if not self.game_path:
            messagebox.showerror(self.t['path_error'], self.t['path_error_msg'])
            return False
            
        try:
            # Correct path for localization
            localization_dir = os.path.join(self.game_path, "game", "citadel", "resource", "localization", "citadel_gc")
            
            # Create directory if it doesn't exist
            if not os.path.exists(localization_dir):
                os.makedirs(localization_dir)
                
            # Path to original localization files
            original_loc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "original_localization")
            if not os.path.exists(original_loc_path):
                original_loc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "original_localization")
                
            # Copy original localization files
            for file in os.listdir(original_loc_path):
                if file.endswith('.txt'):
                    source_path = os.path.join(original_loc_path, file)
                    if os.path.exists(source_path):
                        shutil.copy2(source_path, os.path.join(localization_dir, file))
                        
            return True
            
        except Exception as e:
            messagebox.showerror(self.t['error'], f"{self.t['localization_error']}:\n{str(e)}")
            return False

    def remove_all_mods(self):
        """Removes all mods from the addons directory"""
        if not self.game_path:
            messagebox.showerror(self.t['path_error'], self.t['path_error_msg'])
            return False
            
        try:
            # Path to the addons directory
            addons_dir = os.path.join(self.game_path, "game", "citadel", "addons")
            
            if os.path.exists(addons_dir):
                # Remove all .vpk files
                for file in os.listdir(addons_dir):
                    if file.endswith('.vpk'):
                        file_path = os.path.join(addons_dir, file)
                        os.remove(file_path)
                        
                messagebox.showinfo(self.t['success'], self.t['mods_removed'])
                return True
            else:
                messagebox.showinfo(self.t['info'], self.t['no_mods_found'])
                return True
                
        except Exception as e:
            messagebox.showerror(self.t['error'], f"{self.t['remove_mods_error']}:\n{str(e)}")
            return False
