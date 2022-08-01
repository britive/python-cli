## Local Install

~~~
pip install --editable .
~~~

## Build

* Update version in `setup.cfg`
* Push code to GitHub
* Cut a new PR and merge when appropriate
* Run below commands


~~~
python -m pip install --upgrade build
python -m build
~~~

* Cut a new release in GitHub with the version tag
* Add the assets from `dist` directory to the release

## Testing
It is generally advisable to set environment variable `PYBRITIVE_HOME_DIR` to some temp location if you
will be performing the full suite of tests. This will ensure that no changes are made to your existing
configuration or credentials.

Set environment variable `PYBRITIVE_UNIT_TESTING` to any value if you do not want the `pytest` process to clean
up configuration/credential files in the `.britive` directory.

Other environment variables that should be set for testing include the following.

* `PYBRITIVE_TEST_TENANT` - the tenant name to be used for testing purposes
* `PYBRITIVE_NPM_IMPORT_PROFILE_ALIAS_VALUE` - the IDs of a profile that can be used to test the import process. This should be in format `"appid/envid/profileid/appname"`.

Create `./testing-variables.txt` and load what you need so you can easily re-create the needed variables. This file is in `.gitignore`. 