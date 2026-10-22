import platform
import shutil
import subprocess

import click

clipboard_commands = {
    'darwin': [['pbcopy']],
    'windows': [['clip']],
    'linux': [
        ['wl-copy'],
        ['xclip', '-selection', 'clipboard'],
        ['xsel', '--clipboard', '--input'],
        ['clip.exe'],  # WSL
    ],
}


def copy_to_clipboard(text: str) -> str:
    system = platform.system().lower()
    for command in clipboard_commands.get(system, clipboard_commands['linux']):
        if shutil.which(command[0]):
            subprocess.run(command, input=text, text=True, check=True)
            return command[0]
    raise click.ClickException(
        'No clipboard utility found. Install one of: '
        f'{", ".join(c[0] for c in clipboard_commands.get(system, clipboard_commands["linux"]))}.'
    )
