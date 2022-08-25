import os
from pathlib import Path
import click
import configparser
import json
import toml
from ..choices.output_format import output_format_choices
from ..choices.backend import backend_choices


def extract_tenant(tenant_key):
    return tenant_key.replace('tenant-', '')


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


non_tenant_sections = [
    'global',
    'profile-aliases'
]

global_fields = [
    'default_tenant',
    'output_format',
    'credential_backend',
    'auto-refresh-profile-cache'
]

tenant_fields = [
    'name',
    'output_format'
]


class ConfigManager:
    def __init__(self, cli: object, tenant_name: str = None):
        self.tenant_name = tenant_name
        self.home = os.getenv('PYBRITIVE_HOME_DIR', str(Path.home()))
        self.path = str(Path(self.home) / '.britive' / 'pybritive.config')  # handle os specific separators properly
        self.config = None
        self.alias = None
        self.default_tenant = None
        self.tenants = None
        self.profile_aliases = {}
        self.cli = cli
        self.loaded = False
        self.validation_error_messages = []

    def get_output_format(self, output_format: str = None):
        return coalesce(
            output_format,
            self.get_tenant().get('output_format'),
            self.config.get('global', {}).get('output_format'),
            'json'  # set to json if no output format is provided
        )

    def load(self, force=False):
        if self.loaded and not force:
            return
        path = Path(self.path)

        if not path.is_file():  # config file does not yet exist, create it as an empty file
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text('')

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
                alias = extract_tenant(key)
                self.tenants[alias] = self.config[key]
        self.profile_aliases = self.config.get('profile-aliases', {})
        self.loaded = True


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
        self.validate()  # ensure we are actually writing a valid config
        config = configparser.ConfigParser()
        config.optionxform = str  # maintain key case
        config.read_dict(self.config)

        # write the new credentials file
        with open(str(self.path), 'w') as f:
            config.write(f, space_around_delimiters=False)

    def save_tenant(self, tenant: str, alias: str = None, output_format: str = None):
        self.load()
        tenant = tenant.replace('.britive-app.com', '')
        if alias:
            alias = alias.replace('.britive-app.com', '')
        else:
            alias = tenant
        if f'tenant-{alias}' not in self.config.keys():
            self.config[f'tenant-{alias}'] = {}
        self.config[f'tenant-{alias}']['name'] = tenant
        if output_format:
            self.config[f'tenant-{alias}']['output_format'] = output_format
        self.save()

    def save_global(self, default_tenant_name: str = None, output_format: str = None, backend: str = None):
        self.load()
        if not default_tenant_name and not output_format and not backend:
            return
        if 'global' not in self.config.keys():
            self.config['global'] = {}
        if default_tenant_name:
            self.config['global']['default_tenant'] = default_tenant_name.replace('.britive-app.com', '')
        if output_format:
            self.config['global']['output_format'] = output_format
        if backend:
            self.config['global']['credential_backend'] = backend
        self.save()

    def save_profile_alias(self, alias, profile):
        self.profile_aliases[alias] = profile
        self.config['profile-aliases'] = self.profile_aliases
        self.save()

    # returns a dict of profile aliases that need to be created after listing profiles
    def import_global_npm_config(self):
        self.load()
        path = str(Path(self.home) / '.britive' / 'config')  # handle os specific separators properly
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
        self.load(force=True)

        return npm_config.get('envProfileMap', {})

    def backend(self):
        self.load()
        return self.config.get('global', {}).get('credential_backend', 'encrypted-file')

    def update(self, section, field, value):
        self.load()
        if section not in self.config.keys():
            self.config[section] = {}
        if field not in self.config[section].keys():
            self.config[section][field] = ''
        self.config[section][field] = value
        self.save()

    def validate(self):
        self.validation_error_messages = []

        for section, fields in self.config.items():
            if section not in non_tenant_sections and not section.startswith('tenant-'):
                self.validation_error_messages.append(f'Invalid section {section} provided.')
            if section == 'global':
                self.validate_global(section, fields)
            if section == 'profile-aliases':
                self.validate_profile_aliases(section, fields)
            if section.startswith('tenant-'):
                self.validate_tenant(section, fields)

        if len(self.validation_error_messages) > 0:
            message = 'Cannot save config file due to invalid data provided. Details below.'
            errors = [message] + [f'* {m}' for m in self.validation_error_messages]
            raise click.ClickException('\n'.join(errors))

    def validate_global(self, section, fields):
        for field, value in fields.items():
            if field not in global_fields:
                self.validation_error_messages.append(f'Invalid {section} field {field} provided.')
            if field == 'output_format' and value not in output_format_choices.choices:
                error = f'Invalid {section} field {field} value {value} provided. Invalid value choice.'
                self.validation_error_messages.append(error)
            if field == 'credential_backend' and value not in backend_choices.choices:
                error = f'Invalid {section} field {field} value {value} provided. Invalid value choice.'
                self.validation_error_messages.append(error)
            if field == 'auto-refresh-profile-cache' and value not in ['true', 'false']:
                error = f'Invalid {section} field {field} value {value} provided. Invalid value choice.'
                self.validation_error_messages.append(error)
            if field == 'default_tenant':
                tenant_aliases_from_sections = [
                    extract_tenant(t) for t in self.config.keys() if t.startswith('tenant-')
                ]
                if value not in tenant_aliases_from_sections:
                    error = f'Invalid {section} field {field} value {value} provided. Tenant not found.'
                    self.validation_error_messages.append(error)

    def validate_profile_aliases(self, section, fields):
        for field, value in fields.items():
            if len(value.split('/')) != 3:
                error = f'Invalid {section} field {field} value {value} provided. Value must be 3 parts ' \
                        'separated by a /'
                self.validation_error_messages.append(error)

    def validate_tenant(self, section, fields):
        for field, value in fields.items():
            if field not in tenant_fields:
                self.validation_error_messages.append(f'Invalid {section} field {field} provided.')
            if field == 'output_format' and value not in output_format_choices.choices:
                error = f'Invalid {section} field {field} value {value} provided. Invalid value choice.'
                self.validation_error_messages.append(error)
            if field == 'name' and 'britive-app.com' in value:
                error = f'Invalid {section} field {field} value {value} provided. Tenant name cannot include ' \
                        'britive-app.com'
                self.validation_error_messages.append(error)

    def auto_refresh_profile_cache(self):
        self.load()
        value = self.config.get('global', {}).get('auto-refresh-profile-cache', 'false')
        if value == 'true':
            return True
        return False
