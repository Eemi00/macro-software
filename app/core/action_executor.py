# core/action_executor.py

import webbrowser
import subprocess

try:
    import keyboard
except ImportError:
    keyboard = None

class ActionExecutor:
    """Handles execution of configured actions."""
    
    def execute(self, action):
        """
        Executes the given action.

        Args:
            action (dict): The action configuration.
        """
        if not action:
            return

        action_type = action.get("type")
        value = action.get("value", "")

        if action_type == "none":
            return

        if action_type == "open_website":
            if value:
                webbrowser.open(value)
            return

        if action_type == "open_app":
            if value:
                subprocess.Popen(value)
            return

        if action_type == "run_command":
            if value:
                subprocess.Popen(f'start cmd /k "{value}"', shell=True)
            return

        if action_type == "key_combo":
            if keyboard and value:
                try:
                    keyboard.press_and_release(value)
                except Exception as e:
                    print(f"[ERROR] Failed to execute key combo: {e}")
            elif not keyboard:
                print("[ERROR] 'keyboard' module not installed.")
            return

        if action_type == "type_text":
            if keyboard and value:
                try:
                    keyboard.write(value)
                except Exception as e:
                    print(f"[ERROR] Failed to write text: {e}")
            elif not keyboard:
                print("[ERROR] 'keyboard' module not installed.")
            return
