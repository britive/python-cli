# Change Log

All changes to the package starting with v0.3.1 will be logged here.

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