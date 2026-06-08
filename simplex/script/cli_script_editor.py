"""
Basic CLI implementation of ScriptEditorInterface for simplex-engine.
Allows listing, viewing, and editing scripts from the terminal.
"""

import os
import subprocess
from .script_editor_interface import ScriptEditorInterface


class CLIScriptEditor(ScriptEditorInterface):
    def __init__(self, script_dir="examples/mvp/scripts"):
        self.script_dir = script_dir

    def list_scripts(self):
        try:
            scripts = [f for f in os.listdir(self.script_dir) if f.endswith(".py")]
            print("Available scripts:")
            for idx, script in enumerate(scripts):
                print(f"  [{idx}] {script}")
            return scripts
        except Exception as e:
            print(f"Error listing scripts: {e}")
            return []

    def view_script(self, script_path):
        try:
            with open(script_path, "r") as f:
                print(f.read())
        except Exception as e:
            print(f"Error viewing script: {e}")

    def edit_script(self, script_path):
        editor = os.environ.get("EDITOR", "nano")
        try:
            subprocess.call([editor, script_path])
        except Exception as e:
            print(f"Error launching editor: {e}")
