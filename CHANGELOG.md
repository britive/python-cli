# Changelog

> As of v1.4.0, release candidates will be published in an effort to get new features out faster while still allowing
> time for full QA testing before moving the release candidate to a full release.

## v2.1.4 [2025-04-02]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fixed missing environments when using `list` format with `ls profiles`

__Dependencies:__

* None

__Other:__

* None

## v2.1.3 [2025-03-31]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fixed missing catch for `ClickException` in `pybritive-aws-cred-process` after previous catch update change in `9bf6738f`

__Dependencies:__

* None

__Other:__

* None

## v2.1.2 [2025-03-14]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fixed missing underscore string replace in global field names.

__Dependencies:__

* None

__Other:__

* None

## v2.1.1 [2025-03-13]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Skip `construct_kube_config` if `env_properties` is missing.
* Retrieve `profileEnvironmentProperties` from `my_access.list_profiles` if the new API doesn't return the data.

__Dependencies:__

* None

__Other:__

* None

## v2.1.0 [2025-03-10]

__What's New:__

* `pybritive-aws-cred-process` can now prompt users for `otp` or `justification` when needed.
* `my_resource` profile checkouts can now specify a `response_template` by appending `/{template name}` to the profile.
* Added "Global Settings" section to docs site.

__Enhancements:__

* Added ITSM `--ticket-type` `--ticket-id` options.
* Additional `global` config settings: `my_[access|resources]_retrieval_limit` to limit size of retrieved items.

__Bug Fixes:__

* Fixed missing `exceptions.StepUpAuthRequiredButNotProvided` catch during `checkout`.

__Dependencies:__

* `britive>=4.1.2,<5.0`
* `colored>=2.2.5`

__Other:__

* Python 3.8 is EOL, so support is dropped.
* Allow `_` uniformity for `auto_refresh_[kube_config|profile_cache]` in `global` config.
* Tests and Documentation updates for SDK alignment.

## v2.1.0-rc.7 [2025-03-10]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fixed inverted `catalogAppDisplayName|catalogAppName` in `_set_available_profiles` and sped up generation.

__Dependencies:__

* None

__Other:__

* None

## v2.1.0-rc.6 [2025-03-06]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Return all profiles if not limited with `my_access_retrieval_limit`.

__Dependencies:__

* `britive>=4.1.2,<5.0`

__Other:__

* None

## v2.1.0-rc.5 [2025-03-06]

__What's New:__

* None

__Enhancements:__

* Return the desired quantity of actual profiles when using `my_access_retrieval_limit`.

__Bug Fixes:__

* None

__Dependencies:__

* None

__Other:__

* None

## v2.1.0-rc.4 [2025-03-06]

__What's New:__

* Added "Global Settings" section to docs site.

__Enhancements:__

* Additional `global` config settings: `my_[access|resources]_retrieval_limit` to limit size of retrieved items.

__Bug Fixes:__

* Fixed missing `exceptions.StepUpAuthRequiredButNotProvided` catch during `checkout`.

__Dependencies:__

* None

__Other:__

* Allow `_` uniformity for `auto_refresh_[kube_config|profile_cache]` in `global` config.

## v2.1.0-rc.3 [2025-02-28]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* `source_federation_token` is a util now.

__Dependencies:__

* None

__Other:__

* None

## v2.1.0-rc.2 [2025-02-28]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* `getopt` typo in `pybritive-aws-cred-process`

__Dependencies:__

* None

__Other:__

* None

## v2.1.0-rc.1 [2025-02-24]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* `colored>=2.2.5`

__Other:__

* Tests and Documentation updates for SDK alignment.

## v2.1.0-rc.0 [2025-01-27]

__What's New:__

* `pybritive-aws-cred-process` can now prompt users for `otp` or `justification` when needed.
* `my_resource` profile checkouts can now specify a `response_template` by appending `/{template name}` to the profile.

__Enhancements:__

* Added ITSM `--ticket-type` `--ticket-id` options.

__Bug Fixes:__

