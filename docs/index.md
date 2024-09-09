# Welcome to PyBritive

For full documentation visit [docs.britive.com](https://docs.britive.com).

PyBritive is intended to be used as a CLI application for communicating with the Britive Platform.

## Requirements

* Python 3.8 or higher
* Active Britive tenant (or nothing is really going to work)

## Installation

`pybritive` will be installed via Python `pip`.

```sh
pip install pybritive
```

Or you can always pull the latest version directly from GitHub using one of the following commands.

```sh
pip install $(curl -s https://api.github.com/repos/britive/python-cli/releases/latest \
    | jq -r '.assets[] | select(.content_type == "application/x-gzip") | .browser_download_url')
```

OR

```sh
pip install $(curl -s https://api.github.com/repos/britive/python-cli/releases/latest \
    | grep "browser_download_url.*.tar.gz" | cut -d : -f 2,3 | tr -d \")
```

The end user is free to install the CLI into a virtual environment or in the global scope, so it is available
everywhere.

If the `pybritive` executable is not found when attempting to invoke the program, you may need to add the location
of the `pybritive` executable to your path. This location can differ by OS and whether you are using a virtualenv or
not. The easiest way to see where executables get installed via `pip install ...` is to run the following command.

```sh
echo `python3 -m site --user-base`/bin
```

You will need to add this location to your path. The following command will do that but it is recommended to add
this command into your `.bashrc, .zshrc, etc.` file, so it will always get executed on new terminal windows.

```sh
export PATH=`python3 -m site --user-base`/bin:$PATH
```

### Proxies

Under the covers, python [`requests`](https://github.com/psf/requests) is being used to communicate with the Britive API.
As such, any functionality of `requests` can be used, including setting an HTTP proxy.

* HTTP proxies will be set via environment variables.
  * `HTTP_PROXY`
  * `HTTPS_PROXY`
  * `NO_PROXY`
  * `http_proxy`
  * `https_proxy`
  * `no_proxy`

> _Standard HTTP proxy URLs should be utilized._
>
> _Examples:_
>
> * _Unauthenticated Proxy: `http://internalproxy.domain.com:8080`_
> * _Authenticated Proxy: `http://user:pass@internalproxy.domain.com:8080`_

### Custom TLS Certificates

This can be set in the `pybritive.config` `global` settings by setting `ca_bundle`, e.g.:

```toml
[global]
default_tenant=tenant
output_format=json
credential_backend=file
# replace "/location/of/the/CA_BUNDLE_FILE.pem" with the path to the desired CA bundle file
ca_bundle=/location/of/the/CA_BUNDLE_FILE.pem
```

Setting custom TLS certificates functionality of `requests` can also be used.

* Certificate bundles will be set via environment variables.
  * `REQUESTS_CA_BUNDLE`
  * `CURL_CA_BUNDLE` _(used as a fallback)_

> _The values of these environment variables must be a path to a directory of certificates or a specific certificate._
>
> _Example:_
> _`/path/to/certfile`_

#### Examples

__linux/macos:__

```sh
export REQUESTS_CA_BUNDLE="/usr/local/corp-proxy/cacert.pem"
```

__windows (powershell):__

```pwsh
$env:REQUESTS_CA_BUNDLE = "C:\Users\User\AppData\Local\corp-proxy\cacert.pem"
```

__windows (cmd):__

```bat
set REQUESTS_CA_BUNDLE="C:\Users\User\AppData\Local\corp-proxy\cacert.pem"
```

## Tenant Configuration

Before `pybritive` can connect to a Britive tenant, it needs to know some details about that tenant.
This is where `pybritive configure` will help us.

There are 2 ways to tell `pybritive` about tenants.

1. `pybritive configure import`: this will import an existing configuration from the Node.js version of the Britive CLI.
2. `pybritive configure tenant`: This will prompt (or optionally the values can be passed via flags) for tenant details.

An alias for a tenant can be created in case more than 1 tenant is configured for use. This may be the case for admins
who may have access to an EA and GA tenant.

## Tenant Selection Logic

Given the URL `https://example.britive-app.com` used to access your Britive tenant, tenant value can be provided in a
number of formats.

1. `example`
2. `example.britive-app.com`
3. `https://example.britive-app.com`

There are numerous ways to provide the CLI with the Britive tenant that should be used. The below list is the
order of operations for determining the tenant.

1. Value retrieved from CLI option/flag `--tenant/-t`
2. Value retrieved from environment variable `BRITIVE_TENANT`
3. Value retrieved from `~/.britive/pybritive.config` global variable `default_tenant`
4. If none of the above are available then check for configured tenants in `~/.britive/pybritive.config` and if there is
only 1 tenant configured use it
5. If all the above fail then error

## Credential Selection Logic

There are numerous ways to provide the CLI with the Britive credentials that should be used to authenticate to the
Britive tenant. The below list is the order of operations for determining the token to use.

1. Workload federation provider token via option/flag `--federation-provider/-P`
   * see below for more details on this option
2. Value retrieved from CLI option/flag `--token/-T`
3. Value retrieved from environment variable `BRITIVE_API_TOKEN`
4. If none of the above are available an interactive login will be performed and temporary credentials will be stored
locally for future use with the CLI

## `PROFILE` Parameter Construction (`checkout` and `checkin`)

The general construction of a `PROFILE` parameter for `checkout` and `checkin` (in addition to profile aliases)
is in the format `Application Name/Environment Name/Profile Name`.

Behind the scenes `pybritive` will always use this format. However, there are specific application types where
`Application Name == Environment Name`. For these application types, it is acceptable to provide a 2 part `PROFILE`
parameter in the format `Application Name/Profile Name`. `pybritive` will convert this to the required 3 part
format before interacting with backend services.

Additionally, `ls profiles -f list` and `cache profiles` will return the 2 part format where applicable. It is still
acceptable to provide the 3 part format in all cases so any existing profile aliases or other configurations will not be
impacted.

Below is the list of application types in which a 2 part format is acceptable.

* GCP
* Azure
* Oracle
* Google Workspace

The list can be generated (assuming the caller has the required permissions) on demand with the following command.

```sh
pybritive api applications.catalog \
    --query '[*].{"application type": name,"2 part format allowed":requiresHierarchicalModel}' \
    --format table
```

Additionally, the `Environment Name` can be any one of three values. AWS example values are provided.

* `environmentId` - 123456789012
* `environmentName` - 123456789012 (Sigma Labs)
* `alternateEnvironmentName` - Sigma Labs

Any of the above values in the `Environment Name` position will be accepted.

When running `ls profiles -f list` and `cache profiles`, the `environmentName` field will be shown.

## Workload Federation Providers

> _NOTE:_ Before any of the below will work there is required setup and configuration within your Britive tenant
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
* Azure System Assigned Managed Identities
* Azure User Assigned Managed Identities
* Spacelift.io

For more information on [Azure Managed Identities reference](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview 'Link to Microsoft Documentaion')

It is possible to source an identity token from a different OIDC provider and explicitly set it via the `--token\-T`
flag. However, if you are using one of the above providers, a shortcut is provided to abstract away the complexity of
sourcing these tokens. Over time this list will grow. Reach out to your customer success manager if you have an identity
provider you would like added to this list.

### IdP examples

A couple of examples are below which illustrate how to use the above identity providers.

> _NOTE:_ these commands will only work if they are being run within the context of the identity provider. Otherwise,
the necessary data and connections will not be present in the execution environment.

#### GitHub Actions

```sh
# use github actions with the default OIDC audience
pybritive checkout "profile" --federation-provider github

# use github actions with a custom OIDC audience
pybritive checkout "profile" --federation-provider github-audience

# use github actions with a custom OIDC audience and set the Britive expiration (in seconds) of the generated token
pybritive checkout "profile" --federation-provider github-audience_expirationseconds

# use github actions with the default OIDC audience and set the Britive expiration (in seconds) of the generated token
pybritive checkout "profile" --federation-provider github_expirationseconds
```

#### AWS STS

```sh
# use aws sts without an AWS CLI profile (source credentials via the standard credential discovery process)
pybritive checkout "profile" --federation-provider aws

# use aws sts with an AWS CLI profile
pybritive checkout "profile" --federation-provider aws-profile

# use aws sts with an AWS CLI profile and set the Britive expiration (in seconds) of the generated token
pybritive checkout "profile" --federation-provider aws-profile_expirationseconds

# use aws sts without an AWS CLI profile and set the Britive expiration (in seconds) of the generated token
pybritive checkout "profile" --federation-provider aws_expirationseconds
```

#### Bitbucket

> _note: no additional options are available for bitbucket._

```sh
pybritive checkout "profile" --federation-provider bitbucket
```

#### spacelift.io

> _note: no additional options are available for spacelift.io._

```sh
pybritive checkout "profile" --federation-provider spacelift
```

#### Azure system assigned managed identities

```sh
# use system assigned managed identities with...

## the default OIDC audience
pybritive checkout "profile" --federation-provider azuresmi

## a custom OIDC audience
pybritive checkout "profile" --federation-provider azuresmi-audience

## a custom OIDC audience and set the Britive expiration (in seconds) of the generated token
pybritive checkout "profile" --federation-provider azuresmi-audience_expirationseconds

## the default OIDC audience and set the Britive expiration (in seconds) of the generated token
pybritive checkout "profile" --federation-provider azuresmi_expirationseconds
```

#### Azure user assigned managed identities

> _note: a client id is a required field._

```sh
# use user assigned managed identities with...

## the default OIDC audience
pybritive checkout "profile" --federation-provider azuresmi-clientid

## a custom OIDC audience
pybritive checkout "profile" --federation-provider azuresmi-clientid|audience

## a custom OIDC audience and set the Britive expiration (in seconds) of the generated token
pybritive checkout "profile" --federation-provider azuresmi-clientid|audience_expirationseconds

## the default OIDC audience and set the Britive expiration (in seconds) of the generated token
pybritive checkout "profile" --federation-provider azuresmi-clientid_expirationseconds
```

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
provided `pybritive` will use an internally generated passphrase unique to the machine on which the application is
running.

## Home Directory

By default, files that `pybritive` requires will be persisted to `~/.britive/`.

This can be overwritten by specifying environment variable `PYBRITIVE_HOME_DIR`. This can be either one of the following
choices to where the end user wants to persist the `.britive` directory. Note that `.britive` will still be created so
do not specify that as part of the path.

## Browser

By default, `pybritive` will use the OS defined default for any actions that have browser interaction(s).

This can be overwritten by specifying environment variable `PYBRITIVE_BROWSER`. This can either be a one of the choices
listed for commands that have the `--browser` option/flag, or can be set to an open command for browsers not provided by
the Python3 `webbrowser` module.

Example:

```sh
export PYBRITIVE_BROWSER="open -a /Applications/Firefox\ Developer\ Edition.app %s"
```

Note that as of Britive release `2023.11.01` the CLI authentication flow will NOT prompt to login if the user is already
authenticated in the browser. However, this is only true if the browser launched by `pybritive` is the same browser
where the user is already authenticated.

## Escaping

If the name of an application, environment, or profile contains a `/` then that character must be properly escaped with
a `\`.

Example:
* Application: AWS
* Environment: Dev/Test
* Profile: Admin

As we construct the checkout command it would generally be `AWS/Dev/Test/Admin` but since the environment has a `/`
in it, we need to escape that to be `AWS/Dev\/Test/Admin` so the CLI can properly parse out the 3 required parts of the
string.

This holds true for names of secrets and any other free form text that may be submitted via the CLI. Ensure you are
escaping all required characters based on the shell you are using.

## `api` Command - Use the Britive Python SDK via the CLI

As of v0.11.0 a new command called `api` has been introduced. This command exposes the full capability of the Britive
Python SDK to users of the `pybritive` CLI.

Documentation on each SDK method can be found inside the Python SDK itself and on Github
(https://github.com/britive/python-sdk). The Python package `britive` is a dependency of the CLI
already so the SDK is available without installing any extra packages.

It is left up to the caller to provide the proper `method` and `parameters` based on the documentation
of the API call being performed. Examples will follow which explain how to do this.

The authenticated identity must have the appropriate permissions to perform the actions being requested.
General end users of Britive will not have these permissions. This call (and the larger SDK) is generally
meant for administrative functionality.

### `api` examples

Usage examples of: (`pybritive api method --parameter1 value1 --parameter2 value2 [--parameterX valueX]`)

```sh
# list all users in the britive tenant
pybritive api users.list

# create a tag
pybritive api tags.create --name testtag --description "test tag"

# list all users and output just the email address of each user via jmespath query
pybritive api users.list --query '[].email'

# create a profile
pybritive api profiles.create --application-id <id> --name testprofile

# create a secret
pybritive api secrets_manager.secrets.create --name test --vault-id <id> --value '{"Note": {"secret1": "abc"}}'

# create a file secret
pybritive api secrets_manager.secrets.create --name test-file --vault-id <id> --file fileb://test.json \
    --static-secret-template-id <id> --value None
```

* The `method` is the same pattern as what would be used when referencing an instance of the `Britive` class.
* The `parameters` are dynamic based on the method being invoked. Review the documentation for the method in question to
understand which parameters are expected and which are optional. Parameters with `_` in the name should be translated to
`-` when referencing them via the CLI.

## `ssh` Command

The `ssh` command facilitates using the native SSH protocol to connect to private cloud servers.

The goal is to allow all functionality offered by the SSH protocol like local port forwarding to access private
resources and `scp` to copy files to the remote host.

AWS and GCP are supported.

### AWS

The requirements for using SSH with EC2 instances are provided below.

* EC2 instance must have the Systems Manager agent installed and operational.
* EC2 instance must have the EC2 Instance Connect agent installed and operational (if using `--push-public-key`).
* The caller must have appropriate IAM permissions to start a Session Manager session (for all `--key-source`s) and push
a public key via EC2 Instance Connect (if using `--push-public-key`).
* The caller's environment must have the AWS CLI installed along with the Session Manager plugin.
* The caller's python environment must have the `boto3` package installed. As `boto3` is not required for the use of
`pybritive` it is not automatically installed (if using `--push-public-key`).
* The caller must use OpenSSH (and the SSH config file). Other SSH implementations are not currently supported.

There are 3 ways that `pybritive` can help proxy an SSH session to a private EC2 instance.

* Using just Session Manager SSH forwarding to establish the network path over which the SSH protocol will operate. It
is left to the caller then to handle SSH authentication using whichever mechanism has already been established.

```sh
Host bastion.dev
     HostName i-xxxxxxxxxxxxxxxxx.profile[.region]
     
Match host i-*,mi-*
    User ssm-user
    ProxyCommand eval $(pybritive ssh aws ssm-proxy --hostname %h --username %r --port-number %p)
```

* Using Session Manager SSH forwarding along with pushing a randomly generated SSH key pair public key via EC2 Instance
Connect and identifying the private key via static path in the `IdentityFile` parameter.

```sh
Host bastion.dev
     HostName i-xxxxxxxxxxxxxxxxx.profile[.region]
     
Match host i-*,mi-*
    User ssm-user
    IdentityFile ~/.britive/ssh/%h.%r.pem
    ProxyCommand eval $(pybritive ssh aws ssm-proxy \
        --hostname %h \
        --username %r \
        --port-number %p \
        --push-pulbic-key \
        --key-source static)
```

* Using Session Manager SSH forwarding along with pushing a randomly generated SSH key pair public key via EC2 Instance
Connect and adding the private key to the `ssh-agent` via `ssh-add` so it is available without having to specify the
`IdentityFile` parameter.

```sh
Host bastion.dev
     HostName i-xxxxxxxxxxxxxxxxx.profile[.region]
     
Match host i-*,mi-*
    User ssm-user
    ProxyCommand eval $(pybritive ssh aws ssm-proxy \
        --hostname %h \
        --username %r \
        --port-number %p \
        --push-pulbic-key \
        --key-source ssh-agent)
```

The `HostName` parameter must be in the appropriate format. That format is

```sh
[instance-id][.aws-profile-name[.aws-region]]
```

Both `aws-profile-name` and `aws-region` are optional. If `aws-profile-name` is omitted then credentials for Session
Manager and EC2 Instance Connect will be sourced from the standard AWS credential provider chain.
If `aws-region` is omitted then credentials for Session Manager and EC2 Instance Connect will be sourced from the
standard AWS region provider chain.

The command `ssh aws config` can be invoked to generate the above `Match` directives.

### GCP

The requirements for using SSH with GCP compute engine instances are provided below.

* `gcloud` CLI must be installed in the environment and `gcloud auth login` already performed.
* Instance must accept SSH key from either [OS Login](https://cloud.google.com/compute/docs/oslogin/set-up-oslogin)
  * or [SSH Instance Metadata](https://cloud.google.com/compute/docs/connect/add-ssh-keys#metadata)
  (if using `--push-public-key`).
* If using OS Login two-factor authentication cannot be enabled.
* The caller must have appropriate permissions to use identity aware proxy (for all `--key-source`s) and push a public
key via OS Login or SSH Instance Metadata (if using `--push-public-key`).
* The caller's environment must have the `gcloud` cli installed and `gcloud auth login` already performed.
* The caller must use OpenSSH (and the SSH config file). Other SSH implementations are not currently supported.

There are 3 ways that `pybritive` can help proxy an SSH session to a private compute instance.

* Using just Identity Aware Proxy (IAP) SSH forwarding to establish the network path over which the SSH protocol will
operate. It is left to the caller then to handle SSH authentication using whichever mechanism has already been
established.

```sh
Host bastion.dev
     HostName gcp.instance-name.project-id
     
Match host gcp.*
    User username
    ProxyCommand eval $(pybritive ssh gcp identity-aware-proxy --hostname %h --username %r --port-number %p)
```

* Using IAP SSH forwarding along with pushing a randomly generated SSH key pair public key via OS Login or Instance
Metadata and identifying the private key via static path in the `IdentityFile` parameter.

Using OS Login...

```sh
Host bastion.dev
     HostName gcp.instance-name.project-id
     
Match host gcp.*
    User username
    IdentityFile ~/.britive/ssh/%h.%r.pem
    ProxyCommand eval $(pybritive ssh gcp identity-aware-proxy \
        --hostname %h \
        --username %r \
        --port-number %p \
        --push-pulbic-key os-login \
        --key-source static)
```

Using Instance Metadata...

```sh
Host bastion.dev
     HostName gcp.instance-name.project-id
     
Match host gcp.*
    User username
    IdentityFile ~/.britive/ssh/%h.%r.pem
    ProxyCommand eval $(pybritive ssh gcp identity-aware-proxy \
        --hostname %h \
        --username %r \
        --port-number %p \
        --push-pulbic-key instance-metadata \
        --key-source static)
```

* Using IAP SSH forwarding along with pushing a randomly generated SSH key pair public key via OS Login or Instance
Metadata and adding the private key to the `ssh-agent` via `ssh-add` so it is available without having to specify the
`IdentityFile` parameter.

Using OS Login...

```sh
Host bastion.dev
     HostName gcp.instance-name.project-id
     
Match host gcp.*
    User username
    ProxyCommand eval $(pybritive ssh gcp identity-aware-proxy \
        --hostname %h \
        --username %r \
        --port-number %p \
        --push-pulbic-key os-login \
        --key-source ssh-agent)
```

Using Instance Metadata...

```sh
Host bastion.dev
     HostName gcp.instance-name.project-id
     
Match host gcp.*
    User username
    ProxyCommand eval $(pybritive ssh gcp identity-aware-proxy \
        --hostname %h \
        --username %r \
        --port-number %p \
        --push-pulbic-key instance-metadata \
        --key-source ssh-agent)
```

The `HostName` parameter must be in the appropriate format. That format is

```sh
gcp.<instance name>.<project id>
```

The command `ssh gcp config` can be invoked to generate the above `Match` directives.

## `aws` Command

The `aws` command group will hold actions related specifically to AWS.

The first supported sub-command is `console` which will sign an AWS console URL using programmatic access keys
(long-lived IAM User keys or temporary AWS AssumeRole credentials). This will allow you to check out programmatic access
for a Britive AWS profile (or any other system which issues AWS access keys) and use the resulting keys to get into the
AWS console.

## Shell Completion

> _TODO: Provide more automated scripts here to automatically add the required configs to the profiles._
> _For now the below works just fine though._

Behind the scenes the `pybritive` CLI tool uses the python `click` package. `click` offers shell completion for
the following shells.

* `bash`
* `zsh`
* `fish`

A shell completion script has been written for the following shells as well.

* PowerShell

In order to set up shell completion, follow these steps. Once complete either `source` your environment again
or start a new shell in order for the changes to be loaded.

### Bash

Save the completion script somewhere.

```sh
_PYBRITIVE_COMPLETE=bash_source pybritive > ~/.pybritive-complete.bash
```

Source the file in `~/.bashrc`.

```sh
source ~/.pybritive-complete.bash
```

### Zsh

Save the completion script somewhere.

```sh
_PYBRITIVE_COMPLETE=zsh_source pybritive > ~/.pybritive-complete.zsh
```

Source the file in `~/.zshrc`.

```sh
source ~/.pybritive-complete.zsh
```

### Fish

Save the completion script to the `fish` completions directory.

```sh
_PYBRITIVE_COMPLETE=fish_source pybritive > ~/.config/fish/completions/pybritive.fish
```

### PowerShell

Append the below code to your PowerShell profile.

```ps
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
```

The location of your PowerShell profile can be found with command

```sh
echo $profile
```

And is generally something like `C:\Users\{user}\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`.
Create the file (and any needed directories) if needed.

### Shell Completion - Profiles - Local Cache

By default, shell completion only completes commands and options/flags as those values are available without
any authentication to a Britive tenant.

There is an option to enable shell completion for profiles and profile aliases for use with `checkout` and `checkin`.

In order enable this, run the following command.

```sh
pybritive cache profiles
```

This will locally cache profiles for which the authenticated user has permissions. If multiple tenants are being used
then each tenant will need to be cached individually. All profiles across all tenants will be available during shell
completion (this is due to the fact the completion logic doesn't have any context as to which tenant is being used
as the tenant may not be provided yet).

The cache will not be updated over time. In order to update the cache more regularly run the following command.
Note that this config flag is NOT available directly via `pybritive configure global ...`.

```sh
pybritive configure update global auto-refresh-profile-cache true
```

To turn the feature off run

```sh
pybritive configure update global auto-refresh-profile-cache false
pybritive cache clear
```

## `pybritive` with the AWS `credential_process`

`pybritive` natively supports the AWS `credential_process` option present in the AWS credentials file.

```toml
[profile-a]
credential_process=pybritive checkout britive-profile-alias -m awscredentialprocess
region=us-east-1
```

As of v0.4.0 a new "side-car" helper script/CLI program has been created. `pybritive-aws-cred-process` provides a
minimal codebase in an effort to reduce the latency of obtaining credentials via the AWS `credential_process` command.

`pybritive-aws-cred-process` reduces the latency of the call by ~50% while still maintaining basic functionality.

```toml
[profile-a]
credential_process=pybritive-aws-cred-process --profile britive-profile-alias
region=us-east-1
```

## Command Documentation

::: mkdocs-click
    :module: pybritive.cli_interface
    :command: cli
    :prog_name: pybritive
    :style: table
    :list_subcommands: True
    :depth: 2
