"""
Script editing utility for simplex-engine MVP-3.
Allows users to list, view, and edit scripts from the CLI, with hot-reload support.
"""
from simplex.script.cli_script_editor import CLIScriptEditor

def run_script_editor():
    editor = CLIScriptEditor()
    while True:
        print("\nScript Editor Menu:")
        print("1. List scripts")
        print("2. View script")
        print("3. Edit script")
        print("4. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            editor.list_scripts()
        elif choice == "2":
            scripts = editor.list_scripts()
            idx = input("Enter script index to view: ").strip()
            if idx.isdigit() and int(idx) < len(scripts):
                editor.view_script(f"{editor.script_dir}/{scripts[int(idx)]}")
        elif choice == "3":
            scripts = editor.list_scripts()
            idx = input("Enter script index to edit: ").strip()
            if idx.isdigit() and int(idx) < len(scripts):
                editor.edit_script(f"{editor.script_dir}/{scripts[int(idx)]}")
        elif choice == "4":
            print("Exiting script editor.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    run_script_editor()