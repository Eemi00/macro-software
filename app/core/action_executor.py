# core/action_executor.py

UI_ONLY = True

class ActionExecutor:
    def execute(self, action, force=False):
        if not action:
            return

        action_type = action.get("type")
        value = action.get("value", "")

        if UI_ONLY and not force:
            print(f"[UI MODE] Would execute: {action_type} -> {value}")
            return

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

        if action_type == "key_combo":
            try:
                import keyboard
                if value:
                    keyboard.press_and_release(value)
            except ModuleNotFoundError:
                print("[ERROR] 'keyboard' module not installed.")
            return

        if action_type == "type_text":
            try:
                import keyboard
                if value:
                    keyboard.write(value)
            except ModuleNotFoundError:
                print("[ERROR] 'keyboard' module not installed.")
            return
