import re
from click.shell_completion import add_completion_class, BashComplete
from gettext import gettext as _


# inspired by https://github.com/pallets-eco/click-bash4.2-completion
_bash_42_source = """\
%(complete_func)s() {
    local IFS=$'\\n'
    local response
    response=$(env COMP_WORDS="${COMP_WORDS[*]}" COMP_CWORD=$COMP_CWORD \
%(complete_var)s=bash_complete $1)
    for completion in $response; do
        IFS=',' read type value <<< "$completion"
        if [[ $type == 'dir' ]]; then
            COMPREPLY=()
            compopt -o dirnames
        elif [[ $type == 'file' ]]; then
            COMPREPLY=()
            compopt -o default
        elif [[ $type == 'plain' ]]; then
            COMPREPLY+=($value)
        fi
    done
    return 0
}
%(complete_func)s_setup() {
    local COMPLETION_OPTIONS=""
    local BASH_VERSION_ARR=(${BASH_VERSION//./ })
    # Only BASH version 4.4 and later have the nosort option.
    if [ ${BASH_VERSION_ARR[0]} -gt 4 ] || ([ ${BASH_VERSION_ARR[0]} -eq 4 ] \
&& [ ${BASH_VERSION_ARR[1]} -ge 4 ]); then
        COMPLETION_OPTIONS="-o nosort"
    fi
    complete $COMPLETION_OPTIONS -F %(complete_func)s %(prog_name)s
}
%(complete_func)s_setup;
"""


@add_completion_class
class _PatchedBashComplete(BashComplete):
    """ Patched Shell completion for Bash """
    source_template = _bash_42_source
    name = 'bash'  # this will override the default bash provided by click

    # change the original version check
    def _check_version(self) -> None:
        import subprocess

        output = subprocess.run(
            ["bash", "-c", "echo ${BASH_VERSION}"], stdout=subprocess.PIPE
        )
        match = re.search(r"^(\d+)\.(\d+)\.\d+", output.stdout.decode())

        if match is not None:
            major, minor = match.groups()

            if major < "4" or major == "4" and minor < "2":
                raise RuntimeError(
                    _(
                        "Shell completion is not supported for Bash"
                        " versions older than 4.2."
                    )
                )
        else:
            raise RuntimeError(
                _("Couldn't detect Bash version, shell completion is not supported.")
            )
