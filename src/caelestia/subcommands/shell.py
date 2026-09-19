import json
import os
import subprocess
from argparse import Namespace

from caelestia.utils.paths import c_cache_dir

CONFIG_NAME = "caelestia"


class Command:
    args: Namespace

    def __init__(self, args: Namespace) -> None:
        self.args = args

    def run(self) -> None:
        if self.args.show:
            # Print the ipc
            self.print_ipc()
        elif self.args.log:
            # Print the log
            self.print_log()
        elif self.args.kill:
            # Kill the shell
            self.shell("kill")
        elif self.args.message:
            # Send a message
            self.message(*self.args.message)
        else:
            # Start the shell
            args = ["qs", *self.launch_args(), "-n"]
            if self.args.log_rules:
                args.extend(["--log-rules", self.args.log_rules])
            if self.args.daemon:
                args.append("-d")
                subprocess.run(args)
            else:
                shell = subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True)

                # Ensure stdout is not None for the type checker
                if shell.stdout:
                    for line in shell.stdout:
                        if self.filter_log(line):
                            print(line, end="")

    def launch_args(self) -> list[str]:
        # Launching goes by config name so the installed config is picked up,
        # unless an explicit path is set
        override = os.environ.get("CAELESTIA_SHELL_PATH")
        return ["-p", override] if override else ["-c", CONFIG_NAME]

    def instance_args(self) -> list[str]:
        """Config selection args for talking to the running shell.

        `-c caelestia` only resolves a shell launched from the installed
        config directory. The shell fork's `task dev` starts it with
        `qs -p <repo>` instead, which that lookup cannot see, so locate the
        running instance by config path rather than assuming the name.
        """
        override = os.environ.get("CAELESTIA_SHELL_PATH")
        if override:
            return ["-p", override]

        instances = self.instances()

        if not instances:
            raise SystemExit("No running caelestia shell found. Start one with 'caelestia shell -d'.")

        if len(instances) > 1:
            running = "\n".join(f"  {i['config_path']} (pid {i['pid']})" for i in instances)
            raise SystemExit(
                f"Multiple caelestia shells are running:\n{running}\n"
                "Set CAELESTIA_SHELL_PATH to the one you want to talk to."
            )

        return ["-p", instances[0]["config_path"]]

    def instances(self) -> list[dict]:
        """Running quickshell instances that look like a caelestia shell.

        Matched on config path so this covers both the installed config
        (~/.config/quickshell/caelestia) and a shell run straight out of a
        checkout, as the fork's `task dev` does.
        """
        try:
            instances = json.loads(
                subprocess.check_output(["qs", "list", "-a", "-j"], text=True, stderr=subprocess.DEVNULL)
            )
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return []

        return [i for i in instances if CONFIG_NAME in i.get("config_path", "").lower()]

    def shell(self, *args: str) -> str:
        try:
            return subprocess.check_output(["qs", *self.instance_args(), *args], text=True)
        except subprocess.CalledProcessError as e:
            raise SystemExit(f"Shell command failed (exit {e.returncode}): qs {' '.join(args)}") from e

    def filter_log(self, line: str) -> bool:
        return f"Cannot open: file://{c_cache_dir}/imagecache/" not in line

    def print_ipc(self) -> None:
        print(self.shell("ipc", "show"), end="")

    def print_log(self) -> None:
        if self.args.log_rules:
            log = self.shell("log", "-r", self.args.log_rules)
        else:
            log = self.shell("log")
        # FIXME: remove when logging rules are added/warning is removed
        for line in log.splitlines():
            if self.filter_log(line):
                print(line)

    def message(self, *args: list[str]) -> None:
        print(self.shell("ipc", "call", *args), end="")