* None

__Dependencies:__

* `britive~=4.0`

__Other:__

* Python 3.8 is EOL, so support is dropped.

## v2.0.1 [2025-01-17]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* Pinned `britive` to major version 3.

__Other:__

* None

## v2.0.0 [2024-09-09]

__What's New:__

* Added colors to banner output.
* Added Step Up authentication to `my_secrets`

__Enhancements:__

* Switched to `ruff` for style linting and code-quality checking.

__Bug Fixes:__

* Fixed issue with global `default_tenant` test.

__Dependencies:__

* Dropped `python3.7` support.
* Dropped `pkg_resources` dependency.
* Upgrade `britive` to `>=3.0.0`
* Upgrade `click` to `>=8.1.7`

__Other:__

* Dropped legacy `import` functionality for the now long deprecated Node.js CLI.

## v1.8.3 [2024-08-20]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* `setuptools` when running in python 3.12 environments.

__Other:__

* None

## v1.8.2 [2024-07-26]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fixed a bug where checked out `my-resources` profiles weren't included.

__Dependencies:__

* None

__Other:__

* None

## v1.8.1 [2024-07-11]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fixed error related to `my-resources` not containing an `app_name`.

__Dependencies:__

* None

__Other:__

* None

## v1.8.0 [2024-07-01]

