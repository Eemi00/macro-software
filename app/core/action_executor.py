UI_ONLY = True

class ActionExecutor:
    def execute(self, action, force=False):
        if not action:
            return

        action_type = action.get("type")
        value = action.get("value", "")

        # If UI_ONLY is True but force=False → do NOT execute
        if UI_ONLY and not force:
            print(f"[UI MODE] Would execute: {action_type} -> {value}")
            return

        # Import only what is needed
        import webbrowser
        import subprocess

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
                subprocess.Popen(value, shell=True)
            return

        # Only import keyboard if needed
        if action_type == "key_combo":
            try:
                import keyboard
                keyboard.press_and_release(value)
            except ModuleNotFoundError:
                print("[ERROR] 'keyboard' module not installed. Cannot run key_combo.")
            return

        if action_type == "type_text":
            try:
                import keyboard
                keyboard.write(value)
            except ModuleNotFoundError:
                print("[ERROR] 'keyboard' module not installed. Cannot type text.")
            return