import tkinter as tk
from gui import ModInstallerGUI
import sys
import locale
import os

def get_base_path():
    """Get the base path of the application, works for both development and compiled versions"""
    if getattr(sys, 'frozen', False):
        # If running as compiled executable (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # If running in development
        return os.path.dirname(os.path.abspath(__file__))

def main():
    # Set console codepage for proper Unicode handling on Windows
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.kernel32.SetConsoleCP(65001)
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    
    # Set system locale for proper text handling
    locale.setlocale(locale.LC_ALL, '')
    
    # Change working directory to application base path
    os.chdir(get_base_path())
    
    # Initialize and run the main application window
    root = tk.Tk()
    app = ModInstallerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
