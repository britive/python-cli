from pathlib import Path
import click
import configparser
import json
import toml


def lowercase(obj):
    """ Make dictionary lowercase """
    if isinstance(obj, dict):
        return {k.lower(): lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, (list, set, tuple)):
        t = type(obj)
        return t(lowercase(o) for o in obj)
    elif isinstance(obj, str):
        return obj.lower()
    else:
        return obj


def coalesce(*arg):
    for el in arg:
        if el is not None:
            return el
    return None


class ConfigManager:
    def __init__(self, cli: object, tenant_name: str = None):
        self.tenant_name = tenant_name
        self.path = str(Path.home() / '.britive' / 'pybritive.config')  # handle os specific separators properly
        self.config = None
        self.alias = None
        self.default_tenant = None
        self.tenants = None
        self.profile_aliases = None
        self.cli = cli

    def get_output_format(self, output_format: str = None):
        return coalesce(
            output_format,
            self.get_tenant().get('output_format'),
            self.config.get('global', {}).get('output_format'),
            'json'  # set to json if no output format is provided
        )

    def load(self):
        path = Path(self.path)

        if not path.is_file():
            return {}

        config = configparser.ConfigParser()
        config.optionxform = str  # maintain key case
        config.read(str(path))
        config = json.loads(json.dumps(config._sections))  # TODO this is messy but works for now
        self.config = lowercase(config)
        self.alias = None  # will be set in self.get_tenant()
        self.default_tenant = self.config.get('global', {}).get('default_tenant')
        self.tenants = {}
        for key in list(self.config.keys()):
            if key.startswith('tenant-'):
                ignore, alias = key.split('-')
                self.tenants[alias] = self.config[key]
        self.profile_aliases = self.config.get('profile-aliases', {})

    def get_tenant(self):
        # load up the config - doing it here instead of __init__ for the configure commands since config won't
        # yet exist and we don't want to error
        self.load()  # will set self.config and other variables

        # normalize the input
        name = self.tenant_name.lower() if self.tenant_name else None

        # do some error checking to ensure we can actually grab a tenant
        if len(self.tenants.keys()) == 0 and not name:
            raise click.ClickException(f'No tenants found in {self.path}. Cannot continue.')

        # attempt to determine the name of the tenant based on what the user passed in (or didn't pass in)
        provided_tenant_name = name if name else self.default_tenant

        if not provided_tenant_name:  # name not provided and no default has been set
            if len(self.tenants.keys()) != 1:
                raise click.ClickException('Tenant not provided, no default tenant set, and more than one '
                                           'tenant exists.')
            else:
                # nothing given but only 1 tenant so assume that is what should be used
                provided_tenant_name = list(self.tenants.keys())[0]

        # if we get here then we now have a tenant name we can check to ensure exists
        if provided_tenant_name not in self.tenants.keys() and not name:
            raise click.ClickException(f'Tenant name "{provided_tenant_name}" not found in {self.path}')

        self.alias = provided_tenant_name or name
        # return details about the requested tenant
        return self.tenants.get(provided_tenant_name, {'name': name})

    def save(self):
        config = configparser.ConfigParser()
        config.optionxform = str  # maintain key case
        config.read_dict(self.config)

        # write the new credentials file
        with open(str(self.path), 'w') as f:
            config.write(f, space_around_delimiters=False)

    def save_tenant(self, tenant: str, alias: str = None, output_format: str = None):
        if not alias:
            alias = tenant
        if f'tenant-{alias}' not in self.config.keys():
            self.config[f'tenant-{alias}'] = {}
        self.config[f'tenant-{alias}']['name'] = tenant
        if output_format:
            self.config[f'tenant-{alias}']['output_format'] = output_format
        self.save()

    def save_global(self, default_tenant_name: str = None, output_format: str = None):
        if not default_tenant_name and not output_format:
            return
        if 'global' not in self.config.keys():
            self.config['global'] = {}
        if default_tenant_name:
            self.config['global']['default_tenant'] = default_tenant_name
        if output_format:
            self.config['global']['output_format'] = output_format
        self.save()

    def save_profile_alias(self, alias, profile):
        self.profile_aliases[alias] = profile
        self.config['profile-aliases'] = self.profile_aliases
        self.save()

    # returns a dict of profile aliases that need to be created after listing profiles
    def import_global_npm_config(self):
        path = str(Path.home() / '.britive' / 'config')  # handle os specific separators properly
        with open(path, 'r') as f:
            npm_config = toml.load(f)
        tenant = npm_config.get('tenantURL', '').replace('https://', '').replace('.britive-app.com', '').lower()
        output_format = npm_config.get('output_format', '').lower()

        # reset the config as we are building a new one
        self.config = {
            'global': {}
        }
        if tenant != '':
            self.cli.print(f'Found tenant {tenant}.')
            self.config['global']['default_tenant'] = tenant
            self.config[f'tenant-{tenant}'] = {
                'name': tenant
            }
        if output_format != '':
            self.cli.print(f'Found default output format {output_format}.')
            self.config['global']['output_format'] = output_format

        self.save()
        self.load()

        return npm_config.get('envProfileMap', {})

