import keyboard
import subprocess
from time import sleep

# End and start vscode process to stop script execution. 
def reload_vscode_execution(event):
    if event.name == "esc":
        path_vscode = r"C:\Users\User\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        process_name = "Code.exe"
        
        subprocess.run(["taskkill", "/F", "/IM", process_name])  # End vscode process.
        sleep(1)        
        subprocess.Popen([path_vscode], shell=True)  # Start vscode process.


print("The script is running. Press Esc to exit of VSCode.")
keyboard.on_press(reload_vscode_execution)
keyboard.wait() 