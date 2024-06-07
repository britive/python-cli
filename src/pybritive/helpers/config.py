import configparser
import json
import os
from pathlib import Path
import shutil
import toml
from britive.britive import Britive
import click
from ..choices.backend import backend_choices
from ..choices.mode import mode_choices
from ..choices.output_format import output_format_choices
from ..helpers.split import profile_split


def extract_tenant(tenant_key):
    return tenant_key.replace('tenant-', '')


def lowercase(obj):
    """Make dictionary lowercase"""
    if isinstance(obj, dict):
        return {k.lower(): lowercase(v) for k, v in obj.items()}
    if isinstance(obj, (list, set, tuple)):
        t = type(obj)
        return t(lowercase(o) for o in obj)
    if isinstance(obj, str):
        return obj.lower()
    return obj


def coalesce(*arg):
    for el in arg:
        if el is not None:
            return el
    return None


non_tenant_sections = ['global', 'profile-aliases', 'aws', 'gcp']

global_fields = [
    'default_tenant',
    'output_format',
    'credential_backend',
    'auto-refresh-profile-cache',
    'auto-refresh-kube-config',
    'ca_bundle',
]

tenant_fields = ['name', 'output_format', 'sso_idp']

aws_fields = ['default_checkout_mode']

gcp_fields = ['gcloud_default_account']


