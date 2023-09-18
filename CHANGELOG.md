# Change Log

* As of v1.4.0 release candidates will be published in an effort to get new features out faster while still allowing time for full QA testing before moving the release candidate to a full release.

## v1.5.0rc1 [2023-09-18]
#### What's New
* None

#### Enhancements
* Enrich shell completion results for the `api` command

#### Bug Fixes
* Fixes an issue with interactive login when randomly generated tokens include `--` which the WAF sometimes sees as a SQL injection attack
* Fixes an issue with `ssh-add` and temporary keys filling up the `ssh-agent` due to the order of command flags
* Fixes and issue with `checkin` checking in the wrong profile type (programmatic vs console)

#### Dependencies
* `britive>=2.21.0`

#### Other
* None


## v1.4.0 [2023-07-25]
#### What's New
* `pybritive ssh gcp identity-aware-proxy` command - supports OS Login and SSH Instance Metadata
* Command `request approve`
* Command `request reject`
* Command `ls approvals`

#### Enhancements
* Support for `sso_idp` in the tenant configuration block of the config file. Set with `configure update tenant-<name> sso_idp <value>`. This will enable automatic re-direction to your identity provider, thus eliminating a manual step when authenticating to your tenant.
* When checking in an AWS profile remove any AWS `credential_process` cached credentials.
* `clear cached-aws-credentials PROFILE`

#### Bug Fixes
* Better handling which submitting a request to checkout a profile but a prior request has already been approved.
* Properly catch and error when Cognito tokens have been invalidated.
* Resolved issue with profile alias names which included uppercase and special characters.
* Resolved an issue with `checkout --mode browser-*` that was not actually launching the browser.

#### Dependencies
* Fix dependabot alert for `requests` - https://github.com/britive/python-cli/security/dependabot/4
* Fix dependabot alert for `cryptography` - https://github.com/britive/python-cli/security/dependabot/5
* `britive>=2.20.1`

#### Other
* None


## v1.4.0rc6 [2023-06-27]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* Better handling which submitting a request to checkout a profile but a prior request has already been approved.

#### Dependencies
* `britive>=2.20.1`

#### Other
* None

## v1.4.0rc5 [2023-06-22]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* Fix bug with lowercase vs. uppercase when using tenant config attribute `sso_idp`.

#### Dependencies
* None

#### Other
* None

## v1.4.0rc4 [2023-06-22]
#### What's New
* `pybritive ssh gcp identity-aware-proxy` command - supports OS Login and SSH Instance Metadata

#### Enhancements
* Support for `sso_idp` in the tenant configuration block of the config file. Set with `configure update tenant-<name> sso_idp <value>`. This will enable automatic re-direction to your identity provider, thus eliminating a manual step when authenticating to your tenant.

#### Bug Fixes
* Properly catch and error when Cognito tokens have been invalidated.

#### Dependencies
* Fix dependabot alert for `requests` - https://github.com/britive/python-cli/security/dependabot/4
* Fix dependabot alert for `cryptography` - https://github.com/britive/python-cli/security/dependabot/5
* `britive>=2.20.0`

#### Other
* None


## v1.4.0rc3 [2023-05-16]
#### What's New
* None

#### Enhancements
* When checking in an AWS profile remove any AWS `credential_process` cached credentials.
* `clear cached-aws-credentials PROFILE`

#### Bug Fixes
* None

#### Dependencies
* None

#### Other
* None


## v1.4.0rc2 [2023-05-09]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* `checkout` bug when no `--mode/-m` is provided.

#### Dependencies
* None

#### Other
* None

## v1.4.0rc1 [2023-05-09]
#### What's New
* Command `request approve`
* Command `request reject`
* Command `ls approvals`

#### Enhancements
* None

#### Bug Fixes
* Resolved issue with profile alias names which included uppercase and special characters.
* Resolved an issue with `checkout --mode browser-*` that was not actually launching the browser.

#### Dependencies
* `britive>=2.19.0`

#### Other
* None

## v1.3.0 [2023-03-28]
#### What's New
* `pybritive ssh aws ssm-proxy` command
* `pybritive aws console` command

