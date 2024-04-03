## Local Install

~~~
pip install --editable .
~~~

## Build

* Update version in `setup.cfg` and `src/pybritive/__init__.py` (TODO: create some pre-build script that will update one of these automatically)
* Push code to GitHub
* Cut a new PR and merge when appropriate
* Run below commands


~~~
python -m pip install --upgrade build
python -m build
~~~

* Cut a new release in GitHub with the version tag
* Add the assets from `dist` directory to the release

## Github Actions
There are 2 Github Actions in play that publish to PyPI.

1. Trigger off of a push to the `develop` branch. Will deploy to test PyPI.
2. Trigger off of a new release being published. Will deploy to real PyPI.

## Testing
It is generally advisable to set environment variable `PYBRITIVE_HOME_DIR` to some temp location if you
will be performing the full suite of tests. This will ensure that no changes are made to your existing
configuration or credentials.

Environment variables that should be set for testing include the following.

* `PYBRITIVE_HOME_DIR` - a path to a home directory where `.britive` directory will be created
* `PYBRITIVE_TEST_TENANT` - the tenant name to be used for testing purposes
* `PYBRITIVE_NPM_IMPORT_PROFILE_ALIAS_VALUE` - the IDs of a profile that can be used to test the import process. This should be in format `"appid/envid/profileid/appname"`.
* `PYBRITIVE_ENCRYPTED_CREDENTIAL_PASSPHRASE` - the password for encrypted file credential storage
* `PYBRITIVE_PREPARE_DOT_BRITIVE` - set to true if you want to have the `.britive` directory cleared before starting the tests
* `BRITIVE_API_TOKEN` - set if you want to avoid an interactive login process - the interactive login process will need to be tested separately

Create `./testing-variables.txt` and load what you need so you can easily re-create the needed variables. This file is in `.gitignore`. 

Package the code locally with `pip install -e .` so pytest can run against the python package.
Then `pytest tests/ -vvv` to perform the testing. 

The identity used for testing will require access to at least one profile to test `checkout` and `checkin`. 
Additionally, the identity will need access to 2 secrets
* one standard secret with path `/pybritive-test-standard` to test `view` - the value of the secret should be generic note with note of `test`
* one file secret with path `/pybritive-test-file` to test `download` - the filename should be `pybritive-test-secret-file.txt` and contain contents of `test`

## Docs

https://docs.readthedocs.io/en/stable/intro/getting-started-with-mkdocs.html

To set up the doc infrastructure the first time run the following from the base directory

~~~
pip install mkdocs
mkdocs new .
~~~

For real time local updates in HTML...
~~~
mkdocs serve
~~~

To build...

~~~
mkdocs build
~~~

This will create a new directory `site`.

As we are using source code control we have added `site/` to `.gitignore` so you will have to build the docs locally.

We will ultimately deploy via GitHub pages. But you can also copy everything in `site/` and host as a static website anywhere you want.

To deploy to GitHub project pages....

~~~
# checkout whichever branch is needed (main or develop most likely)
mkdocs gh-deploy
~~~

This will build the docs by performing the actions of `mkdocs build` and shove those built docs into the `gh-pages` branch of the repo.
`gh-pages` is auto-linked to `https://britive.github.io/python-cli/` and will update that site in near real time.