class ConfigManager:
    def __init__(self, cli: object, tenant_name: str = None):
        self.tenant_name = tenant_name
        self.home = os.getenv('PYBRITIVE_HOME_DIR', str(Path.home()))
        self.base_path = str(Path(self.home) / '.britive')
        self.path = str(Path(self.base_path) / 'pybritive.config')
        self.config = None
        self.alias = None
        self.default_tenant = None
        self.tenants = None
        self.tenants_by_name = None
        self.aliases_and_names = None
        self.profile_aliases = {}
        self.cli: object = cli
        self.loaded = False
        self.validation_error_messages = []
        self.gcloud_key_file_path: str = str(Path(self.path).parent / 'pybritive-gcloud-key-files')
        self.global_ca_bundle = None

    def clear_gcloud_auth_key_files(self, profile=None):
        path = Path(self.gcloud_key_file_path)
        if profile:  # if we are given a specific profile we should clear just that key file
            key_file = self.cli.build_gcloud_key_file_for_gcloudauthexec(profile=profile)
            path = path / key_file

            # path.unlink(missing_ok=True)
            # removed for now, for 3.7 compatability
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        else:  # otherwise we can remove all items in the directory and the directory itself
            shutil.rmtree(str(path), ignore_errors=True)

    def get_output_format(self, output_format: str = None):
        return coalesce(
            output_format,
            self.get_tenant().get('output_format'),
            self.config.get('global', {}).get('output_format'),
            'json',  # set to json if no output format is provided
        )

    def load(self, force=False):
        if self.loaded and not force:
            return
        path = Path(self.path)

        if not path.is_file():  # config file does not yet exist, create it as an empty file
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text('', encoding='utf-8')

        config = configparser.ConfigParser()
        config.optionxform = str  # maintain key case
        config.read(str(path))
        config = json.loads(json.dumps(config._sections))  # TODO this is messy but works for now

        self.config = lowercase(config)
        self.alias = None  # will be set in self.get_tenant()
        self.default_tenant = self.config.get('global', {}).get('default_tenant')
        self.tenants = {}
        self.tenants_by_name = {}
        for key in self.config:
            if key.startswith('tenant-'):
                alias = extract_tenant(key)
                item = {**self.config[key], **{'alias': alias}}
                self.tenants[alias] = item

                name = self.config[key].get('name', alias)
                if name != alias:
                    self.tenants_by_name[name] = item
        self.aliases_and_names = {**self.tenants, **self.tenants_by_name}
        self.profile_aliases = self.config.get('profile-aliases', {})
        self.global_ca_bundle = self.config.get('ca_bundle', {})
        self.loaded = True

    def get_tenant(self):
        # load up the config - doing it here instead of __init__ for the configure commands since config won't
        # yet exist and we don't want to error
        self.load()  # will set self.config and other variables

        # normalize the input
        name = self.tenant_name.lower() if self.tenant_name else None

        # do some error checking to ensure we can actually grab a tenant
        if len(self.tenants) == 0 and not name:
            raise click.ClickException(f'No tenants found in {self.path}. Cannot continue.')

        # attempt to determine the name of the tenant based on what the user passed in (or didn't pass in)
        provided_tenant_name = name if name else self.default_tenant

        if not provided_tenant_name:  # name not provided and no default has been set
            if len(self.tenants) != 1:
                raise click.ClickException(
                    'Tenant not provided, no default tenant set, and more than one tenant exists.'
                )
            # nothing given but only 1 tenant so assume that is what should be used
            provided_tenant_name = list(self.tenants)[0]

        # if we get here then we now have a tenant name we can check to ensure exists
        if provided_tenant_name not in self.aliases_and_names and not name:
            raise click.ClickException(f'Tenant name "{provided_tenant_name}" not found in {self.path}')

        self.alias = provided_tenant_name or name
        # return details about the requested tenant
        return self.aliases_and_names.get(provided_tenant_name, {'name': name, 'alias': name})

    def save(self):
        self.validate()  # ensure we are actually writing a valid config
        config = configparser.ConfigParser()
        config.optionxform = str  # maintain key case
        config.read_dict(self.config)

        # write the new credentials file
        with open(str(self.path), 'w', encoding='utf-8') as f:
            config.write(f, space_around_delimiters=False)

    def save_tenant(self, tenant: str, alias: str = None, output_format: str = None):
        self.load()
        if not alias:
            alias = tenant
        if f'tenant-{alias}' not in self.config:
            self.config[f'tenant-{alias}'] = {}
        self.config[f'tenant-{alias}']['name'] = tenant
        if output_format:
            self.config[f'tenant-{alias}']['output_format'] = output_format
        self.save()

    def save_global(self, default_tenant_name: str = None, output_format: str = None, backend: str = None):
        self.load()
        if not default_tenant_name and not output_format and not backend:
            return
        if 'global' not in self.config:
            self.config['global'] = {}
        if default_tenant_name:
            self.config['global']['default_tenant'] = default_tenant_name
        if output_format:
            self.config['global']['output_format'] = output_format
        if backend:
            self.config['global']['credential_backend'] = backend
        self.save()

    def get_profile_aliases(self, reverse_keys: bool = False):
        self.load()
        aliases = self.config.get('profile-aliases', {})
        if reverse_keys:
            return {v: k for k, v in aliases.items()}
        else:
            return aliases

    def save_profile_alias(self, alias, profile):
        self.profile_aliases[alias] = profile
        self.config['profile-aliases'] = self.profile_aliases
        self.save()

    # returns a dict of profile aliases that need to be created after listing profiles
    def import_global_npm_config(self):
        self.load()
        path = str(Path(self.home) / '.britive' / 'config')  # handle os specific separators properly
        with open(path, 'r', encoding='utf-8') as f:
            npm_config = toml.load(f)
        tenant = npm_config.get('tenantURL', '').replace('https://', '').replace('.britive-app.com', '').lower()
        output_format = npm_config.get('output_format', '').lower()
        aws_section = npm_config.get('AWS', None)

        # reset the config as we are building a new one
        self.config = {'global': {}}
        if tenant != '':
            self.cli.print(f'Found tenant {tenant}.')
            self.config['global']['default_tenant'] = tenant
            self.config[f'tenant-{tenant}'] = {'name': tenant}
        if output_format != '':
            self.cli.print(f'Found default output format {output_format}.')
            self.config['global']['output_format'] = output_format

        if aws_section:
            checkout_mode = aws_section.get('checkoutMode')
            if checkout_mode:
                checkout_mode = checkout_mode.lower().replace('display', '')
                self.cli.print(f'Found aws default checkout mode of {checkout_mode}.')
                self.config['aws'] = {'default_checkout_mode': checkout_mode}

        self.save()
        self.load(force=True)

        return npm_config.get('envProfileMap', {})

    def backend(self):
        self.load()
        return self.config.get('global', {}).get('credential_backend', 'encrypted-file')

    def aws_default_checkout_mode(self):
        self.load()
        return self.config.get('aws', {}).get('default_checkout_mode', None)

    def gcloud_default_account(self):
        self.load()
        return self.config.get('gcp', {}).get('gcloud_default_account', None)

    def update(self, section, field, value):
        self.load()
        if section not in self.config:
            self.config[section] = {}
        if field not in self.config[section]:
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
            if section == 'aws':
                self.validate_aws(section, fields)
            if section == 'gcp':
                self.validate_gcp(section, fields)
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
            if field == 'auto-refresh-kube-config' and value not in ['true', 'false']:
                error = f'Invalid {section} field {field} value {value} provided. Invalid value choice.'
                self.validation_error_messages.append(error)
            if field == 'default_tenant':
                tenant_aliases_from_sections = [extract_tenant(t) for t in self.config if t.startswith('tenant-')]
                if value not in tenant_aliases_from_sections:
                    error = f'Invalid {section} field {field} value {value} provided. Tenant not found.'
                    self.validation_error_messages.append(error)
            if field == 'ca_bundle':
                ca_bundle_file_path = Path(value).expanduser()
                if not Path.is_file(ca_bundle_file_path):
                    error = f'Invalid {field} file {ca_bundle_file_path}. File does not exist.'
                    self.validation_error_messages.append(error)

    def validate_profile_aliases(self, section, fields):
        for field, value in fields.items():
            if len(profile_split(value)) not in [2, 3]:
                error = (
                    f'Invalid {section} field {field} value {value} provided. Value must be 2 or 3 parts '
                    'separated by a /'
                )
                self.validation_error_messages.append(error)

    def validate_aws(self, section, fields):
        for field, value in fields.items():
            if field not in aws_fields:
                self.validation_error_messages.append(f'Invalid {section} field {field} provided.')
            if field == 'default_checkout_mode' and value not in mode_choices.choices:
                error = f'Invalid {section} field {field} value {value} provided. Invalid value choice.'
                self.validation_error_messages.append(error)

    def validate_gcp(self, section, fields):
        for field, value in fields.items():
            if field not in gcp_fields:
                self.validation_error_messages.append(f'Invalid {section} field {field} provided.')

    def validate_tenant(self, section, fields):
        for field, value in fields.items():
            if field not in tenant_fields:
                self.validation_error_messages.append(f'Invalid {section} field {field} provided.')
            if field == 'name':
                try:
                    Britive.parse_tenant(value)
                except Exception as e:
                    raise click.ClickException(f'Error validating tenant name: {str(e)}')
            if field == 'output_format' and value not in output_format_choices.choices:
                error = f'Invalid {section} field {field} value {value} provided. Invalid value choice.'
                self.validation_error_messages.append(error)

    def auto_refresh_profile_cache(self):
        self.load()
        value = self.config.get('global', {}).get('auto-refresh-profile-cache', 'false')
        if value == 'true':
            return True
        return False

    def auto_refresh_kube_config(self):
        self.load()
        value = self.config.get('global', {}).get('auto-refresh-kube-config', 'false')
        if value == 'true':
            return True
        return False
