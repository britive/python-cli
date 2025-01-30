import contextlib
import inspect
from importlib.metadata import version

from britive.britive import Britive


def get_dynamic_method_parameters(method):
    try:
        # create an instance of the Britive class, so we can inspect it
        # this doesn't need to actually connect to any tenant, and we couldn't even if we
        # wanted to since when performing shell completion we have no tenant/token
        # context in order to properly establish a connection.
        b = Britive(token='ignore', tenant='britive.com', query_features=False)

        # parse the method, so we can determine where in the "hierarchy" we are
        # and what commands/subcommands the user should be presented with

        for part in method.split('.'):
            b = getattr(b, part)

        params = {}
        spec = inspect.getfullargspec(b)
        # reformat parameters into a more consumable dict while holds all the required details
        helper = spec[6]
        helper.pop('return', None)

        for param in helper:
            params[param] = {}

        defaults = [] if spec[3] is None else list(spec[3])
        names = [] if spec[0] is None else list(spec[0])

        if len(defaults) > 0:
            for i in range(1, len(defaults) + 1):
                name = names[-1 * i]
                default = defaults[-1 * i]
                params[name]['default'] = '<empty string>' if default == '' else default

        # we don't REALLY need the doc string so if there are errors just eat them and move on
        with contextlib.suppress(Exception):
            doc_lines = inspect.getdoc(b)
            doc_lines = doc_lines.replace(':returns:', 'RETURNSPLIT')
            doc_lines = doc_lines.replace(':return:', 'RETURNSPLIT')
            doc_lines = doc_lines.split('RETURNSPLIT', maxsplit=1)[0].split(':param ')[1:]

            for line in doc_lines:
                helper = line.split(':')
                name = helper[0].strip()
                help_text = ''.join(helper[1].strip().splitlines()).replace('    ', ' ')
                params[name]['help'] = help_text

        param_list = []

        for name, values in params.items():
            help_text = values.get('help') or ''

            if 'default' in values:  # cannot do a .get('default') as the default value could be False/None/etc.
                preamble = f'[optional: default = {values["default"]}]'
                help_text = preamble if help_text == '' else f'{preamble} - {help_text}'

            param = {'flag': f'--{name.replace("_", "-")}', 'help': help_text}

            param_list.append(param)

        param_list.append(
            {'flag': '---------------------', 'help': 'separator between sdk parameters and cli parameters'}
        )

        return param_list
    except Exception:
        return []


def command_api_patch_shell_complete(cls):
    # click < 8.0.0 does shell completion different...
    # not all the classes/decorators are available, so we cannot
    # create custom shell completions like we can with click > 8.0.0
    major, minor = version('click').split('.')[:2]

    # we cannot patch the shell_complete method because it does not exist (click 7.x doesn't have it)
    # future proofing this as well in case click 9.x changes things up a lot
    if int(major) != 8:
        return

    # we could potentially patch but there could be changes to shell_complete method which are not
    # accounted for in this patch - we will have to manually review any changes and ensure they are
    # backwards compatible.
    if int(minor) != 1:
        return

    from click import Context, Option
    from click.core import ParameterSource
    from click.shell_completion import CompletionItem

    # https://stackoverflow.com/questions/43778914/python3-using-super-in-eq-methods-raises-runtimeerror-super-class
    __class__ = cls  # provide closure cell for super()  # noqa: F841

    def shell_complete(self, ctx: Context, incomplete: str) -> list[CompletionItem]:
        from click.shell_completion import CompletionItem  # here since this method will be monkey patched in

        results: list[CompletionItem] = []

        if incomplete and not incomplete[0].isalnum():
            method = ctx.params.get('method')
            if method:
                dynamic_params = get_dynamic_method_parameters(method)

                results.extend(
                    CompletionItem(p['flag'], help=p['help'])
                    for p in dynamic_params
                    if p['flag'].startswith(incomplete)
                )

            for param in self.get_params(ctx):
                if (
                    not isinstance(param, Option)
                    or param.hidden
                    or (
                        not param.multiple
                        and ctx.get_parameter_source(param.name)  # type: ignore
                        is ParameterSource.COMMANDLINE
                    )
                ):
                    continue

                results.extend(
                    CompletionItem(name, help=param.help)
                    for name in [*param.opts, *param.secondary_opts]
                    if name.startswith(incomplete)
                )

        results.extend(super().shell_complete(ctx, incomplete))

        return results

    cls.shell_complete = shell_complete
