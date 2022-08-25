---
**NOTE**

This is a BETA release. This codebase should not be used for production workloads.

---

# Britive CLI - Pure Python Implementation

PyBritive is intended to be used as a CLI application for communicating with the Britive Platform.

## Installation

`pybritive` will be installed via Python `pip`. The package is not available in PyPi at this time, so it will be 
installed via the published tar balls in the GitHub repo. Determine the most recent version that has been published
and add the version below.

~~~bash
version=x.y.z
pip install https://github.com/britive/python-cli/releases/download/v$version/pybritive-$version.tar.gz
~~~

Or you can always pull the latest version using one of the following commands

~~~
pip install $(curl -s https://api.github.com/repos/britive/python-cli/releases/latest | jq -r '.assets[] | select(.content_type == "application/x-gzip") | .browser_download_url')

OR

pip install $(curl -s https://api.github.com/repos/britive/python-cli/releases/latest | grep "browser_download_url.*.tar.gz" | cut -d : -f 2,3 | tr -d \")
~~~

The end user is free to install the CLI into a virtual environment or in the global scope, so it is available
everywhere.


## Documentation

https://britive.github.io/python-cli/


