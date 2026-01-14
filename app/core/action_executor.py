import subprocess
import webbrowser
import os
import platform


class ActionExecutor:
    def __init__(self):
        pass

    def execute(self, action):
        print("[ActionExecutor] execute called with:", action)

        if not action:
            print("[ActionExecutor] No action provided")
            return

        action_type = action.get("type")

        if action_type == "None" or action_type is None:
            print("[ActionExecutor] Action type is None, doing nothing")
            return

        if action_type == "Open Application":
            self.open_application(action.get("path"))

        elif action_type == "Open Website":
            self.open_website(action.get("url"))

        elif action_type == "Run Command":
            self.run_command(action.get("command"))

        else:
            print("[ActionExecutor] Unknown action type:", action_type)

    def open_application(self, path):
        if not path:
            print("[ActionExecutor] No application path provided")
            return

        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen([path])
            print(f"[ActionExecutor] Opened application: {path}")
        except Exception as e:
            print("[ActionExecutor] Error opening application:", e)

    def open_website(self, url):
        if not url:
            print("[ActionExecutor] No URL provided")
            return

        try:
            webbrowser.open(url)
            print(f"[ActionExecutor] Opened website: {url}")
        except Exception as e:
            print("[ActionExecutor] Error opening website:", e)

    def run_command(self, cmd):
        if not cmd:
            print("[ActionExecutor] No command provided")
            return

        try:
            subprocess.Popen(cmd, shell=True)
            print(f"[ActionExecutor] Executed command: {cmd}")
        except Exception as e:
            print("[ActionExecutor] Error running command:", e)