# Welcome to PyBritive

!!! note
    This is a BETA release. This codebase should not be used for production workloads.

For full documentation visit [docs.britive.com](https://docs.britive.com).

PyBritive is intended to be used as a CLI application for communicating with the Britive Platform.

## Requirements

* Python 3.7 or higher
* Active Britive tenant (or nothing is really going to work)

## Installation

`pybritive` will be installed via Python `pip`. 

~~~bash
pip install pybritive
~~~

Or you can always pull the latest version directly from Github using one of the following commands.

~~~
pip install $(curl -s https://api.github.com/repos/britive/python-cli/releases/latest | jq -r '.assets[] | select(.content_type == "application/x-gzip") | .browser_download_url')

OR

pip install $(curl -s https://api.github.com/repos/britive/python-cli/releases/latest | grep "browser_download_url.*.tar.gz" | cut -d : -f 2,3 | tr -d \")
~~~

The end user is free to install the CLI into a virtual environment or in the global scope, so it is available
everywhere.

## Tenant Configuration

Before `pybritive` can connect to a Britive tenant, it needs to know some details about that tenant.
This is where `pybritive configure` will help us.

There are 2 ways to tell `pybritive` about tenants.

1. `pybritive configure import`: this will import an existing configuration from the Node.js version of the Britive CLI.
2. `pybritive configure tenant`: This will prompt (or optionally the values can be passed via flags) for tenant details.

An alias for a tenant can be created in case more than 1 tenant is configured for use. This may be the case for admins
who may have access to an EA and GA tenant.

## Tenant Selection Logic

Given the URL `https://example.britive-app.com` used to access your Britive tenant, tenant value can be provided in a number of formats.

1. `example`
2. `example.britive-app.com`
3. `https://example.britive-app.com`

There are numerous ways to provide the CLI with the Britive tenant that should be used. The below list is the
order of operations for determining the tenant.

1. Value retrieved from CLI option/flag `--tenant/-t`
2. Value retrieved from environment variable `BRITIVE_TENANT`
3. Value retrieved from `~/.britive/pybritive.config` global variable `default_tenant`
4. If none of the above are available then check for configured tenants in `~/.britive/pybritive.config` and if there is only 1 tenant configured use it
5. If all the above fail then error


## Credential Selection Logic

There are numerous ways to provide the CLI with the Britive credentials that should be used to authenticate to the
Britive tenant. The below list is the order of operations for determining the token to use.

1. Workload federation provider token via option/flag `--federation-provider/-P` (see below for more details on this option)
2. Value retrieved from CLI option/flag `--token/-T`
3. Value retrieved from environment variable `BRITIVE_API_TOKEN`
4. If none of the above are available an interactive login will be performed and temporary credentials will be stored locally for future use with the CLI


## Workload Federation Providers

*NOTE*: Before any of the below will work there is required setup and configuration within your Britive tenant 
so trust can be established between the identity provider and Britive.

`pybritive` and the Python SDK offer the capability to source an ephemeral token from a federation provider. 
This use case is targeted for machines/automated workloads and removes the need to store a long-lived API token 
to interact with Britive. These tokens are mapped to service identities within your Britive tenant.

At feature launch the following types of identity providers are supported for workload identity federation.

* Open ID Connect (OIDC)
* AWS STS

`pybritive` offers some native integrations with the following services.

* Github Actions
* AWS
* Bitbucket

It is possible to source an identity token from a different OIDC provider and explicitly set it via the `--token\-T` flag.
However, if you are using one of the above providers, a shortcut is provided to abstract away the complexity of sourcing these tokens.
Over time this list will grow. Reach out to your customer success manager if you have an identity provider you would like added to
this list.

A couple of examples are below which illustrate how to use the above identity providers. Note that these commands will only work
if they are being run within the context of the identity provider. Otherwise, the necessary data and connections will not be 
present in the execution environment.

~~~bash
# github actions
pybritive checkout "profile" --federation-provider github  # use github actions with the default OIDC audience
pybritive checkout "profile" --federation-provider github-audience  # use github actions with a custom OIDC audience
pybritive checkout "profile" --federation-provider github-audience_expirationseconds   # use github actions with a custom OIDC audience and set the Britive expiration (in seconds) of the generated token
pybritive checkout "profile" --federation-provider github_expirationseconds  # use github actions with the default OIDC audience and set the Britive expiration (in seconds) of the generated token

# aws sts
pybritive checkout "profile" --federation-provider aws  # use aws sts without an AWS CLI profile (source credentials via the standard credential discovery process)
pybritive checkout "profile" --federation-provider aws-profile  # use aws sts with an AWS CLI profile
pybritive checkout "profile" --federation-provider aws-profile_expirationseconds   # use aws sts with an AWS CLI profile and set the Britive expiration (in seconds) of the generated token
pybritive checkout "profile" --federation-provider aws_expirationseconds  # use aws sts without an AWS CLI profile and set the Britive expiration (in seconds) of the generated token

# bitbucket (note that no additional options are available for bitbucket)
pybritive checkout "profile" --federation-provider bitbucket
~~~

In general the field format for `--federation-provider` is `provider-[something provider specific]_[duration in seconds]`.

## Credential Stores

The CLI currently offers two ways in which temporary credentials obtained via interactive login can be stored.
Future enhancements aim to offer other credential storage options.

### File

Credentials will be stored in a plaintext file located at `~/.britive/pybritive.credentials`

### Encrypted File (Default)
Credentials will be stored in an encrypted file located at `~/.britive/pybritive.credentials.encrypted`.

The user will be prompted for a passphrase to use to encrypt the file. The user can also pass in the passphrase
via flag `--passphrase/-p` or via environment variable `PYBRITIVE_ENCRYPTED_CREDENTIAL_PASSPHRASE`. If no passphrase is
provided `pybritive` will use an internally generated passphrase unique to the machine on which the application is running.


## Home Directory
By default, files that `pybritive` requires will be persisted to `~/.britive/`. 

This can be overwritten by specifying environment variable `PYBRITIVE_HOME_DIR`. This should be a path to where
the end user wants to persist the `.britive` directory. Note that `.britive` will still be created so do not specify
that as part of the path.


## Escaping
If the name of an application, environment, or profile contains a `/` then that character must be properly escaped with a `\`.

Example:
* Application: AWS
* Environment: Dev/Test
* Profile: Admin

As we construct the checkout command it would generally be `AWS/Dev/Test/Admin` but since the environment has a `/`
in it, we need to escape that to be `AWS/Dev\/Test/Admin` so the CLI can properly parse out the 3 required parts of the string .

## `api` Command - Use the Britive Python SDK via the CLI

As of v0.11.0 a new command called `api` has been introduced. This command exposes the full capability of the Britive Python SDK
to users of the `pybritive` CLI.

Documentation on each SDK method can be found inside the Python SDK itself and on Github
(https://github.com/britive/python-sdk). The Python package `britive` is a dependency of the CLI
already so the SDK is available without installing any extra packages.

It is left up to the caller to provide the proper `method` and `parameters` based on the documentation
of the API call being performed. Examples will follow which explain how to do this.

The authenticated identity must have the appropriate permissions to perform the actions being requested.
General end users of Britive will not have these permissions. This call (and the larger SDK) is generally
meant for administrative functionality.

Example of use: (`pybritive api method --parameter1 value1 --parameter2 value2 [--parameterX valueX]`)

* `pybritive api users.list` | will list all users in the britive tenant
* `pybritive api tags.create --name testtag --description "test tag"` | will create a tag
* `pybritive api users.list --query '[].email'` | will list all users and output just the email address of each user via jmespath query
* `pybritive api profiles.create --application-id <id> --name testprofile` | will create a profile
* `pybritive api secrets_manager.secrets.create --name test --vault-id <id> --value '{"Note": {"secret1": "abc"}}'` | creates a secret
* `pybritive api secrets_manager.secrets.create --name test-file --vault-id <id> --file fileb://test.json --static-secret-template-id <id> --value None` | creates a file secret


* The `method` is the same pattern as what would be used when referencing an instance of the `Britive` class.
* The `parameters` are dynamic based on the method being invoked. Review the documentation for the method in question to understand
which parameters are expected and which are optional. Parameters with `_` in the name should be translated to `-` when referencing them
via the CLI.

## Shell Completion

TODO: Provide more automated scripts here to automatically add the required configs to the profiles. For now the below works just fine though.

Behind the scenes the `pybritive` CLI tool uses the python `click` package. `click` offers shell completion for
the following shells.

* Bash
* Zsh
* Fish

A shell completion script has been written for the following shells as well.

* PowerShell

In order to set up shell completion, follow these steps. Once complete either `source` your environment again
or start a new shell in order for the changes to be loaded.

### Bash
Save the completion script somewhere.

~~~bash
_PYBRITIVE_COMPLETE=bash_source pybritive > ~/.pybritive-complete.bash
~~~

Source the file in `~/.bashrc`.

~~~
source ~/.pybritive-complete.bash
~~~

### Zsh
Save the completion script somewhere.

~~~bash
_PYBRITIVE_COMPLETE=zsh_source pybritive > ~/.pybritive-complete.zsh
~~~

Source the file in `~/.zshrc`.

~~~
source ~/.pybritive-complete.zsh
~~~

### Fish
Save the completion script to the `fish` completions directory.

~~~bash
_PYBRITIVE_COMPLETE=fish_source pybritive > ~/.config/fish/completions/pybritive.fish
~~~

### PowerShell
Append the below code to your PowerShell profile.

~~~
$pybritive_completion = {
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
    New-Item -Path Env: -Name _PYBRITIVE_COMPLETE -Value "powershell_complete" | Out-Null

    # call pybritive and it will inspect env vars and provide completion results
    Invoke-Expression pybritive -ErrorAction SilentlyContinue | Tee-Object -Var completionResult | Out-Null

    # cleanup environment variables
    Remove-Item Env:\COMP_LINE | Out-Null
    Remove-Item Env:\_PYBRITIVE_COMPLETE | Out-Null

    # get list of completion items
    $items = $completionResult -split '\r?\n'

    $items | ForEach-Object {"$_ "} # trailing space important as completion is "done"
}

# register tab completion
Register-ArgumentCompleter -Native -CommandName pybritive -ScriptBlock $pybritive_completion
~~~


The location of your PowerShell profile can be found with command

~~~bash
echo $profile
~~~

And is generally something like `C:\Users\{user}\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`.
Create the file (and any needed directories) if needed.


### Shell Completion - Profiles - Local Cache

By default, shell completion only completes commands and options/flags as those values are available without
any authentication to a Britive tenant.

There is an option to enable shell completion for profiles and profile aliases for use with `checkout` and `checkin`.

In order enable this, run the following command.

~~~bash
pybritive cache profiles
~~~

This will locally cache profiles for which the authenticated user has permissions. If multiple tenants are being used
then each tenant will need to be cached individually. All profiles across all tenants will be available during shell
completion (this is due to the fact the completion logic doesn't have any context as to which tenant is being used
as the tenant may not be provided yet).

The cache will not be updated over time. In order to update the cache more regularly run the following command.
Note that this config flag is NOT available directly via `pybritive configure global ...`.

~~~bash
pybritive configure update global auto-refresh-profile-cache true
~~~

To turn the feature off run

~~~bash
pybritive configure update global auto-refresh-profile-cache false
pybritive cache clear
~~~

## `pybritive` with the AWS `credential_process`

`pybritive` natively supports the AWS `credential_process` option present in the AWS credentials file.

~~~
[profile-a]
credential_process=pybritive checkout britive-profile-alias -m awscredentialprocess
region=us-east-1
~~~

As of v0.4.0 a new "side-car" helper script/CLI program has been created. `pybritive-aws-cred-process` provides a minimal codebase in an effort 
to reduce the latency of obtaining credentials via the AWS `credential_process` command.

`pybritive-aws-cred-process` reduces the latency of the call by ~50% while still maintaining basic functionality.

~~~
[profile-a]
credential_process=pybritive-aws-cred-process --profile britive-profile-alias
region=us-east-1
~~~

## Command Documentation

::: mkdocs-click
    :module: pybritive.cli_interface
    :command: cli
    :prog_name: pybritive
    :style: table
    :list_subcommands: True
    :depth: 2
