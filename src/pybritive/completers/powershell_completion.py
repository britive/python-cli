from click.shell_completion import add_completion_class
from click.shell_completion import ShellComplete, CompletionItem
import os
from click.parser import split_arg_string
import typing as t


# inspired by https://raw.githubusercontent.com/tibortakacs/powershell-argcomplete/master/mat.complete.ps1
_powershell_source = """\
$%(complete_func)s = {
    param($wordToComplete, $commandAst, $cursorPosition)

    # in case of scripts, this object holds the current line after string conversion
    $line = "$commandAst"

    # The behaviour of completion should depend on the trailing spaces in the current line:
    # * "command subcommand " --> TAB --> Completion items parameters/sub-subcommands of "subcommand"
    # * "command subcom" --> TAB --> Completion items to extend "subcom" into matching subcommands.
    # $line never contains the trailing spaces. However, $cursorPosition is the length of the original
    # line (with trailing spaces) in this case. This comparison allows the expected user experience.
    if ($cursorPosition -gt $line.Length) {
        $line = "$line "
    }

    # set environment variables that pybritive completion will use
    New-Item -Path Env: -Name COMP_LINE -Value $line | Out-Null # Current line
    New-Item -Path Env: -Name %(complete_var)s -Value "powershell_complete" | Out-Null

    # call %(prog_name)s and it will inspect env vars and provide completion results
    Invoke-Expression %(prog_name)s -ErrorAction SilentlyContinue | Tee-Object -Var completionResult | Out-Null

    # cleanup environment variables
    Remove-Item Env:\COMP_LINE | Out-Null
    Remove-Item Env:\%(complete_var)s | Out-Null

    # get list of completion items
    $items = $completionResult -split '\\r?\\n'
    
    $items | ForEach-Object {"$_ "} # trailing space important as completion is "done"
}

# register tab completion
Register-ArgumentCompleter -Native -CommandName %(prog_name)s -ScriptBlock $%(complete_func)s
"""


@add_completion_class
class PowershellComplete(ShellComplete):
    name = "powershell"
    source_template = _powershell_source

    def get_completion_args(self):
        line = os.environ["COMP_LINE"]
        cwords = split_arg_string(line)
        num_cwords = len(cwords)
        args = cwords[1:num_cwords]

        if line.endswith(' '):
            incomplete = ''
        else:
            try:
                incomplete = args.pop()
            except IndexError:
                incomplete = ''
        return args, incomplete

    def format_completion(self, item: CompletionItem) -> str:
        value = item.value
        if ' ' in value:
            value = f'"{value}"'
        return f"{value}"

    def source_vars(self) -> t.Dict[str, t.Any]:
        """Vars for formatting :attr:`source_template`.
        By default this provides ``complete_func``, ``complete_var``,
        and ``prog_name``.
        """
        return {
            "complete_func": self.func_name[1:],  # remove leading _
            "complete_var": self.complete_var,
            "prog_name": self.prog_name
        }