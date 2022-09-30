# Change Log

All changes to the package starting with v0.3.1 will be logged here.

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