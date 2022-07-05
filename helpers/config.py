from pathlib import Path
import yaml
import click


def lowercase(obj):
    """ Make dictionary lowercase """
    if isinstance(obj, dict):
        return {k.lower():lowercase(v) for k, v in obj.items()}
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
    def __init__(self, tenant_name: str = None, save=False):
        self.tenant_name = tenant_name
        self.path = str(Path.home() / '.pybritive' / 'config.yaml')  # handle os specific separators properly
        self.config = self.load()  # every key/value will have been lowercased by load()

        if not save:  # if we are saving then no need to go through all this logic
            self.alias = None  # will be set in self.get_tenant()
            self.default_tenant = self.config.get('default_tenant')
            self.keys = self.config.keys()
            self.tenants = self.config.get('tenants', {})
            self.selected_tenant = self.get_tenant()

    def get_output_format(self, output_format: str = None):
        return coalesce(
            output_format,
            self.selected_tenant.get('output_format'),
            self.config.get('output_format'),
            'json'  # set to json if no output format is provided
        )

    def load(self):
        path = Path(self.path)

        if not path.is_file():
            return {}

        with open(self.path, 'r') as f:
            try:
                config = yaml.safe_load(f)
                if not config:
                    return {}
                return lowercase(config)  # lowercase keys and values in the config
            except yaml.YAMLError:
                click.echo(f'Invalid YAML file at {self.path}')
                exit()

    def get_tenant(self):
        # normalize the input
        name = self.tenant_name.lower() if self.tenant_name else None

        # do some error checking to ensure we can actually grab a tenant
        if 'tenants' not in self.keys and not name:
            click.echo(f'No "tenants" block found in {self.path}. Cannot continue.')
            exit()

        if len(self.tenants.keys()) == 0 and not name:
            click.echo(f'No tenants found in {self.path}. Cannot continue.')
            exit()

        # attempt to determine the name of the tenant based on what the user passed in (or didn't pass in)
        provided_tenant_name = name if name else self.default_tenant

        if not provided_tenant_name:  # name not provided and no default has been set
            if len(self.tenants.keys()) != 1:
                click.echo('Tenant not provided, no default tenant set, and more than one tenant exists.')
                exit()
            else:
                # nothing given but only 1 tenant so assume that is what should be used
                provided_tenant_name = list(self.tenants.keys())[0]

        # if we get here then we now have a tenant name we can check to ensure exists
        if provided_tenant_name not in self.tenants.keys() and not name:
            click.echo(f'Tenant name "{provided_tenant_name}" not found in {self.path}')
            exit()

        self.alias = provided_tenant_name or name
        # return details about the requested tenant
        return self.tenants.get(provided_tenant_name, {'name': name})

    def save(self):
        with open(self.path, 'w') as f:
            f.write(yaml.safe_dump(self.config))

    def save_tenant(self, tenant: str, alias: str = None, output_format: str = None):
        if 'tenants' not in self.config.keys():
            self.config['tenants'] = {}
        if not alias:
            alias = tenant

        attributes = {'name': tenant}
        if output_format:
            attributes['output_format'] = output_format
        self.config['tenants'][alias] = attributes
        self.save()

    def save_global(self, default_tenant_name: str = None, output_format: str = None):
        if not default_tenant_name and not output_format:
            return
        if default_tenant_name:
            self.config['default_tenant'] = default_tenant_name
        if output_format:
            self.config['output_format'] = output_format
        self.save()