#### Enhancements
* Additional `--mode/-m` values
  * `console`: checkout console access (without having to specify --console/-c`) and print the URL
  * `browser-mozilla`: checkout console access and open a mozilla browser with the checked out URL
  * `browser-firefox`: checkout console access and open a firefox browser with the checked out URL
  * `browser-windows-default`: checkout console access and open a windows default browser with the checked out URL
  * `browser-macosx`: checkout console access and open a macosx browser with the checked out URL
  * `browser-safari`: checkout console access and open a safari browser with the checked out URL
  * `browser-chrome`: checkout console access and open a chrome browser with the checked out URL
  * `browser-chromium`: checkout console access and open a chromium browser with the checked out URL
* For the `checkout` command the option `--mode/-m` with values of `browser` and `console` now implicitly indicate that the console version of the profile should be checked out (without having to specify `--console/-c`)

#### Bug Fixes
* None

#### Dependencies
* `britive>=2.18.0`

#### Other
* Addition of Community Projects to the README.

## v1.2.2 [2023-03-17]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* Fix bug with `logout` command when no active credentials were available
* Expand `--silent/-s` flag to the following commands
  * `api`
  * `cache profiles`
  * `checkin`
  * `login`
  * `logout`
  * `ls [profiles|environments|applications|secrets]`
  * `request [submit|withdraw]`
  * `secret view`
  * `user`
* Fix bug when saving profile alias when the `PROFILE` is only 2 parts instead of 3

#### Dependencies
* None

#### Other
* None

## v1.2.1 [2023-03-14]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* `api` command shell completion fixed - dynamic sourcing of `method` values and options from the Britive Python SDK.

#### Dependencies
* `britive>=2.17.0`

#### Other
* None

## v1.2.0 [2023-03-03]
#### What's New
* Support for Azure Managed Identities as federation providers.

#### Enhancements
* Fall back to reduced functionality (no shell completion) when the python environment is using `click<8.0.0`.

#### Bug Fixes
* If a justification for checkout/secrets viewing is provided, ensure it is <=255 characters.
* Fix issue with extraction of OIDC token expiration time. Moved to `jwt` library to perform the token decode.

#### Dependencies
* Switching `britive` dependency from a compatible version requirement to a `>=` requirement to capture minor updates.
* `britive>=2.16.0` from britive~=2.15.1

#### Other
* Modify the error handling and reporting process to not raise `click.ClickException` exceptions in the `safe_cli` method. Instead, raise the underlying exception so a better error message is provided.

## v1.1.1 [2023-02-16]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* fix issue with `checkin`, `request submit`, `request withdrawl` due to `PROFILE` parameter changes

#### Dependencies
* None

#### Other
* None

## v1.1.0 [2023-02-16]
#### What's New
* Allowing 2 part `PROFILE` parameters (see documentation for details)
* Build support for multiple environment name formats (name, id, alternate environment name) for the `PROFILE` parameter

#### Enhancements
* None

#### Bug Fixes
* add a default checkout mode for AWS - bug fix as the effort is to match parity with legacy CLI tool

#### Dependencies
* None

#### Other
* None

## v1.0.0 [2023-02-09]
#### What's New
* Moving out of beta and into general availability. No other changes except for documentation updates reflecting the move out of beta.

#### Enhancements
* None

#### Bug Fixes
* None

#### Dependencies
* None

#### Other
* None

## v0.11.1 [2023-02-08]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* None
* 
#### Dependencies
* `cryptography~=39.0.1` to resolve dependabot alert #1 and #3
* `certifi>=2022.12.7` to resolve dependabot alert #2
* `britive~=2.15.0` to bring in new API calls

#### Other
* None

## v0.11.0 [2023-02-07]
#### What's New
* The `api` command is now available which exposes all the methods available in the Britive Python SDK.

#### Enhancements
* None

#### Bug Fixes
* None
* 
#### Dependencies
* None

#### Other
* Updated documentation with examples of how to use the new `api` command.

## v0.10.2 [2023-02-06]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* Fix issue with `checkout` and related commands that use the `PROFILE` positional argument when the one or more of the `PROFILE` components (application, environment, profile) have a `/` in the name. Caller must now properly escape any `/` with a `\`  (e.g. `AWS/Dev\/Test/Admin`).

#### Dependencies
* None

#### Other
* None

## v0.10.1 [2023-01-19]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* Fix interactive login issue for local development when using `BRITIVE_NO_VERIFY_SSL`

#### Dependencies
* None

#### Other
* None

## v0.10.0 [2023-01-18]
#### What's New
* Support Bitbucket as a federation provider

#### Enhancements
* None

#### Bug Fixes
* None

#### Dependencies
* `britive~=2.14.0` from `britive~=2.13.0` - bitbucket federation provider

#### Other
* None

## v0.9.2 [2023-01-11]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* Fix GCP console checkout issue

#### Dependencies
* None

#### Other
* None

## v0.9.1 [2023-01-09]
#### What's New
* None
* 
#### Enhancements
* None

#### Bug Fixes
* Fix console script `pybritive-aws-cred-process` due to recent changes with the `checkout` method

#### Dependencies
* None

#### Other
* None

## v0.9.0 [2023-01-06]
#### What's New
* `pybritive checkout` will now report progress of the action by default (if `stdout` is a tty). Can show more verbose output with `--verbose/-v`. Can silence the progress with the already available `--silent\-s` flag.

#### Enhancements
* None

#### Bug Fixes
* None

#### Dependencies
* `britive~=2.13.0` from `britive~=2.12.4` - checkout progress callback

#### Other
* None

## v0.8.0 [2023-01-05]
#### What's New
* Ability to store a GCP `gcloud` key file locally so `eval $(pybritive checkout "profile" -m gcloudauth)` will automatically authenticate the user with the gcloud CLI.
* Ability to override the default location of the GCP `gcloud` key file with `pybritive checkout "profile" -m gcloudauth --gcloud-key-file /path/to/key.json`
* New command `clear` with subcommands `cache` and `gcloud-key-files`. `cache` has same functionality as `pybritive cache clear` and `gcloud-key-files` will remove all `pybritive` generated temporary key files stored in the default location.

#### Enhancements
* None

#### Bug Fixes
* None

#### Dependencies
* `britive~=2.12.4` from `britive~=2.12.3` - AWS provider optional session token

#### Other
* None

## v0.7.2 [2022-12-12]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* None

#### Dependencies
* `britive~=2.12.3` from `britive~=2.12.2` - AWS provider tenant port removal, disable SSL verification, json decode bug fix

#### Other
* None

## v0.7.1 [2022-11-28]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* None

#### Dependencies
* `britive~=2.12.2` from `britive~=2.12.1` - AWS provider tenant logic fix

#### Other
* None

## v0.7.0 [2022-11-18]
#### What's New
> **_NOTE:_**  This is a pre-release feature. It is being published in anticipation of upcoming features being released to production. This functionality will not yet work in production environments.
* Support for workload identity federation providers 

#### Enhancements
* None

#### Bug Fixes
* None

#### Dependencies
* None

#### Other
* None

## v0.6.0 [2022-11-15]
#### What's New
* None

#### Enhancements
* When checking out a profile, the default is to check out programmatic access unless the `--console/-c` flag is set. This
enhancement will enable auto check out of console access if programmatic access is not available for the specified profile.

#### Bug Fixes
* None

#### Dependencies
* None

#### Other
* None

## v0.5.3 [2022-11-01]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* None

#### Dependencies
* `britive~=2.11.2` from `britive~=2.11.1` - reduced # of API calls required to checkout a profile

#### Other
* None

## v0.5.2 [2022-10-24]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* Allow local machine DNS to resolve (e.g. /etc/hosts) for tenant url

#### Dependencies
* `britive~=2.11.1` from `britive~=2.11.0`

#### Other
* None

## v0.5.1 [2022-10-21]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* Allow a port to be specified in a tenant URL

#### Dependencies
* `britive~=2.11.0` from `britive~=2.10.0`

#### Other
* None

## v0.5.0 [2022-10-11]
#### What's New
* None

#### Enhancements
* Allow for non `*.britive-app.com` tenants. Default to `britive-app.com` if no valid URL is provided (for backwards compatibility)

#### Bug Fixes
* None

#### Dependencies
* `britive~=2.10.0` from `britive~=2.9.0`

#### Other
* None

## v0.4.1 [2022-09-30]
#### What's New
* None

#### Enhancements
* None

#### Bug Fixes
* Fix and issue with `pybritive ls profile --checked-out` where all environments for the checked out profile were being returned instead of just the actual environments checked out.

#### Dependencies
* `britive~=2.9.0` from `britive~=2.8.0`

#### Other
* None

## v0.4.0 [2022-09-16]
#### What's New
* `pybritive-aws-cred-process` - a "side-car" helper script/CLI program that provides a minimal codebase in an effort to reduce the latency of obtaining credentials via the AWS `credential_process` command.

An example of how to use is below. Contents of `~/.aws/credentials`...

~~~
[profile-a]
credential_process=pybritive-aws-cred-process --profile britive-profile-alias
region=us-east-1
~~~

Note that the following is also still acceptable.

~~~
[profile-a]
credential_process=pybritive checkout britive-profile-alias -m awscredentialprocess
region=us-east-1
~~~

However, the former reduces the latency of the call by ~50% while still maintaining basic functionality.

#### Enhancements
* Provided a `GenericCloudCredentialPrinter` class which handles printing all cloud credentials not covered by a cloud specific credential printer.

#### Bug Fixes
* Fixes an issue when checking in a profile due to the `--force-renew` flag being set.

#### Dependencies
* None

#### Other
* None


## v0.3.1 [2022-09-13]
#### What's New
* None

### Enhancements
* None

#### Bug Fixes
* Fixes an issue with Britive tenant credential encryption when using `backend-credential-process=encrypted-file`. If an invalid `--passphrase` is provided the encrypted credentials will now be removed and a new interactive login process will commence.

#### Dependencies
* None

#### Other
* None