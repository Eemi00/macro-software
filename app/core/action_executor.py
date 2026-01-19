# core/action_executor.py

import webbrowser
import subprocess

try:
    import keyboard
except ImportError:
    keyboard = None

# Default safe mode prevents accidental execution during testing
UI_ONLY = True

class ActionExecutor:
    """Handles execution of configured actions."""
    
    def execute(self, action, force=False):
        """
        Executes the given action.

        Args:
            action (dict): The action configuration.
            force (bool): If True, bypasses UI_ONLY safe mode.
        """
        if not action:
            return

        action_type = action.get("type")
        value = action.get("value", "")

        if UI_ONLY and not force:
            print(f"[UI MODE] Would execute: {action_type} -> {value}")
            return

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
