# Britive CLI - Pure Python Implementation


## Requirements

* Python 3.7 or higher
* Active Britive tenant (or nothing is really going to work)

## Installation

`pybritive` will be installed via Python `pip`. The package is not available in PyPi at this time so it will be 
installed via the published tar balls in the Github repo.

~~~bash
pip install https://github.com/britive/python-cli/releases/download/v1.0.0/pybritive-1.0.0.tar.gz
~~~

The end user is free to install the CLI into a virtual environment or in the global scope so it is available
everywhere.

## Tenant Configuration

Before `pybritive` can connect to a Britive tenant, it needs to know some details about that tenant.
This is where `pybritive configure` will help us.

There are 2 ways to tell `pybritive` about tenants.

1. `pybritive configure import`: this will import an existing configuration from the Node.js version of the Britive CLI.
2. `pybritive configure tenant`: This will prompt (or optionally the values can be passed via flags) for tenant details.

An alias for a tenant can be created in case more than 1 tenant is configured for us. This may be the case for admins
who may have access to an EA and GA tenant.

## Tenant Selection Logic

There are numerous ways to provide the CLI with the Britive tenant that should be used. The below list is the
order of operations for determining the tenant.

The tenant excludes `.britive-app.com`. Just include the leftmost part.
Example: `example.britive-app.com` will have a tenant name in the CLI of `example`.

1. Value retrieved from CLI option/flag `--tenant/-t`
2. Value retrieved from environment variable `BRITIVE_TENANT`
3. Value retrieved from `~/.britive/pybritive.config` global variable `default_tenant`
4. If none of the above are available then check for configured tenants in `~/.britive/pybritive.config` and if there is only 1 tenant configured use it
5. If all the above fail then error


## Credential Selection Logic

There are numerous ways to provide the CLI with the Britive credentials that should be used to authenticate to the
Britive tenant. The below list is the order of operations for determining the tenant.

1. Value retrieved from CLI option/flag `--token/-T`
2. Value retrieved from environment variable `BRITIVE_API_TOKEN`
3. If none of the above are available an interactive login will be performed and temporary credentials will be stored locally for future use with the CLI


## Credential Stores

The CLI currently offers only one way in which temporary credentials obtained via interactive login can be stored.
Future enhancements aim to offer other credential storage options.

### File

Credentials will be stored in a plaintext file located at `~/.britive/pybritive.credentials`

### Encrypted File
Credentials will be stored in an encrypted file located at `~/.britive/pybritive.credentials.encrypted`.

The user will be prompted for a passphrase to use to encrypt the file. The user can also pass in the passphrase
via flag `--passphrase/-p` or via environment variable `PYBRITIVE_ENCRYPTED_CREDENTIAL_PASSPHRASE`.


## Shell Completion
Behind the scenes the `pybritive` CLI tool uses the python `click` package. `click` offers shell completion for
the following shells.

* Bash
* Zsh
* Fish
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
. ~/.pybritive-complete.bash
~~~

### Zsh
Save the completion script somewhere.

~~~bash
_PYBRITIVE_COMPLETE=zsh_source pybritive > ~/.pybritive-complete.zsh
~~~

Source the file in `~/.zshrc`.

~~~
. ~/.pybritive-complete.zsh
~~~

### Fish
Save the completion script to the `fish` completions directory.

~~~bash
_PYBRITIVE_COMPLETE=fish_source pybritive > ~/.config/fish/completions/foo-bar.fish
~~~

### PowerShell
Append the below code to your PowerShell profile.

~~~
if ((Test-Path Function:\TabExpansion) -and -not (Test-Path Function:\pybritiveTabExpansionBackup)) {
    Rename-Item Function:\TabExpansion pybritiveTabExpansionBackup
}

function TabExpansion($line, $lastWord) {
    $lastBlock = [regex]::Split($line, '[|;]')[-1].TrimStart()
    $aliases = @("pybritive") + @(Get-Alias | where { $_.Definition -eq "pybritive" } | select -Exp Name)
    $aliasPattern = "($($aliases -join '|'))"
    if($lastBlock -match "^$aliasPattern ") {
        $Env:_PYBRITIVE_COMPLETE = "complete-powershell"
        $Env:COMMANDLINE = "$lastBlock"
        (pybritive) | ? {$_.trim() -ne "" }
        Remove-Item Env:_PYBRITIVE_COMPLETE
        Remove-Item Env:COMMANDLINE
    }
    elseif (Test-Path Function:\pybritiveTabExpansionBackup) {
        # Fall back on existing tab expansion
        pybritiveTabExpansionBackup $line $lastWord
    }
}
~~~


The location of your PowerShell profile can be found with command

~~~bash
echo $profile
~~~

And is generally something like `C:\Users\{user}\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`.
