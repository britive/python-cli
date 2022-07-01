# Britive CLI - Pure Python Implementation

## Tenant Selection Logic

There are numerous ways to provide the CLI with the Britive tenant that should be used. The below list is the
order of operations for determining the tenant.

1. Value retrieved from CLI option/flag `--tenant`
2. Value retrieved from environment variable `BRITIVE_TENANT`
3. Value retrieved from `~/.pybritive/config.yaml` attribute key `default_tenant`
4. If none of the above are available then check for configured tenants in `~/.pybritive/config.yaml` and if there is only 1 tenant configured use it
5. If all the above fail then error


## Credential Selection Logic

There are numerous ways to provide the CLI with the Britive credentials that should be used to authenticate to the
Britive tenant. The below list is the order of operations for determining the tenant.

1. Value retrieved from CLI option/flag `--token`
2. Value retrieved from environment variable `BRITIVE_API_TOKEN`
3. If none of the above are available an interactive login will be performed and temporary credentials will be stored locally for future use of the CLI


## Credential Stores

The CLI offers a few ways in which temporary credentials obtained via interactive login can be stored.

* File: credentials will be stored in an unencrypted file located at `~/.pybritive/credentials.yaml`
* Encrypted File: credentials will be stored in an encrypted file located at `~/.pybritive/credentials.yaml`
* Vault: credentials will be stored in the local OS credential vault
    * MacOS: Keychain
    * Windows: Credential Vault
    * Linux: TODO