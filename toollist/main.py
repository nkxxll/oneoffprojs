import os
import shutil
import subprocess

cmds = [
    {
        "tool": "mise",
        "cmd": ["mise", "list"],
    },
    {
        "tool": "npm",
        "cmd": ["npm", "list", "-g"],
    },
    {
        "tool": "pnpm",
        "cmd": ["pnpm", "list", "-g"],
    },
    {
        "tool": "yarn",
        "cmd": ["yarn", "global", "list"],
    },
    {
        "tool": "uv",
        "cmd": ["uv", "tool", "list"],
    },
    {
        "tool": "pip",
        "cmd": ["pip", "list"],
    },
    {
        "tool": "poetry",
        "cmd": ["poetry", "show"],
    },
    {
        "tool": "cargo",
        "cmd": ["cargo", "install", "--list"],
    },
    {
        "tool": "gem",
        "cmd": ["gem", "list"],
    },
    {
        "tool": "brew",
        "cmd": ["brew", "list", "--installed-on-request"],
    },
    {
        "tool": "pacman",
        "cmd": ["pacman", "-Qe"],
    },
    {
        "tool": "apt",
        "cmd": ["apt", "list", "--installed"],
    },
    {
        "tool": "conda",
        "cmd": ["conda", "list"],
    },
]


def is_executable(file_path):
    # Using shutil.which() to get the executable path
    executable_path = shutil.which(file_path)

    # Check if the executable path is not None and is executable
    if executable_path and os.access(executable_path, os.X_OK):
        return True
    else:
        return False


def list_tools(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def main():
    successful = []
    failed = []
    
    for cmd in cmds:
        if is_executable(cmd["tool"]):
            print(f"{10 * "-"}  {cmd["tool"]}  {10 * "-"}")
            print(list_tools(cmd["cmd"]))
            successful.append(cmd["tool"])
        else:
            failed.append(cmd["tool"])
    
    print("\n" + "=" * 50)
    print(f"✓ Successful: {', '.join(successful)}")
    if failed:
        print(f"✗ Failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