> _NOTE: This will be the last [minor](https://semver.org/#summary) version before 2.0.0_

__What's New:__

* Added a new global config setting for CA bundle certificates.
* Cloud PAM Anywhere - list, checkout, and checkin resources.
* Support for step up MFA/OTP when performing a `checkout`, using the `--otp` flag.

__Enhancements:__

* Added additional `clear kubeconfig` option to clear just the `pybritive` cached `kubeconfig` file.
* Added new `ca_bundle` global setting for user provided CA bundle certs.

__Bug Fixes:__

* check for enabled feature before listing `my-resources`.
* Fixed `python3.7` compatibility issues.
* Removed unexpected keyword argument from `hashlib.sha512` calls.
* missing `profile_type` kwarg in `ls profiles`.
* `None` type handling for `my-resources` profiles.
* Switched `pybritive-kube-exec` to full path in for kube config.

__Dependencies:__

* `britive>=2.25.0`
* Moved to minimally freezing dependencies.

__Other:__

* A `ca_bundle` being configured will override, or ignore, `REQUESTS_CA_BUNDLE` and `CURL_CA_BUNDLE`
* Documentation linting/conformity updates.
* Python linting changes.
* Resolve dependabot issue [dependabot/7](https://github.com/britive/python-cli/security/dependabot/7).
* Testing updates for `python3.7` compatability and warn when API token is present instead of fail.

## v1.8.0rc5 [2024-06-24]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* check for enabled feature before listing `my-resources`.

__Dependencies:__

* None

__Other:__

* None

## v1.8.0rc4 [2024-06-24]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* missing `profile_type` kwarg in `ls profiles`.
* `None` type handling for `my-resources` profiles.

__Dependencies:__

* None

__Other:__

* None

## v1.8.0rc3 [2024-06-07]

__What's New:__

* Cloud PAM Anywhere - list, checkout, and checkin resources.

__Enhancements:__

* Added additional `clear kubeconfig` option to clear just the `pybritive` cached `kubeconfig` file.

__Bug Fixes:__

* None

__Dependencies:__

* `britive>=2.25.0rc5`

__Other:__

* A `ca_bundle` being configured will override, or ignore, `REQUESTS_CA_BUNDLE` and `CURL_CA_BUNDLE`

## v1.8.0rc2 [2024-06-07]

__What's New:__

* Added a new global config setting for CA bundle certificates.

__Enhancements:__

* Added new `ca_bundle` global setting for user provided CA bundle certs.

__Bug Fixes:__

* Switched `pybritive-kube-exec` to full path in for kube config.

__Dependencies:__

* `britive>=2.25.0rc4`

__Other:__

* None

## v1.8.0rc1 [2024-06-03]

__What's New:__

* Support for step up MFA/OTP when performing a `checkout`, using the `--otp` flag.

__Enhancements:__

* None

__Bug Fixes:__

* Fixed `python3.7` compatibility issues.
* Removed unexpected keyword argument from `hashlib.sha512` calls.

__Dependencies:__

* `britive>=2.25.0rc3`
* Moved to minimally freezing dependencies.

__Other:__

* Documentation linting/conformity updates.
* Python linting changes.
* Resolve dependabot issue [dependabot/7](https://github.com/britive/python-cli/security/dependabot/7).
* Testing updates for `python3.7` compatability and warn when API token is present instead of fail.

## v1.7.0 [2024-04-17]

__What's New:__

* Display system announcement/banner if one is present for the tenant
* Support for OpenShift checkout modes `os-oclogin` and `os-ocloginexec`. These checkout modes will perform the OIDC
authorization code grant flow and extraction of the `oc login` command in code vs. having to use the browser. It is
a "best effort" approach as the OpenShift login pages and programmatic access pages could change over time.

__Enhancements:__

* New checkout mode of `gcloudauthexec` which will invoke, via sub-shell, the `gcloud auth activate-service-account`
command to switch credentials for `gcloud`. Additionally, a `checkin` will reset this configuration.
* Adds 3 part profile name for command `ls profiles -f json` - [#141](https://github.com/britive/python-cli/issues/141)

__Bug Fixes:__

* Fix issue related to the `cache` and `clear` commands when no global default tenant is set
* Fixes issue with `--force-renew` on `checkout` not providing the `--console` flag properly to `checkin`
* Flag `-p` was being used by `--maxpolltime` and `--passphrase` for command `checkout`. Switched `--maxpolltime` to
`-x`.

__Dependencies:__

* `britive>=2.24.0`
* Removal of `pkg_resources` dependency

__Other:__

* Documentation updates for `--federation-provider` and `spacelift`
* Documentation update for Azure Managed Identities
* Introduction of `__version__` in `__init.py__`
* Re-enabling the system banner/announcement logic

## v1.7.0rc3 [2024-04-03]

__What's New:__

* Support for OpenShift checkout modes `os-oclogin` and `os-ocloginexec`. These checkout modes will perform the OIDC
authorization code grant flow and extraction of the `oc login` command in code vs. having to use the browser. It is
a "best effort" approach as the OpenShift login pages and programmatic access pages could change over time.

__Enhancements:__

* Adds 3 part profile name for command `ls profiles -f json` - [#141](https://github.com/britive/python-cli/issues/141)

__Bug Fixes:__

* Fixes issue with `--force-renew` on `checkout` not providing the `--console` flag properly to `checkin`
* Flag `-p` was being used by `--maxpolltime` and `--passphrase` for command `checkout`. Switched `--maxpolltime` to
`-x`.

__Dependencies:__

* `britive>=2.24.0rc5`
* Removal of `pkg_resources` dependency

__Other:__

* Documentation updates for `--federation-provider` and `spacelift`
* Documentation update for Azure Managed Identities
* Introduction of `__version__` in `__init.py__`
* Re-enabling the system banner/announcement logic

## v1.7.0rc2 [2024-01-19]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Remove the banner logic as the banner api is not yet available in production

__Dependencies:__

* None

__Other:__

* None

## v1.7.0rc1 [2024-01-19]

__What's New:__

* Display system announcement/banner if one is present for the tenant

__Enhancements:__

* New checkout mode of `gcloudauthexec` which will invoke, via sub-shell, the `gcloud auth activate-service-account`
command to switch credentials for `gcloud`. Additionally, a `checkin` will reset this configuration.

__Bug Fixes:__

* Fix issue related to the `cache` and `clear` commands when no global default tenant is set

__Dependencies:__

* `britive>=2.24.0rc1`

__Other:__

* None

## v1.6.1 [2023-12-18]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fixes issue when an authentication token has been invalidated on the server side by discarding local credentials and
re-authenticating
* Send proper logout type based on the type of user (local or SAML)

__Dependencies:__

* None

__Other:__

* Additional debug logging related to the authentication process
* Remove logic for "safe token expiration" now that CLI and Browser tokens are shared
* Switch to extracting expiration time from the JWT instead of calculating based on auth time + session duration

## v1.6.1rc6 [2023-12-18]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* None

__Other:__

* Additional debug logging related to the authentication process

## v1.6.1rc5 [2023-12-15]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Switch to extracting expiration time from the JWT instead of calculating based on auth time + session duration

__Dependencies:__

* None

__Other:__

* Additional debug logging related to the authentication process

## v1.6.1rc4 [2023-12-14]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Remove logic for "safe token expiration" now that CLI and Browser tokens are shared

__Dependencies:__

* None

__Other:__

* None

## v1.6.1rc3 [2023-12-13]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Continuing to troubleshoot the `401 - EOOOO` login issue.

__Dependencies:__

* None

__Other:__

* None

## v1.6.1rc2 [2023-12-08]

__What's New:__

* None

__Enhancements:__

* Send proper logout type based on the type of user (local or SAML)

__Bug Fixes:__

* Fixes issue with `user` command

__Dependencies:__

* None

__Other:__

* Additional logging when entering a login/logout loop

## v1.6.1rc1 [2023-12-07]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fixes issue when an authentication token has been invalidated on the server side by auto-logging out the user from the
CLI and re-authenticating

__Dependencies:__

* None

__Other:__

* None

## v1.6.0 [2023-11-08]

__What's New:__

* Initial support for Kubernetes - this functionality is not yet available publicly on the Britive Platform - this is a
beta feature for internal use only

__Enhancements:__

* Add command `cache kubeconfig`
* Update command `cache clear` to delete the kube config file if it exists
* Add global config flag `auto-refresh-kube-config` set by `configure update global auto-refresh-kube-config true`
* Add checkout mode `k8s-exec` for use exclusively inside an `exec` command of a kube config file
* Add console helper script `pybritive-kube-exec` for use exclusively inside an `exec` command of a kube config file
* Add the `pybritive` package version into the `User-Agent` string used by the Britive Python SDK (`britive` package)
* For command `ls profiles -c` show the time remaining for the checkout
* Add new flag `-e/--extend` to command `checkout` which will extend the expiration time of a currently checked out
profile (only applicable to specific application types)

__Bug Fixes:__

* Clarified language in an error message when an authentication token has been invalidated on the server side and the
resulting action the user must take to clear the token
* Fix bug in `configure import` related to the default AWS checkout mode

__Dependencies:__

* `britive>=2.23.0`

__Other:__

* Documentation update to reflect that auto-login via browser will only work if the browser launched by `pybritive` is
the same as the browser where the user is already authenticated to Britive.

## v1.6.0rc5 [2023-11-06]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fix bug in `pybritive-kube-exec` and `pybritive-aws-cred-process` for handling the `--extend` flag of a `checkout`
command

__Dependencies:__

* None

__Other:__

* None

## v1.6.0rc4 [2023-11-03]

__What's New:__

* None

__Enhancements:__

* For command `ls profiles -c` show the time remaining for the checkout
* Add new flag `-e/--extend` to command `checkout` which will extend the expiration time of a currently checked out
profile (only applicable to specific application types)

__Bug Fixes:__

* Fix bug in `configure import` related to the default AWS checkout mode

__Dependencies:__

* None

__Other:__

* None

## v1.6.0rc3 [2023-10-31]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Clarified language in an error message when an authentication token has been invalidated on the server side and the
resulting action the user must take to clear the token.
* More gracefully handle when a Kubernetes `certificate-authority-data` cannot be base64 decoded to a proper
certificate - we will skip over that specific cluster.

__Dependencies:__

* None

__Other:__

* None

## v1.6.0rc2 [2023-10-27]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fixed bug with auto generated kube config when no alias existed for a profile.

__Dependencies:__

* None

__Other:__

* None

## v1.6.0rc1 [2023-10-25]

__What's New:__

* Initial support for Kubernetes - this functionality is not yet available publicly on the Britive Platform - this is a
beta feature for internal use only

__Enhancements:__

* Add command `cache kubeconfig`
* Update command `cache clear` to delete the kube config file if it exists
* Add global config flag `auto-refresh-kube-config` set by `configure update global auto-refresh-kube-config true`
* Add checkout mode `k8s-exec` for use exclusively inside an `exec` command of a kube config file
* Add console helper script `pybritive-kube-exec` for use exclusively inside an `exec` command of a kube config file
* Add the `pybritive` package version into the `User-Agent` string used by the Britive Python SDK (`britive` package)

__Bug Fixes:__

* None

__Dependencies:__

* None

__Other:__

* Documentation update on bash command to add the python `bin` path to your `PATH` environment variable.

## v1.5.0 [2023-10-20]

__What's New:__

* None

__Enhancements:__

* Enrich shell completion results for the `api` command
* Support `browser` option for `login` command
* Support environment variable `PYBRITIVE_BROWSER` to allow a user to specify a default browser option, as well as use
non-standard `webbrowser` options.

__Bug Fixes:__

* Fixes an issue with interactive login when randomly generated tokens include `--` which the WAF sometimes sees as a
SQL injection attack
* Fixes an issue with `ssh-add` and temporary keys filling up the `ssh-agent` due to the order of command flags
* Fixes and issue with `checkin` checking in the wrong profile type (programmatic vs console)
* Fixes bug which did not always honor the specified browser.

__Dependencies:__

* `britive>=2.22.0`

__Other:__

* Various linting
* Updates to the documentation calling out the requirement to properly escape input based on the shell you are using
* Resolve dependabot issue [dependabot/6](https://github.com/britive/python-cli/security/dependabot/6)
* Documentation updates

## v1.5.0rc3 [2023-10-13]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* `britive>=2.22.0`

__Other:__

* Updates to the documentation calling out the requirement to properly escape input based on the shell you are using
* Resolve dependabot issue [dependabot/6](https://github.com/britive/python-cli/security/dependabot/6)

## v1.5.0rc2 [2023-09-18]

__What's New:__

* None

__Enhancements:__

* Support `browser` option for `login` command
* Support environment variable `PYBRITIVE_BROWSER` to allow a user to specify a default browser option, as well as use
non-standard `webbrowser` options.

__Bug Fixes:__

* Fixes bug which did not always honor the specified browser.

__Dependencies:__

* None

__Other:__

* Various linting

## v1.5.0rc1 [2023-09-18]

__What's New:__

* None

__Enhancements:__

* Enrich shell completion results for the `api` command

__Bug Fixes:__

* Fixes an issue with interactive login when randomly generated tokens include `--` which the WAF sometimes sees as a
SQL injection attack
* Fixes an issue with `ssh-add` and temporary keys filling up the `ssh-agent` due to the order of command flags
* Fixes and issue with `checkin` checking in the wrong profile type (programmatic vs console)

__Dependencies:__

* `britive>=2.21.0`

__Other:__

* None

## v1.4.0 [2023-07-25]

__What's New:__

* `pybritive ssh gcp identity-aware-proxy` command - supports OS Login and SSH Instance Metadata
* Command `request approve`
* Command `request reject`
* Command `ls approvals`

__Enhancements:__

* Support for `sso_idp` in the tenant configuration block of the config file. Set with `configure update tenant-<name>
sso_idp <value>`. This will enable automatic re-direction to your identity provider, thus eliminating a manual step
when authenticating to your tenant.
* When checking in an AWS profile remove any AWS `credential_process` cached credentials.
* `clear cached-aws-credentials PROFILE`

__Bug Fixes:__

* Better handling which submitting a request to checkout a profile but a prior request has already been approved.
* Properly catch and error when Cognito tokens have been invalidated.
* Resolved issue with profile alias names which included uppercase and special characters.
* Resolved an issue with `checkout --mode browser-*` that was not actually launching the browser.

__Dependencies:__

* Fix dependabot alert for `requests` - [dependabot/4](https://github.com/britive/python-cli/security/dependabot/4)
* Fix dependabot alert for `cryptography` - [dependabot/5](https://github.com/britive/python-cli/security/dependabot/5)
* `britive>=2.20.1`

__Other:__

* None

## v1.4.0rc6 [2023-06-27]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Better handling which submitting a request to checkout a profile but a prior request has already been approved.

__Dependencies:__

* `britive>=2.20.1`

__Other:__

* None

## v1.4.0rc5 [2023-06-22]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fix bug with lowercase vs. uppercase when using tenant config attribute `sso_idp`.

__Dependencies:__

* None

__Other:__

* None

## v1.4.0rc4 [2023-06-22]

__What's New:__

* `pybritive ssh gcp identity-aware-proxy` command - supports OS Login and SSH Instance Metadata

__Enhancements:__

* Support for `sso_idp` in the tenant configuration block of the config file. Set with `configure update tenant-<name>
sso_idp <value>`. This will enable automatic re-direction to your identity provider, thus eliminating a manual step
when authenticating to your tenant.

__Bug Fixes:__

* Properly catch and error when Cognito tokens have been invalidated.

__Dependencies:__

* Fix dependabot alert for `requests` - [dependabot/4](https://github.com/britive/python-cli/security/dependabot/4)
* Fix dependabot alert for `cryptography` - [dependabot/5](https://github.com/britive/python-cli/security/dependabot/5)
* `britive>=2.20.0`

__Other:__

* None

## v1.4.0rc3 [2023-05-16]

__What's New:__

* None

__Enhancements:__

* When checking in an AWS profile remove any AWS `credential_process` cached credentials.
* `clear cached-aws-credentials PROFILE`

__Bug Fixes:__

* None

__Dependencies:__

* None

__Other:__

* None

## v1.4.0rc2 [2023-05-09]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* `checkout` bug when no `--mode/-m` is provided.

__Dependencies:__

* None

__Other:__

* None

## v1.4.0rc1 [2023-05-09]

__What's New:__

* Command `request approve`
* Command `request reject`
* Command `ls approvals`

__Enhancements:__

* None

__Bug Fixes:__

* Resolved issue with profile alias names which included uppercase and special characters.
* Resolved an issue with `checkout --mode browser-*` that was not actually launching the browser.

__Dependencies:__

* `britive>=2.19.0`

__Other:__

* None

## v1.3.0 [2023-03-28]

__What's New:__

* `pybritive ssh aws ssm-proxy` command
* `pybritive aws console` command

__Enhancements:__

* Additional `--mode/-m` values
  * `console`: checkout console access (without having to specify --console/-c`) and print the URL
  * `browser-mozilla`: checkout console access and open a mozilla browser with the checked out URL
  * `browser-firefox`: checkout console access and open a firefox browser with the checked out URL
  * `browser-windows-default`: checkout console access and open a windows default browser with the checked out URL
  * `browser-macosx`: checkout console access and open a macosx browser with the checked out URL
  * `browser-safari`: checkout console access and open a safari browser with the checked out URL
  * `browser-chrome`: checkout console access and open a chrome browser with the checked out URL
  * `browser-chromium`: checkout console access and open a chromium browser with the checked out URL
* For the `checkout` command the option `--mode/-m` with values of `browser` and `console` now implicitly indicate that
the console version of the profile should be checked out (without having to specify `--console/-c`)

__Bug Fixes:__

* None

__Dependencies:__

* `britive>=2.18.0`

__Other:__

* Addition of Community Projects to the README.

## v1.2.2 [2023-03-17]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

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

__Dependencies:__

* None

__Other:__

* None

## v1.2.1 [2023-03-14]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* `api` command shell completion fixed - dynamic sourcing of `method` values and options from the Britive Python SDK.

__Dependencies:__

* `britive>=2.17.0`

__Other:__

* None

## v1.2.0 [2023-03-03]

__What's New:__

* Support for Azure Managed Identities as federation providers.

__Enhancements:__

* Fall back to reduced functionality (no shell completion) when the python environment is using `click<8.0.0`.

__Bug Fixes:__

* If a justification for checkout/secrets viewing is provided, ensure it is <=255 characters.
* Fix issue with extraction of OIDC token expiration time. Moved to `jwt` library to perform the token decode.

__Dependencies:__

* Switching `britive` dependency from a compatible version requirement to a `>=` requirement to capture minor updates.
* `britive>=2.16.0` from britive~=2.15.1

__Other:__

* Modify the error handling and reporting process to not raise `click.ClickException` exceptions in the `safe_cli`
method. Instead, raise the underlying exception so a better error message is provided.

## v1.1.1 [2023-02-16]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* fix issue with `checkin`, `request submit`, `request withdrawl` due to `PROFILE` parameter changes

__Dependencies:__

* None

__Other:__

* None

## v1.1.0 [2023-02-16]

__What's New:__

* Allowing 2 part `PROFILE` parameters (see documentation for details)
* Build support for multiple environment name formats (name, id, alternate environment name) for the `PROFILE` parameter

__Enhancements:__

* None

__Bug Fixes:__

* add a default checkout mode for AWS - bug fix as the effort is to match parity with legacy CLI tool

__Dependencies:__

* None

__Other:__

* None

## v1.0.0 [2023-02-09]

__What's New:__

* Moving out of beta and into general availability. No other changes except for documentation updates reflecting the
move out of beta.

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* None

__Other:__

* None

## v0.11.1 [2023-02-08]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* `cryptography~=39.0.1` to resolve dependabot alert #1 and #3
* `certifi>=2022.12.7` to resolve dependabot alert #2
* `britive~=2.15.0` to bring in new API calls

__Other:__

* None

## v0.11.0 [2023-02-07]

__What's New:__

* The `api` command is now available which exposes all the methods available in the Britive Python SDK.

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* None

__Other:__

* Updated documentation with examples of how to use the new `api` command.

## v0.10.2 [2023-02-06]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fix issue with `checkout` and related commands that use the `PROFILE` positional argument when the one or more of the
`PROFILE` components (application, environment, profile) have a `/` in the name. Caller must now properly escape any `/`
with a `\`  (e.g. `AWS/Dev\/Test/Admin`).

__Dependencies:__

* None

__Other:__

* None

## v0.10.1 [2023-01-19]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fix interactive login issue for local development when using `BRITIVE_NO_VERIFY_SSL`

__Dependencies:__

* None

__Other:__

* None

## v0.10.0 [2023-01-18]

__What's New:__

* Support Bitbucket as a federation provider

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* `britive~=2.14.0` from `britive~=2.13.0` - bitbucket federation provider

__Other:__

* None

## v0.9.2 [2023-01-11]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fix GCP console checkout issue

__Dependencies:__

* None

__Other:__

* None

## v0.9.1 [2023-01-09]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fix console script `pybritive-aws-cred-process` due to recent changes with the `checkout` method

__Dependencies:__

* None

__Other:__

* None

## v0.9.0 [2023-01-06]

__What's New:__

* `pybritive checkout` will now report progress of the action by default (if `stdout` is a tty). Can show more verbose
output with `--verbose/-v`. Can silence the progress with the already available `--silent\-s` flag.

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* `britive~=2.13.0` from `britive~=2.12.4` - checkout progress callback

__Other:__

* None

## v0.8.0 [2023-01-05]

__What's New:__

* Ability to store a GCP `gcloud` key file locally so `eval $(pybritive checkout "profile" -m gcloudauth)` will
automatically authenticate the user with the gcloud CLI.
* Ability to override the default location of the GCP `gcloud` key file with `pybritive checkout "profile" -m gcloudauth
--gcloud-key-file /path/to/key.json`
* New command `clear` with subcommands `cache` and `gcloud-key-files`. `cache` has same functionality as `pybritive
cache clear` and `gcloud-key-files` will remove all `pybritive` generated temporary key files stored in the default
location.

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* `britive~=2.12.4` from `britive~=2.12.3` - AWS provider optional session token

__Other:__

* None

## v0.7.2 [2022-12-12]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* `britive~=2.12.3` from `britive~=2.12.2` - AWS provider tenant port removal, disable SSL verification, json decode bug
fix

__Other:__

* None

## v0.7.1 [2022-11-28]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* `britive~=2.12.2` from `britive~=2.12.1` - AWS provider tenant logic fix

__Other:__

* None

## v0.7.0 [2022-11-18]

__What's New:__

> ___NOTE:___  This is a pre-release feature. It is being published in anticipation of upcoming features being released
to production. This functionality will not yet work in production environments.

* Support for workload identity federation providers

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* None

__Other:__

* None

## v0.6.0 [2022-11-15]

__What's New:__

* None

__Enhancements:__

* When checking out a profile, the default is to check out programmatic access unless the `--console/-c` flag is set.
This enhancement will enable auto check out of console access if programmatic access is not available for the specified
profile.

__Bug Fixes:__

* None

__Dependencies:__

* None

__Other:__

* None

## v0.5.3 [2022-11-01]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* None

__Dependencies:__

* `britive~=2.11.2` from `britive~=2.11.1` - reduced # of API calls required to checkout a profile

__Other:__

* None

## v0.5.2 [2022-10-24]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Allow local machine DNS to resolve (e.g. /etc/hosts) for tenant url

__Dependencies:__

* `britive~=2.11.1` from `britive~=2.11.0`

__Other:__

* None

## v0.5.1 [2022-10-21]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Allow a port to be specified in a tenant URL

__Dependencies:__

* `britive~=2.11.0` from `britive~=2.10.0`

__Other:__

* None

## v0.5.0 [2022-10-11]

__What's New:__

* None

__Enhancements:__

* Allow for non `*.britive-app.com` tenants. Default to `britive-app.com` if no valid URL is provided (for backwards
compatibility)

__Bug Fixes:__

* None

__Dependencies:__

* `britive~=2.10.0` from `britive~=2.9.0`

__Other:__

* None

## v0.4.1 [2022-09-30]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fix and issue with `pybritive ls profile --checked-out` where all environments for the checked out profile were being
returned instead of just the actual environments checked out.

__Dependencies:__

* `britive~=2.9.0` from `britive~=2.8.0`

__Other:__

* None

## v0.4.0 [2022-09-16]

__What's New:__

* `pybritive-aws-cred-process` - a "side-car" helper script/CLI program that provides a minimal codebase in an effort
to reduce the latency of obtaining credentials via the AWS `credential_process` command.

An example of how to use is below. Contents of `~/.aws/credentials`...

```toml
[profile-a]
credential_process=pybritive-aws-cred-process --profile britive-profile-alias
region=us-east-1
```

Note that the following is also still acceptable.

```toml
[profile-a]
credential_process=pybritive checkout britive-profile-alias -m awscredentialprocess
region=us-east-1
```

However, the former reduces the latency of the call by ~50% while still maintaining basic functionality.

__Enhancements:__

* Provided a `GenericCloudCredentialPrinter` class which handles printing all cloud credentials not covered by a cloud
specific credential printer.

__Bug Fixes:__

* Fixes an issue when checking in a profile due to the `--force-renew` flag being set.

__Dependencies:__

* None

__Other:__

* None

## v0.3.1 [2022-09-13]

__What's New:__

* None

__Enhancements:__

* None

__Bug Fixes:__

* Fixes an issue with Britive tenant credential encryption when using `backend-credential-process=encrypted-file`. If an
invalid `--passphrase` is provided the encrypted credentials will now be removed and a new interactive login process
will commence.

__Dependencies:__

* None

__Other:__

* None
