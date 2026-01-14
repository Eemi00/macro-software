import webbrowser
import subprocess
import keyboard


class ActionExecutor:
    def execute(self, action):
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
                subprocess.Popen(value, shell=True)
            return

        if action_type == "key_combo":
            if value:
                keyboard.press_and_release(value)
            return

        if action_type == "type_text":
            if value:
                keyboard.write(value)
            return